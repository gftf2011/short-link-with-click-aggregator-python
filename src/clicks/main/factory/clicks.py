from functools import cache

from clicks.handler.count_clicks.count_clicks_handler import CountClicksHandler
from clicks.infra.buffer.redis_clicks_buffer import RedisClicksBuffer
from clicks.infra.tasks.celery_aggregate_clicks_task import CeleryAggregateClicksTask
from clicks.infra.tasks.celery_count_clicks_task import CeleryCountClicksTask
from shared.domain.events.shortlink_clicked_event import ShortlinkClickedEvent
from shared.infra.celery_broker import celery_app
from shared.infra.celery_mediator import CeleryMediator
from shared.infra.redis_database import redis_client_for_clicks


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


@cache
def scheduler() -> None:
    task = CeleryAggregateClicksTask()

    app = celery_app()
    app.register_task(task)
    app.conf.beat_schedule = {
        **app.conf.beat_schedule,
        "aggregate-clicks-every-minute": {
            "task": task.name,
            "schedule": 60.0,
        },
    }
