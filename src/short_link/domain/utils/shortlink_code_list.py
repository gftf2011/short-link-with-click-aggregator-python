import asyncio
from collections.abc import AsyncIterator
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import ClassVar


class ShortLinkCodeList:
    __short_link_codes: ClassVar[list[str]] = []
    _codes_lock: ClassVar[asyncio.Lock] = asyncio.Lock()

    @classmethod
    def mutation_lock(cls) -> AbstractAsyncContextManager[None]:
        @asynccontextmanager
        async def _lock() -> AsyncIterator[None]:
            async with cls._codes_lock:
                yield

        return _lock()

    @classmethod
    def add(cls, codes: list[str] | None = None) -> None:
        if codes:
            cls.__short_link_codes.extend(codes)

    @classmethod
    def pop(cls) -> str | None:
        if cls.is_empty():
            return None
        return cls.__short_link_codes.pop(0)

    @classmethod
    def is_empty(cls) -> bool:
        return len(cls.__short_link_codes) == 0

    @classmethod
    def reset(cls) -> None:
        cls.__short_link_codes = []
