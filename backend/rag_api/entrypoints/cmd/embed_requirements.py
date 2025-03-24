from rag_api.infrastructure.bindings import di
from rag_api.infrastructure.ports import VectorDBPort
from rag_api.domain.user_requirement import UserRequirement
from google.cloud.firestore_v1.vector import Vector
import os
from dotenv import load_dotenv

load_dotenv()

def embed_requirements(vector_db: VectorDBPort):
    try:
        print("Embedding Requirements in Vector DB")
        for doc in vector_db.iterate_documents():
            print(f"Embedding document: {doc.to_dict()['ticket_id']}")
            document = doc.to_dict()
            user_requirement = UserRequirement.model_validate(document)
            embedded_user_requirement = vector_db.embed_doc(user_requirement)
            #vector_db.update_document(document_id=doc.id, document=embedded_user_requirement)
            vector_db.update_document_with_embedding(document_id=doc.id, embedding=embedded_user_requirement.embedding_field)
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
   embed_requirements(di["FirestoreVectorDB"])