from abc import ABC


class ConnectionManager(ABC):
    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError
