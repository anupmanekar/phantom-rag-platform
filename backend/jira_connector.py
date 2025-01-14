import requests
from fireworksai import Embeddings
import os

class JiraConnector:
    def __init__(self):
        self.jira_url = os.getenv("JIRA_URL")
        self.auth = (os.getenv("JIRA_USERNAME"), os.getenv("JIRA_API_TOKEN"))

    def fetch_tickets(self, jql):
        url = f"{self.jira_url}/rest/api/2/search"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        params = {
            "jql": jql
        }
        response = requests.get(url, headers=headers, params=params, auth=self.auth)
        response.raise_for_status()
        return response.json()["issues"]

    def convert_to_embeddings(self, tickets):
        embeddings = Embeddings()
        ticket_embeddings = []
        for ticket in tickets:
            ticket_data = f"{ticket['key']} {ticket['fields']['summary']} {ticket['fields']['description']}"
            embedding = embeddings.encode(ticket_data)
            ticket_embeddings.append({
                "ticket_id": ticket["id"],
                "embedding": embedding
            })
        return ticket_embeddings
