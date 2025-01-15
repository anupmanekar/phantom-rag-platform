import requests
from requests.auth import HTTPBasicAuth
from langchain_fireworks import FireworksEmbeddings
import os
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking.models import Wiql, WorkItem

class AzureDevOpsConnector:
    def __init__(self, azure_devops_url, username, pat, project):
        self.azure_devops_url = azure_devops_url
        self.pat = pat
        self.project = project
        self.username = username
        self.auth = HTTPBasicAuth(username, pat)

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


    def convert_to_embeddings(self, tickets):
        embeddings = FireworksEmbeddings()
        ticket_embeddings = []
        for ticket in tickets:
            ticket_data = f"{ticket['id']} {ticket['fields']['System.Title']} {ticket['fields']['System.Description']}"
            embedding = embeddings.encode(ticket_data)
            ticket_embeddings.append({
                "ticket_id": ticket["id"],
                "embedding": embedding
            })
        return ticket_embeddings
