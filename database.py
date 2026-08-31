import os

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine

DB_PASSWORD = os.getenv("DB_PASSWORD", "example")

class DocumentRecord(SQLModel, table=True):
    """
    Represents a document in the database.
    The sanitized_text will be populated asynchronously by the Celery worker.
    """
    id: int | None = Field(default=None, primary_key=True)
    doc_id: str = Field(index=True)
    sanitized_text: str | None = Field(default=None)
    status: str = Field(default="PENDING")


postgres_url = f"postgresql://postgres:{DB_PASSWORD}@db:5432/postgres"
engine = create_engine(postgres_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]