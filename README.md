# Enterprise PII Gateway (Async Ingestion) 🛡️
A production-grade FastAPI microservice designed to ingest enterprise documents, perform asynchronous PII masking (redacting credit cards/sensitive data), and persist the sanitized data to PostgreSQL.
## 🚀 Current Features (Phase 2 - Database Integration)
- **FastAPI Ingestion Endpoint:** `POST /api/v1/documents/ingest`
- **Retrieval Endpoint:** `GET /api/v1/documents/{doc_id}`
- **Authentication:** Enforced JWT / Bearer Token validation (`HTTPBearer`).
- **Data Validation:** Strict schema validation using Pydantic.
- **Database Persistence:** Fully integrated PostgreSQL via Docker with SQLModel ORM.
- **Database UI:** Adminer interface available for monitoring at `localhost:8080`.
## 🛠️ Tech Stack
- **API Framework:** FastAPI
- **Authentication:** HTTPBearer (Dependency Injection)
- **Database:** PostgreSQL & SQLModel
- **Infrastructure:** Docker Compose (Postgres, Adminer, Redis)
- *(Upcoming)* **Background Processing:** Celery & Redis


## 💻 How to Run (Local Dev)
1. Clone the repo.
2. Start the Docker infrastructure (Database & Queue): 
   ```bash
   docker compose up -d
3. Install dependencies using uv (Fastest Python package manager):
uv pip install -r requirements.txt
4. Run the API server:
uv run fastapi dev