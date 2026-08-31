import os
import jwt

from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlmodel import select
from database import create_db_and_tables, DocumentRecord, SessionDep, HTTPException

from tasks import mask_pii_document


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


JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-fde-signature-key")
def verify_jwt(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        # מנסים לפענח את הטוקן עם החותמת הסודית שלנו
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        return payload # אם הצליח, מחזירים את התוכן של הטוקן
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token signature")


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
    # Calling worker
    task = mask_pii_document.delay(doc.doc_id,doc.text)

    new_record = DocumentRecord(doc_id=doc.doc_id, status="PENDING")
    session.add(new_record)
    session.commit()
    token_payload: dict = Depends(verify_jwt)

    return {"task_id": task.id, "status": "PENDING"}


@app.get("/api/v1/document/{doc_id}")
async def get_document(
    doc_id: str,
    credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)],
    session: SessionDep
):
    """
    Retrieves a document's status and sanitized text from the database.
    """

    statement = select(DocumentRecord).where(DocumentRecord.doc_id == doc_id)

    document = session.exec(statement).first()

    if not document:
        return {"error": "Document not found"}

    return document