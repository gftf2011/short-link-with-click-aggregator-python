from abc import ABC, abstractmethod
from typing import Any

from shared.domain.event import Event


class Mediator(ABC):
    @abstractmethod
    def subscribe(self, event_type: type[Event], task: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def publish(self, events: list[Event]) -> None:
        raise NotImplementedError
