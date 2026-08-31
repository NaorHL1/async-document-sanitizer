from celery import Celery

# 1. Initialize Celery to point to our Redis container
celery_app = Celery(
    "pii_worker",
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['tasks']
)

