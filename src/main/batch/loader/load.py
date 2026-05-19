from typing import Awaitable, cast

from shared.infra.redis_database import redis_client_for_shortlink_codes


async def load() -> None:
    await cast(Awaitable[bool], redis_client_for_shortlink_codes().ping())
