from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class DocumentRecord(SQLModel, table=True):
    """
    Represents a document in the database.
    The sanitized_text will be populated asynchronously by the Celery worker.
    """
    id: int | None = Field(default=None, primary_key=True)
    doc_id: str = Field(index=True)
    sanitized_text: str | None = Field(default=None)
    status: str = Field(default="PENDING")

# Using SQLite for intial local development to reduce dependencies(will migrate to Postgres via Docker in next phase).
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread":False}
engine = create_engine(sqlite_url,connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]