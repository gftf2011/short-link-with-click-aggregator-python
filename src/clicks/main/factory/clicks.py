from functools import cache

from clicks.handler.count_clicks.count_clicks_handler import CountClicksHandler
from clicks.infra.buffer.redis_clicks_buffer import RedisClicksBuffer
from clicks.infra.tasks.celery_count_clicks_task import CeleryCountClicksTask
from shared.infra.celery_broker import celery_app
from shared.infra.celery_mediator import CeleryMediator
from shared.infra.redis_database import redis_client_for_clicks
from shared.domain.events.shortlink_clicked_event import ShortlinkClickedEvent


@cache
def worker() -> CeleryMediator:
    buffer = RedisClicksBuffer(redis_client=redis_client_for_clicks())
    handler = CountClicksHandler(buffer=buffer)
    task = CeleryCountClicksTask(handler=handler)

    app = celery_app()
    app.register_task(task)

    mediator = CeleryMediator()
    mediator.subscribe(ShortlinkClickedEvent, task)

    return mediator
