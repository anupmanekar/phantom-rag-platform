import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from backend.jira_connector import JiraConnector
from backend.azure_devops_connector import AzureDevOpsConnector
from backend.embedding_storage import EmbeddingStorage
from backend.llm_handler import LLMHandler
from backend.rag_operations import RAGOperations
from dotenv import load_dotenv
from fastapi.openapi.utils import get_openapi

load_dotenv()

app = FastAPI()

azure_connector = AzureDevOpsConnector.get_instance(
            azure_devops_url=os.environ.get("AZURE_DEVOPS_URL"),
            pat=os.environ.get("AZURE_DEVOPS_PAT"),
            project=os.environ.get("AZURE_DEVOPS_PROJECT"),
            username=os.environ.get("AZURE_DEVOPS_USERNAME")
        )

jira_connector = JiraConnector.get_instance(
            jira_url=os.getenv("JIRA_URL"),
            username=os.getenv("JIRA_USERNAME"),
            api_token=os.getenv("JIRA_API_TOKEN")
        )

embedding_storage = EmbeddingStorage.get_instance(
            mongo_uri=os.environ.get("MONGO_URI"),
            db_name=os.environ.get("DB_NAME"),
            collection_name=os.environ.get("COLLECTION_NAME")
        )

llm_handler = LLMHandler()

rag_operations = RAGOperations(embedding_storage, llm_handler)

class Query(BaseModel):
    query: str

class IngestRequest(BaseModel):
    ProjectKey: str
    MaxTickets: int
    IngestionType: str

@app.post("/search")
async def search(query: Query):
    try:
        results = rag_operations.search(query.query)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest-jira")
async def ingest_jira(request: IngestRequest):
    try:
        response = embedding_storage.ingest_jira(jira_connector, request.ProjectKey, request.MaxTickets)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ingest-azure")
async def ingest_azure():
    try:
        response = embedding_storage.ingest_azure(azure_connector, os.environ.get("AZURE_DEVOPS_PROJECT"))
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Jira RAG App",
        version="1.0.0",
        description="API documentation for the Jira RAG App",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
