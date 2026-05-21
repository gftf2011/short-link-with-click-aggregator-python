import asyncio
from collections import defaultdict
from datetime import datetime

from celery import Task

from shared.domain.event import Event
from shared.handlers.mediator import Mediator


def _to_json_safe(event: Event) -> dict:
    return {
        k: v.isoformat() if isinstance(v, datetime) else v
        for k, v in event.__dict__.items()
    }


class CeleryMediator(Mediator):
    def __init__(self) -> None:
        self._tasks: dict[type[Event], list[Task]] = defaultdict(list)

    def subscribe(self, event_type: type[Event], task: Task) -> None:
        self._tasks[event_type].append(task)

    async def publish(self, events: list[Event]) -> None:
        for event in events:
            for task in self._tasks[type(event)]:
                asyncio.create_task(
                    asyncio.to_thread(task.delay, _to_json_safe(event))
                )
