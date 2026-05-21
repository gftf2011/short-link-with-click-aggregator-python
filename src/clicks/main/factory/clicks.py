from functools import cache

from sqlalchemy.ext.asyncio import AsyncSession

from clicks.handler.count_clicks.count_clicks_handler import CountClicksHandler
from clicks.infra.buffer.redis_clicks_buffer import RedisClicksBuffer
from clicks.infra.repositories.sqlalchemy_clicks_repository import SqlAlchemyClicksRepository
from clicks.infra.tasks.celery_aggregate_clicks_task import CeleryAggregateClicksTask
from clicks.infra.tasks.celery_count_clicks_task import CeleryCountClicksTask
from clicks.infra.tasks.celery_flush_clicks_task import CeleryFlushClicksTask
from clicks.presentation.api.clicks_api_controller import ClicksApiController
from clicks.usecases.get_clicks_count_by_short_code.get_clicks_count_by_short_code_use_case import (
    GetClicksCountByShortCodeUseCase,
)
from shared.domain.events.shortlink_clicked_event import ShortlinkClickedEvent
from shared.infra.celery_broker import celery_app
from shared.infra.celery_mediator import CeleryMediator
from shared.infra.in_memory_mediator import InMemoryMediator
from shared.infra.redis_database import sync_redis_client_for_clicks


def http(session: AsyncSession) -> ClicksApiController:
    repository = SqlAlchemyClicksRepository(session=session)
    use_case = GetClicksCountByShortCodeUseCase(clicks_repository=repository)
    return ClicksApiController(get_clicks_count_use_case=use_case)

@cache
def api_mediator() -> InMemoryMediator:
    buffer = RedisClicksBuffer(redis_client=sync_redis_client_for_clicks())
    handler = CountClicksHandler(buffer=buffer)

    mediator = InMemoryMediator()
    mediator.subscribe(ShortlinkClickedEvent, handler)

    return mediator


@cache
def worker() -> CeleryMediator:
    buffer = RedisClicksBuffer(redis_client=sync_redis_client_for_clicks())
    handler = CountClicksHandler(buffer=buffer)
    task = CeleryCountClicksTask(handler=handler)

    app = celery_app()
    app.register_task(task)

    mediator = CeleryMediator()
    mediator.subscribe(ShortlinkClickedEvent, task)

    return mediator


@cache
def scheduler() -> None:
    aggregate_task = CeleryAggregateClicksTask()
    flush_task = CeleryFlushClicksTask()

    app = celery_app()
    app.register_task(aggregate_task)
    app.register_task(flush_task)
    app.conf.beat_schedule = {
        **app.conf.beat_schedule,
        "aggregate-clicks-every-10-seconds": {
            "task": aggregate_task.name,
            "schedule": 10.0,
        },
        "flush-clicks-every-1-minute": {
            "task": flush_task.name,
            "schedule": 60.0,
        },
    }
