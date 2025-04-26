from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta
from enum import Enum


class TicketSourceEnum(Enum):
    AZURE = "AZURE"
    JIRA = "JIRA"

class UserRequirement(BaseModel):
    id: str
    source: TicketSourceEnum
    ticket_id: str
    title: str
    description: str
    additional_description: Optional[str]
    images: Optional[list[str]]
    embedding_field: list[float]
    ingested_at: Optional[datetime]
    embedded_at: Optional[datetime]
    ingestion_job_id: Optional[str]
    embedding_job_id: Optional[str]

    def model_dump(self):
        data = super().model_dump()
        data['source'] = self.source.value  # Convert Enum to string
        return data