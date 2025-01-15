import requests
from langchain_fireworks import FireworksEmbeddings
import os

class AzureDevOpsConnector:
    def __init__(self, azure_devops_url, pat, project):
        self.azure_devops_url = azure_devops_url
        self.pat = pat
        self.project = project

    def fetch_tickets(self, query):
        url = f"{self.azure_devops_url}/{self.project}/_apis/wit/wiql?api-version=6.0"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Basic {self.pat}"
        }
        data = {
            "query": query
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        work_items = response.json()["workItems"]
        tickets = []
        for item in work_items:
            ticket_url = f"{self.azure_devops_url}/_apis/wit/workItems/{item['id']}?api-version=6.0"
            ticket_response = requests.get(ticket_url, headers=headers)
            ticket_response.raise_for_status()
            tickets.append(ticket_response.json())
        return tickets

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
