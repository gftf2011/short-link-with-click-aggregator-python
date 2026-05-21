from abc import ABC, abstractmethod


class ClicksLock(ABC):
    @abstractmethod
    async def __aenter__(self) -> "ClicksLock": ...

    @abstractmethod
    async def __aexit__(self, *_: object) -> None: ...

    @property
    @abstractmethod
    def acquired(self) -> bool: ...
