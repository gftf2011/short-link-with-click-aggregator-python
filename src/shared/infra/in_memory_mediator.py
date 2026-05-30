import asyncio
from collections import defaultdict
from typing import Any

from shared.domain.event import Event
from shared.handlers.mediator import Mediator
from shared.handlers.handler import Handler


class InMemoryMediator(Mediator):
    def __init__(self) -> None:
        self._handlers: dict[type[Event], list[Handler[Any, Any]]] = defaultdict(list)

    def subscribe(self, event_type: type[Event], task: Handler[Any, Any]) -> None:
        self._handlers[event_type].append(task)

    async def publish(self, events: list[Event]) -> None:
        for event in events:
            for handler in self._handlers[type(event)]:
                asyncio.create_task(handler.handle(event))
