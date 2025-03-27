from rag_api.domain.user_requirement import UserRequirement
from rag_api.infrastructure.ports import VectorDBPort
from google.cloud import firestore
from langchain_google_firestore import FirestoreVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
from google.cloud.firestore_v1.vector import Vector
from rag_api.infrastructure.monitoring.observability import getLogger

logger = getLogger(__name__)

class FirestoreVectorDBAdapter(VectorDBPort):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FirestoreVectorDBAdapter, cls).__new__(cls)
        return cls._instance

    def __init__(self, project_id, db_name, collection_name):
        if not hasattr(self, 'initialized'):
            logger.info(f"Connecting to Firestore at {project_id}")
            self.client = firestore.Client(project=project_id, database=db_name)
            self.db = firestore.Client(project=project_id, database=db_name)
            self.collection = self.client.collection(collection_name)
            self.embeddings = VertexAIEmbeddings(model_name="text-embedding-004",
                                project=project_id)
            self.vector_store = FirestoreVectorStore(
                                    collection=collection_name,
                                    embedding_service=self.embeddings,
                                    embedding_field="embedding_field",
                                )
            self.initialized = True

    @classmethod
    def get_instance(cls, project_id=None, db_name=None, collection_name=None):
        if not cls._instance:
            cls._instance = cls(project_id, db_name, collection_name)
        return cls._instance

    def store_documents(self, documents: list[UserRequirement]):
        for doc in documents:
            print(f"Ingesting document: {doc.ticket_id}")
            self.collection.add(doc.model_dump())
        return

    def search_embeddings(self, query_embedding, threshold=0.8):
        return []
    
    def get_document(self, criteria):
        logger.info(f"Getting document with criteria: {criteria}")
        criteria_key = list(criteria.keys())[0]
        criteria_value = str(criteria[criteria_key])
        print(f"Criteria: {criteria_key} - {criteria_value}")
        docs = self.collection.where(filter=firestore.FieldFilter(criteria_key, "==", criteria_value)).get()
        for doc in docs:
            logger.info(f"Document retrieved: {doc}")
        logger.info(f"Document retrieved: {docs}")
        return docs[0] if len(docs) > 0 else None

    def embed_doc(self, doc: UserRequirement) -> UserRequirement:
        doc.embedding_field = self.embeddings.embed_query(doc.title)
        return doc

    def embed_all_docs(self, documents: list[UserRequirement]) -> list[UserRequirement]:
        if (len(documents) == 0):
            documents = self.collection.stream()
        for doc in documents:
            doc = self.embed_doc(doc)
        return documents

    def iterate_documents(self):
        docs = self.collection.stream()
        for doc in docs:
            yield doc if doc.exists else None
    
    def update_document_with_additional_info(self, document_id, additional_info):
        print(f"Updating document with additional info: {document_id} - {additional_info}")
        return self.collection.document(document_id=document_id).update({"additional_description": additional_info})
    
    def update_document_with_embedding(self, document_id, embedding):
        print(f"Updating document with embedding: {document_id}")
        return self.collection.document(document_id=document_id).update({"embedding_field": Vector(embedding)})

    def update_document(self, document_id, document):
        print(f"Updating document with embedding: {document_id}")
        return self.collection.document(document_id=document_id).set(document, merge=True)
        
