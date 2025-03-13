from abc import ABC, abstractmethod

class EmbeddingStoragePort(ABC):
    @abstractmethod
    def store_embeddings(self, embeddings):
        pass

    @abstractmethod
    def search_embeddings(self, query_embedding, threshold=0.8):
        pass

    @abstractmethod
    def get_document(self, criteria):
        pass
