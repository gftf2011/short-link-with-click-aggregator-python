from abc import ABC, abstractmethod


class ClicksRepository(ABC):
    @abstractmethod
    async def get_clicks_by_short_code(self, short_code: str) -> int: ...

    @abstractmethod
    async def increment_clicks(self, counts: dict[str, int]) -> None: ...
