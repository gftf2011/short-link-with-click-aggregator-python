from abc import ABC, abstractmethod


class ClicksRepository(ABC):
    @abstractmethod
    async def increment_clicks(self, counts: dict[str, int]) -> None: ...
