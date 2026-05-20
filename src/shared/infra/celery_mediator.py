from collections import defaultdict

from celery import Task

from shared.domain.event import Event
from shared.handlers.mediator import Mediator


class CeleryMediator(Mediator):
    def __init__(self) -> None:
        self._tasks: dict[type[Event], list[Task]] = defaultdict(list)

    def subscribe(self, event_type: type[Event], task: Task) -> None:
        self._tasks[event_type].append(task)

    def publish(self, events: list[Event]) -> None:
        for event in events:
            for task in self._tasks[type(event)]:
                task.delay(event.__dict__)
