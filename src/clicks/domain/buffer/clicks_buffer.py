from abc import ABC, abstractmethod


class ClicksBuffer(ABC):
    @abstractmethod
    def add(self, short_code: str) -> None: ...

    @abstractmethod
    async def drain(self) -> list[str]: ...
