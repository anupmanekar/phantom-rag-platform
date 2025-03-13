from azure_devops_adapter import AzureDevOpsAdapter
from command_interface import CommandInterface

class FetchTicketsCommand(CommandInterface):
    def __init__(self, adapter: AzureDevOpsAdapter, query: str):
        self.adapter = adapter
        self.query = query

    def execute(self):
        return self.adapter.fetch_tickets(self.query)

class ConvertToEmbeddingsCommand(CommandInterface):
    def __init__(self, adapter: AzureDevOpsAdapter, tickets: list):
        self.adapter = adapter
        self.tickets = tickets

    def execute(self):
        return self.adapter.convert_to_embeddings(self.tickets)
