from rag_api.infrastructure.bindings import di
from rag_api.infrastructure.ports import LLMPort, VectorDBPort, RequirementsStorePort
import os
from dotenv import load_dotenv

load_dotenv()

def ingest_requirements(requirements_service: RequirementsStorePort, vector_db: VectorDBPort):
    try:
        print("Ingesting Azure DevOps")
        project = os.environ.get("AZURE_DEVOPS_PROJECT")
        # query = f"Select [System.Id], [System.Title], [System.Description] From WorkItems Where [System.TeamProject] = '{request.ProjectKey}'"
        query = f"Select [System.Id], [System.Title], [System.Description] From WorkItems Where [System.WorkItemType] = 'Task' and [System.TeamProject] = '{project}'"
        #tickets = azure_connector.fetch_tickets(query)[:request.MaxTickets]
        tickets = requirements_service.fetch_tickets(query)[:100]
        user_requirements = requirements_service.convert_tickets_to_user_requirements(tickets)
        vector_db.store_documents(user_requirements)
        print(f"message: Ingestion successful")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
   ingest_requirements(di["AzureRequirements"], di["FirestoreVectorDB"])