from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from shared.infra.sqlalchemy_database import AsyncSessionLocal


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
