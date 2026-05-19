from typing import Awaitable, cast

from sqlalchemy import text

from shared.infra.redis_database import (
    redis_client_for_shortlink_cache,
    redis_client_for_shortlink_codes,
)
from shared.infra.sqlalchemy_database import engine


async def load() -> None:
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    await cast(Awaitable[bool], redis_client_for_shortlink_cache().ping())
    await cast(Awaitable[bool], redis_client_for_shortlink_codes().ping())
