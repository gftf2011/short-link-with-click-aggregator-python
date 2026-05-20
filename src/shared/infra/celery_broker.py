import os

from celery import Celery

_celery_app: Celery | None = None


def reset_celery_app() -> None:
    global _celery_app
    _celery_app = None


def celery_app() -> Celery:
    global _celery_app
    if _celery_app is None:
        broker_url = os.getenv("CELERY_BROKER_URL")
        if not broker_url:
            raise ValueError("CELERY_BROKER_URL is not set")
        backend_url = os.getenv("CELERY_RESULT_BACKEND_URL")
        _celery_app = Celery("short_link", broker=broker_url, backend=backend_url)
        _celery_app.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            task_acks_late=True,
            worker_prefetch_multiplier=10,
        )
    return _celery_app
