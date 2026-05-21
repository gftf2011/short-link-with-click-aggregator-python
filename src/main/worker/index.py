from main.worker.bootstrap.boot import boot
from main.worker.loader.load import load
from clicks.main.factory.clicks import scheduler, worker
from shared.infra.celery_broker import celery_app

boot()
load()
worker()
scheduler()

app = celery_app()
