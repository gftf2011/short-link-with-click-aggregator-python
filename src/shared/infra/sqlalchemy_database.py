import os
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set")

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker[AsyncSession](
    bind=engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
)
