from abc import ABC, abstractmethod


class ClicksAggregator(ABC):
    @abstractmethod
    async def aggregate(self, counts: dict[str, int]) -> None: ...
