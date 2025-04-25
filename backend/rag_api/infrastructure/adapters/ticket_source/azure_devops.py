import requests
from datetime import date, datetime, time, timedelta
from requests.auth import HTTPBasicAuth
from langchain_fireworks import FireworksEmbeddings
import os
from kink import inject
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking.models import Wiql, WorkItem
from rag_api.domain.user_requirement import UserRequirement
from azure.devops.v7_1.work_item_tracking.work_item_tracking_client import WorkItemTrackingClient
from rag_api.infrastructure.ports import RequirementsStorePort
import re

class AzureDevopsAdapter(RequirementsStorePort):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AzureDevopsAdapter, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, azure_devops_url, username, pat, project):
        if not hasattr(self, 'initialized'):
            self.azure_devops_url = azure_devops_url
            self.pat = pat
            self.project = project
            self.username = username
            self.auth = HTTPBasicAuth(username, pat)
            self.initialized = True

    @classmethod
    def get_instance(cls, azure_devops_url=None, username=None, pat=None, project=None):
        if not cls._instance:
            cls._instance = cls(azure_devops_url, username, pat, project)
        return cls._instance

    def fetch_tickets_via_rest(self, query):
        url = f"{self.azure_devops_url}/{self.project}/_apis/wit/wiql?api-version=6.0"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Basic {self.pat}"
        }
        data = {
            "query": query
        }
        response = requests.post(url, headers=headers, json=data, auth=self.auth)
        response.raise_for_status()
        work_items = response.json()["workItems"]
        tickets = []
        for item in work_items:
            ticket_url = f"{self.azure_devops_url}/_apis/wit/workItems/{item['id']}?api-version=6.0"
            ticket_response = requests.get(ticket_url, headers=headers)
            ticket_response.raise_for_status()
            tickets.append(ticket_response.json())
        return tickets
    
    def fetch_tickets(self, query) -> list[WorkItem]:
        credentials = BasicAuthentication(self.username, self.pat)
        connection = Connection(base_url=self.azure_devops_url, creds=credentials)

        # Get a client (the "core" client provides access to projects, teams, etc)
        work_client = connection.clients.get_work_item_tracking_client()
        wiql = Wiql(query=query)
        
        wiql_results = work_client.query_by_wiql(wiql, top=60).work_items
        if wiql_results:
            work_items = (work_client.get_work_item(int(res.id)) for res in wiql_results)
            return [item for item in work_items]
        return []

    def convert_to_embeddings(self, tickets: list[WorkItem]):
        embeddings = FireworksEmbeddings(model='nomic-ai/nomic-embed-text-v1.5')
        ticket_embeddings = []
        for ticket in tickets:
            ticket_dict = ticket.as_dict()
            description = ticket_dict['fields']['System.Description'] if 'System.Description' in ticket_dict['fields'] else ''
            ticket_data = f"{ticket_dict['fields']['System.Title']}"
            embedding = embeddings.embed_documents(ticket_data)
            ticket_embeddings.append({
                "ticket_id": ticket.id,
                "ticket_title": ticket_dict['fields']['System.Title'],
                "embedding": embedding[0],
                "description": description
            })
            print(f"Ticket {ticket.id} processed")
        return ticket_embeddings

    def convert_tickets_to_user_requirements(self, tickets: list[WorkItem]) -> list[UserRequirement]:
        user_requirements = []
        for ticket in tickets:
            ticket_dict = ticket.as_dict()
            description = ticket_dict['fields']['System.Description'] if 'System.Description' in ticket_dict['fields'] else ''
            image_tags = re.findall(r'<img src="([^"]+)"', description)
            images = []
            for tag in image_tags:
                images.append(tag)
            user_requirements.append(UserRequirement(
                ticket_id=str(ticket_dict['id']),
                title=ticket_dict['fields']['System.Title'],
                description=description,
                images=images,
                embedding_field=[],
                additional_description=None,
                ingested_at=datetime.now(),
                embedded_at=None,
                embedding_job_id=None,
                ingestion_job_id=None
            ))
        return user_requirements
    
    def download_attachment(self, url):
        """Download attachment from Azure DevOps"""
        response = requests.get(url, auth=('', self.pat))
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to download attachment: {response.status_code}")