from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


class Handler(ABC, Generic[Input, Output]):
    @abstractmethod
    async def handle(self, input: Input) -> Output:
        raise NotImplementedError
