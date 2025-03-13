from backend.commands.command_interface import CommandInterface
from backend.jira_adapter import JiraAdapter

class FetchTicketsCommand(CommandInterface):
    def __init__(self, jira_adapter: JiraAdapter, jql: str):
        self.jira_adapter = jira_adapter
        self.jql = jql

    def execute(self):
        return self.jira_adapter.fetch_tickets(self.jql)

class ConvertToEmbeddingsCommand(CommandInterface):
    def __init__(self, jira_adapter: JiraAdapter, tickets):
        self.jira_adapter = jira_adapter
        self.tickets = tickets

    def execute(self):
        return self.jira_adapter.convert_to_embeddings(self.tickets)
