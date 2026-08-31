from python:3.12-slim
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.12.7 /uv /uvx /bin/

COPY requirements.txt ./

RUN uv pip install --system --no-cache -r requirements.txt

COPY main.py database.py tasks.py celery_app.py config.py ./

CMD ["fastapi", "run", "main.py", "--port", "8000"]
