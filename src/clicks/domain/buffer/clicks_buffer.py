from abc import ABC, abstractmethod


class ClicksBuffer(ABC):
    @abstractmethod
    def add(self, short_code: str, click_impression_id: str) -> None: ...

    @abstractmethod
    def drain(self) -> list[str]: ...
