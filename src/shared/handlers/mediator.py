from collections import defaultdict
from typing import Any

from shared.domain.event import Event
from shared.handlers.handler import Handler


class Mediator:
    def __init__(self) -> None:
        self._handlers: dict[type[Event], list[Handler[Event, None]]] = defaultdict(list)

    def subscribe(self, event_type: type[Event], handler: Handler[Event, None]) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, events: list[Event]) -> None:
        for event in events:
            for handler in self._handlers[type(event)]:
                await handler.handle(event)
