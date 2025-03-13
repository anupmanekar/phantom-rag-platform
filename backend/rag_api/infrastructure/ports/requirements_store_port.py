from abc import ABC, abstractmethod

class RequirementsStorePort(ABC):
    @abstractmethod
    def fetch_tickets(self, query: str):
        pass

    @abstractmethod
    def convert_to_embeddings(self, tickets):
        pass
