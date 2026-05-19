from typing import Generic, TypeVar

from shared.usecases.connection_manager import ConnectionManager
from shared.usecases.usecase import UseCase

InT = TypeVar("InT")
OutT = TypeVar("OutT")


class RetrieveUnitOfWork(Generic[InT, OutT], UseCase[InT, OutT]):
    def __init__(
        self, usecase: UseCase[InT, OutT], connection_manager: ConnectionManager
    ):
        self._usecase = usecase
        self._connection_manager = connection_manager

    async def execute(self, input: InT) -> OutT:
        return await self._usecase.execute(input)
