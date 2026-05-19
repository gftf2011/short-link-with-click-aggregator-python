from datetime import datetime

from redis.asyncio import Redis
from short_link.domain.gateways.shortlink_gateway import ShortLinkGateway
from short_link.domain.shortlink_aggregate import ShortLinkAggregate
from short_link.domain.utils.shortlink_code_list import ShortLinkCodeList
from shared.utils.encode_fixed_base62 import encode_int_to_fixed_base62


class RedisShortLinkGateway(ShortLinkGateway):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_counter(self) -> str | None:
        return await self.redis.get("shortlink:counter")

    async def set_counter(self, counter: str) -> None:
        await self.redis.set("shortlink:counter", counter)

    def generate(self, num: int) -> str:
        return encode_int_to_fixed_base62(num)

    async def set_shortlink_codes(self, codes: list[str]) -> None:
        await self.redis.rpush("shortlink:codes", *codes)  # type: ignore

    async def get_shortlink(
        self, url: str, expires_at: datetime
    ) -> ShortLinkAggregate | None:
        async with ShortLinkCodeList.mutation_lock():
            if ShortLinkCodeList.is_empty():
                codes: list[str] | None = await self.redis.lpop("shortlink:codes", 1000)  # type: ignore
                ShortLinkCodeList.add(codes)

            code = ShortLinkCodeList.pop()
        if code:
            return ShortLinkAggregate.create_new(
                short_code=code, url=url, expires_at=expires_at, is_custom=False
            )
        return None
