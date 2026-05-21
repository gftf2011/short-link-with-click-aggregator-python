from redis.asyncio import Redis

from clicks.domain.gateways.clicks_gateway import ClicksGateway


class RedisClicksGateway(ClicksGateway):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def get_clicks_count(self) -> dict[str, int]:
        raw: dict[str, str] = await self.redis.hgetall("clicks:counts")  # type: ignore
        return {short_code: int(count) for short_code, count in raw.items()}

    async def reset_clicks_count(self) -> None:
        await self.redis.delete("clicks:counts")
