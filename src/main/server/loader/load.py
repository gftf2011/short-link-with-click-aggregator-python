from typing import Awaitable, cast

from sqlalchemy import text

import shared.infra.sqlalchemy_database as _db
from shared.infra.redis_database import (
    redis_client_for_shortlink_cache,
    redis_client_for_shortlink_codes,
    sync_redis_client_for_clicks,
)


async def load() -> None:
    if _db.engine is not None:
        async with _db.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

    await cast(Awaitable[bool], redis_client_for_shortlink_cache().ping())
    await cast(Awaitable[bool], redis_client_for_shortlink_codes().ping())
    sync_redis_client_for_clicks().ping()
