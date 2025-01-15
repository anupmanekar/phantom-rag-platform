import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from backend.jira_connector import JiraConnector
from backend.azure_devops_connector import AzureDevOpsConnector
from backend.embedding_storage import EmbeddingStorage
from dotenv import load_dotenv
from fastapi.openapi.utils import get_openapi

load_dotenv()

app = FastAPI()

class Query(BaseModel):
    query: str

class IngestRequest(BaseModel):
    ProjectKey: str
    MaxTickets: int
    IngestionType: str

@app.post("/search")
async def search(query: Query):
    try:
        # Placeholder for search functionality integration
        results = ["result1", "result2", "result3", "result4", "result5"]
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest-jira")
async def ingest_jira(request: IngestRequest):
    try:
        jira_connector = JiraConnector(
            jira_url=os.getenv("JIRA_URL"),
            username=os.getenv("JIRA_USERNAME"),
            api_token=os.getenv("JIRA_API_TOKEN")
        )
        jql = f"project = {request.ProjectKey} ORDER BY created DESC"
        tickets = jira_connector.fetch_tickets(jql)[:request.MaxTickets]
        embeddings = jira_connector.convert_to_embeddings(tickets)
        
        embedding_storage = EmbeddingStorage(
            mongo_uri=os.environ.get("MONGO_URI"),
            db_name=os.environ.get("DB_NAME"),
            collection_name=os.environ.get("COLLECTION_NAME")
        )
        embedding_storage.store_embeddings(embeddings)
        
        return {"message": "Ingestion successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ingest-azure")
async def ingest_azure():
    try:
        print("Ingesting Azure DevOps")
        azure_connector = AzureDevOpsConnector(
            azure_devops_url=os.environ.get("AZURE_DEVOPS_URL"),
            pat=os.environ.get("AZURE_DEVOPS_PAT"),
            project=os.environ.get("AZURE_DEVOPS_PROJECT"),
            username=os.environ.get("AZURE_DEVOPS_USERNAME")
        )
        project = os.environ.get("AZURE_DEVOPS_PROJECT")
        # query = f"Select [System.Id], [System.Title], [System.Description] From WorkItems Where [System.TeamProject] = '{request.ProjectKey}'"
        query = f"Select [System.Id], [System.Title], [System.Description] From WorkItems Where [System.WorkItemType] = 'Task' and [System.TeamProject] = '{project}'"
        #tickets = azure_connector.fetch_tickets(query)[:request.MaxTickets]
        tickets = azure_connector.fetch_tickets(query)[:50]
        embeddings = azure_connector.convert_to_embeddings(tickets)
        embedding_storage = EmbeddingStorage(
            mongo_uri=os.environ.get("MONGO_URI"),
            db_name=os.environ.get("DB_NAME"),
            collection_name=os.environ.get("COLLECTION_NAME")
        )
        embedding_storage.store_embeddings(embeddings)
        
        return {"message": "Ingestion successful"}
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
