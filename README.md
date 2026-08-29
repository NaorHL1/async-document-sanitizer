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

### ADR 002: Asynchronous Background Processing
* **Context:** PII redaction (Regex masking) in large documents is a CPU-bound operation. Running this on the main API event loop will block incoming requests and cause timeouts. We need a reliable mechanism to offload this processing.

* **Alternatives Considered:** 
  1. **Temporal.io:** Rejected. While providing excellent durable execution, the operational overhead (4-container control plane) is too heavy for this specific microservice scope.
  2. **Taskiq / FastStream:** Rejected. Extremely fast and modern, but lacks mature enterprise monitoring tools and native polyglot/cross-language support.
  3. **FastAPI BackgroundTasks:** Rejected. Lacks persistence; tasks are permanently lost if the API pod restarts.
  4. **Celery + Redis:** Evaluated as the optimal choice.
* **Decision:** Selected **Celery** as the task queue, with **Redis** as the message broker, and **Flower** for real-time observability.
* **Reasoning:** Since PII regex scanning is CPU-bound rather than I/O-bound, Celery's synchronous worker model is not a bottleneck here. Furthermore, Celery provides a highly mature ecosystem, guarantees message persistence (zero data loss on API restart), and Flower provides enterprise-grade visual monitoring out-of-the-box.


## 💻 How to Run (Local Dev)
1. Clone the repo.
2. Start the Docker infrastructure (Database & Queue): 
   ```bash
   docker compose up -d
3. Install dependencies using uv (Fastest Python package manager):
uv pip install -r requirements.txt
4. Run the API server:
uv run fastapi dev