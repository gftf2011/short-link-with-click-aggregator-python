import redis

from clicks.domain.buffer.clicks_buffer import ClicksBuffer


class RedisClicksBuffer(ClicksBuffer):
    def __init__(self, redis_client: redis.Redis) -> None:
        self.redis_client = redis_client

    def add(self, short_code: str, click_impression_id: str) -> None:
        added = self.redis_client.hsetnx("clicks:impressions", click_impression_id, "1")
        if added:
            self.redis_client.rpush("clicks:buffer", short_code)

    def drain(self) -> list[str]:
        pipe = self.redis_client.pipeline()
        pipe.lrange("clicks:buffer", 0, -1)
        pipe.delete("clicks:buffer")
        pipe.delete("clicks:impressions")
        results = pipe.execute()
        return results[0]
