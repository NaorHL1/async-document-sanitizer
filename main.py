from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from database import create_db_and_tables, DocumentRecord, SessionDep


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


class Document(BaseModel):
    doc_id: str
    text: str


app = FastAPI(
    title="Enterprise PII Gateway",
    description="Async ingestion service for sanitizing sensitive documents.",
    lifespan=lifespan
)

security = HTTPBearer()


@app.post("/api/v1/documents/ingest", status_code=202)
async def ingest_document(
    doc: Document,
    response: Response,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: SessionDep
):
    """
    Ingests a new document payload for asynchronous PII masking.

    Required a valid JWT Beared token. metadata saved to database
    immediately with a PENDING status, while text will be queued
    for background processing.
    """
    
    new_record = DocumentRecord(doc_id=doc.doc_id, status="PENDING")

    session.add(new_record)
    session.commit()

    return {"task_id": "temp-task-123", "status": "PENDING"}
