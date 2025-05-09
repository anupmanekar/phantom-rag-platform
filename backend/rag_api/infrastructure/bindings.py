import os
from kink import di
from rag_api.infrastructure.adapters.ticket_source.azure_devops import AzureDevopsAdapter
from rag_api.infrastructure.adapters.ticket_source.jira import JiraAdapter
from rag_api.infrastructure.adapters.vectordb.mongodb import MongoVectorDBAdapter
from rag_api.infrastructure.adapters.llm.fireworksai import FireworksLLMAdapter
from rag_api.infrastructure.adapters.llm.documentai import DocumentAILLMAdapter
from rag_api.infrastructure.adapters.llm.googlegenai import GoogleGenAILLMAdapter
from rag_api.infrastructure.adapters.vectordb.firestore import FirestoreVectorDBAdapter
from rag_api.infrastructure.ports import VectorDBPort, LLMPort, RequirementsStorePort

di["AzureRequirements"] = lambda _: AzureDevopsAdapter.get_instance (
                azure_devops_url=os.environ.get("AZURE_DEVOPS_URL"),
                pat=os.environ.get("AZURE_DEVOPS_PAT"),
                project=os.environ.get("AZURE_DEVOPS_PROJECT"),
                username=os.environ.get("AZURE_DEVOPS_USERNAME")
            )
di["JiraRequirements"] = lambda _: JiraAdapter.get_instance(
                jira_url=os.getenv("JIRA_URL"),
                username=os.getenv("JIRA_USERNAME"),
                api_token=os.getenv("JIRA_API_TOKEN")
            )
di[LLMPort] = lambda _: FireworksLLMAdapter()
di["DocumentAILLM"] = lambda _: DocumentAILLMAdapter(gcp_project_id=os.environ.get("GCP_PROJECT_ID"))
di["GoogleGenAILLM"] = lambda _: GoogleGenAILLMAdapter()
di[VectorDBPort] = lambda _: MongoVectorDBAdapter.get_instance(
                mongo_uri=os.environ.get("MONGO_URI"),
                db_name=os.environ.get("DB_NAME"),
                collection_name=os.environ.get("COLLECTION_NAME")
            )
di["FirestoreVectorDB"] = lambda _: FirestoreVectorDBAdapter.get_instance(
                project_id=os.environ.get("GCP_PROJECT_ID"),
                db_name=os.environ.get("FIRESTORE_DB_NAME"),
                collection_name=os.environ.get("FIRESTORE_COLLECTION_NAME")
            )
