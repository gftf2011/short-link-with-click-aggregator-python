import atexit

from main.worker.bootstrap.boot import boot
from main.worker.loader.load import load
from clicks.main.factory.clicks import scheduler, worker
from shared.infra.celery_broker import celery_app
from shared.infra.redis_database import sync_redis_client_for_clicks

boot()
load()
worker()
scheduler()

app = celery_app()

atexit.register(sync_redis_client_for_clicks().close)
