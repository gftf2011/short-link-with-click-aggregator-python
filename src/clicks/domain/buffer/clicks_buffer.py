from abc import ABC


class ClicksBuffer(ABC):
    def add(self, short_code: str) -> None:
        raise NotImplementedError
