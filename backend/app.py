import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from backend.jira_connector import JiraConnector
from backend.embedding_storage import EmbeddingStorage
from dotenv import load_dotenv

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

@app.post("/ingest")
async def ingest(request: IngestRequest):
    try:
        jira_connector = JiraConnector(
            jira_url=os.getenv("JIRA_URL"),
            username=os.getenv("JIRA_USERNAME"),
            api_token=os.getenv("JIRA_API_TOKEN")
        )
        jql = f"project={request.ProjectKey} ORDER BY created DESC"
        tickets = jira_connector.fetch_tickets(jql)[:request.MaxTickets]
        embeddings = jira_connector.convert_to_embeddings(tickets)
        
        embedding_storage = EmbeddingStorage(
            mongo_uri=os.getenv("MONGO_URI"),
            db_name=os.getenv("DB_NAME"),
            collection_name=os.getenv("COLLECTION_NAME")
        )
        embedding_storage.store_embeddings(embeddings)
        
        return {"message": "Ingestion successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
