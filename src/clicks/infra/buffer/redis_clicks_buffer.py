from redis.asyncio import Redis

from clicks.domain.buffer.clicks_buffer import ClicksBuffer


class RedisClicksBuffer(ClicksBuffer):
    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client

    def add(self, short_code: str) -> None:
        self.redis_client.rpush("clicks:buffer", short_code)

    async def drain(self) -> list[str]:
        pipe = self.redis_client.pipeline()
        pipe.lrange("clicks:buffer", 0, -1)
        pipe.delete("clicks:buffer")
        results = await pipe.execute()
        return results[0]
