from abc import ABC, abstractmethod

class VectorDBPort(ABC):
    @abstractmethod
    def store_embeddings(self, embeddings):
        pass

    @abstractmethod
    def search_embeddings(self, query_embedding, threshold=0.8):
        pass

    @abstractmethod
    def get_document(self, criteria):
        pass

class LLMPort(ABC):
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        pass

class RequirementsStorePort(ABC):
    @abstractmethod
    def fetch_tickets(self, query: str):
        pass

    @abstractmethod
    def convert_to_embeddings(self, tickets):
        pass