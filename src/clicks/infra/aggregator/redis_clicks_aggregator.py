from redis.asyncio import Redis

from clicks.domain.aggregator.clicks_aggregator import ClicksAggregator


class RedisClicksAggregator(ClicksAggregator):
    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client

    async def aggregate(self, counts: dict[str, int]) -> None:
        if not counts:
            return
        pipe = self.redis_client.pipeline()
        for short_code, count in counts.items():
            pipe.hincrby("clicks:counts", short_code, count)
        await pipe.execute()
