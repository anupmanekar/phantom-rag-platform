import os
from kink import inject
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import uvicorn
from rag_api.infrastructure.bindings import di
from rag_api.infrastructure.ports import LLMPort, VectorDBPort, RequirementsStorePort
from rag_api.usecases.rag_handler import RAGHandler
from dotenv import load_dotenv
from fastapi.openapi.utils import get_openapi
from rag_api.infrastructure.monitoring.observability import getLogger

logger = getLogger(__name__)

load_dotenv()

app = FastAPI()

class Query(BaseModel):
    query: str

class IngestRequest(BaseModel):
    ProjectKey: str
    MaxTickets: int
    IngestionType: str

@app.get("/generate-bdd-for-ticket")
async def generate_bdd(ticket_id: int, llm_service: LLMPort = Depends(lambda: di["GoogleGenAILLM"]), 
                    vector_db: VectorDBPort = Depends(lambda: di["FirestoreVectorDB"])) -> JSONResponse:
    try:
        rag_handler = RAGHandler(llm_service, vector_db)
        results = rag_handler.generate_bdd_for_ticket_from_firestore(ticket_id)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate-bdd-for-features")
async def generate_bdd(description: str, llm_service: LLMPort = Depends(lambda: di["GoogleGenAILLM"]), 
                    vector_db: VectorDBPort = Depends(lambda: di["FirestoreVectorDB"])) -> JSONResponse:
    try:
        rag_handler = RAGHandler(llm_service, vector_db)
        results = rag_handler.generate_bdd_for_features(features=description)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer-query")
async def search(query: Query, llm_service: LLMPort = Depends(lambda: di["GoogleGenAILLM"]), 
                    vector_db: VectorDBPort = Depends(lambda: di["FirestoreVectorDB"])) -> JSONResponse:
    try:
        rag_handler = RAGHandler(llm_service, vector_db)
        results = rag_handler.answer_query(query.query)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest-jira")
async def ingest_jira(request: IngestRequest, requirements_service: RequirementsStorePort = Depends(lambda: di["JiraRequirements"]), 
                       vector_db: VectorDBPort = Depends(lambda: di[VectorDBPort])) -> JSONResponse:
    try:
        jql = f"project = {request.ProjectKey} ORDER BY created DESC"
        tickets = requirements_service.fetch_tickets(jql)[:request.MaxTickets]
        embeddings = requirements_service.convert_to_embeddings(tickets)
        
        vector_db.store_documents(embeddings)
        
        return {"message": "Ingestion successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ingest-azure-in-mongodb")
async def ingest_azure(requirements_service: RequirementsStorePort = Depends(lambda: di["AzureRequirements"]), 
                       vector_db: VectorDBPort = Depends(lambda: di[VectorDBPort])) -> JSONResponse:
    try:
        print("Ingesting Azure DevOps")
        project = os.environ.get("AZURE_DEVOPS_PROJECT")
        # query = f"Select [System.Id], [System.Title], [System.Description] From WorkItems Where [System.TeamProject] = '{request.ProjectKey}'"
        query = f"Select [System.Id], [System.Title], [System.Description] From WorkItems Where [System.WorkItemType] = 'Task' and [System.TeamProject] = '{project}'"
        #tickets = azure_connector.fetch_tickets(query)[:request.MaxTickets]
        tickets = requirements_service.fetch_tickets(query)[:100]
        embeddings = requirements_service.convert_to_embeddings(tickets)
        vector_db.store_documents(embeddings)
        
        return {"message": "Ingestion successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ingest-azure-in-firestore")
async def ingest_requirements(requirements_service: RequirementsStorePort = Depends(lambda: di["AzureRequirements"]), 
                       vector_db: VectorDBPort = Depends(lambda: di["FirestoreVectorDB"])) -> JSONResponse:
    try:
        print("Ingesting Azure DevOps")
        project = os.environ.get("AZURE_DEVOPS_PROJECT")
        # query = f"Select [System.Id], [System.Title], [System.Description] From WorkItems Where [System.TeamProject] = '{request.ProjectKey}'"
        query = f"Select [System.Id], [System.Title], [System.Description] From WorkItems Where [System.WorkItemType] = 'Task' and [System.TeamProject] = '{project}'"
        #tickets = azure_connector.fetch_tickets(query)[:request.MaxTickets]
        tickets = requirements_service.fetch_tickets(query)[:100]
        user_requirements = requirements_service.convert_tickets_to_user_requirements(tickets)
        vector_db.store_documents(user_requirements)
        return {"message": "Ingestion successful"}
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="QA RAG Based Services",
        version="1.0.0",
        description="API documentation for the QA RAG App",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
