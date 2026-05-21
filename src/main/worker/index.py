from main.worker.bootstrap.boot import boot
from clicks.main.factory.clicks import scheduler, worker
from shared.infra.celery_broker import celery_app

boot()
worker()
scheduler()

app = celery_app()
