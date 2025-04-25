from abc import ABC, abstractmethod
import typing

from rag_api.domain.user_requirement import UserRequirement

class VectorDBPort(ABC):
    @abstractmethod
    def embed_all_docs(self, documents: list[UserRequirement]) -> list[UserRequirement]:
        pass

    @abstractmethod
    def embed_doc(self, document: UserRequirement) -> UserRequirement:
        pass

    @abstractmethod
    def store_documents(self, documents: list[UserRequirement]):
        pass

    @abstractmethod
    def search_embeddings(self, query_embedding, threshold=0.8):
        pass

    @abstractmethod
    def get_document(self, criteria):
        pass

    @abstractmethod
    def iterate_documents(self):
        pass

    @abstractmethod
    def update_document_with_additional_info(self, document_id, additional_info):
        pass

    @abstractmethod
    def update_document_with_embedding(self, document_id, embedding):
        pass

    @abstractmethod
    def update_document(self, document_id, document):
        pass

class LLMPort(ABC):
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        pass

    @abstractmethod
    def ask_question_on_image(self, image_loc: any, image_bytes:any, question: str) -> any:
        pass

class RequirementsStorePort(ABC):
    @abstractmethod
    def fetch_tickets(self, query: str):
        pass

    @abstractmethod
    def convert_to_embeddings(self, tickets):
        pass

    @abstractmethod
    def convert_tickets_to_user_requirements(self, tickets) -> list[UserRequirement]:
        pass

    @abstractmethod
    def download_attachment(self, url):
        pass