import os

from celery import Celery

_celery_app: Celery | None = None


def reset_celery_app() -> None:
    global _celery_app
    _celery_app = None


def celery_app() -> Celery:
    global _celery_app
    if _celery_app is None:
        host = os.getenv("REDIS_FOR_CLICKS_HOST")
        if not host:
            raise ValueError("REDIS_FOR_CLICKS_HOST is not set")
        port = os.getenv("REDIS_FOR_CLICKS_PORT", "6381")
        username = os.getenv("REDIS_FOR_CLICKS_USERNAME", "")
        password = os.getenv("REDIS_FOR_CLICKS_PASSWORD", "")
        credentials = f"{username}:{password}@" if username else ""
        broker_url = f"redis://{credentials}{host}:{port}/0"
        backend_url = broker_url
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
