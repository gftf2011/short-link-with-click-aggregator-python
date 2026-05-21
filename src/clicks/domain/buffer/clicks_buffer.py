from abc import ABC, abstractmethod


class ClicksBuffer(ABC):
    @abstractmethod
    def add(self, short_code: str) -> None: ...

    @abstractmethod
    def drain(self) -> list[str]: ...
