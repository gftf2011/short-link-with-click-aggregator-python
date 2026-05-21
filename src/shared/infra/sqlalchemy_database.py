import os
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

engine: AsyncEngine | None = None
AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None


def _build_engine() -> AsyncEngine:
    url = os.getenv("DATABASE_URL")
    if url is None:
        raise ValueError("DATABASE_URL is not set")
    return create_async_engine(
        url,
        echo=False,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
    )


def _build_session_factory(eng: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker[AsyncSession](
        bind=eng, autoflush=False, expire_on_commit=False, class_=AsyncSession
    )


def reset_engine() -> None:
    global engine, AsyncSessionLocal
    engine = _build_engine()
    AsyncSessionLocal = _build_session_factory(engine)


if os.getenv("DATABASE_URL") is not None:
    reset_engine()
