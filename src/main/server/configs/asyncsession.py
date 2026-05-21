from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

import shared.infra.sqlalchemy_database as _db


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    session = _db.AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
