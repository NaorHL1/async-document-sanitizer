from typing import Annotated

from fastapi import FastAPI, Response, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

class Document(BaseModel):
    doc_id: str
    text: str

app = FastAPI()

security = HTTPBearer()

@app.post("/api/v1/documents/ingest", status_code=202)
async def ingest_document(doc: Document, response: Response,credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    return {"task_id":"temp-task-123","status":"PENDING8"}
    



