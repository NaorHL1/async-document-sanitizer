# Enterprise PII Gateway (Async Ingestion) 🛡️

A production-grade FastAPI microservice designed to ingest enterprise documents, perform asynchronous PII masking (redacting credit cards/sensitive data), and persist the sanitized data to PostgreSQL.

## 🚀 Current Features (Phase 1)
- **FastAPI Ingestion Endpoint:** `POST /api/v1/documents/ingest`
- **Authentication:** Enforced JWT / Bearer Token validation (`HTTPBearer`).
- **Data Validation:** Strict schema validation using Pydantic.

## 🛠️ Tech Stack
- **API Framework:** FastAPI
- **Authentication:** HTTPBearer (Dependency Injection)
- *(Upcoming)* **Background Processing:** Celery & Redis
- *(Upcoming)* **Database:** PostgreSQL & SQLAlchemy / Alembic

## 💻 How to Run (Local Dev)
1. Clone the repo.
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `uvicorn main:app --reload`