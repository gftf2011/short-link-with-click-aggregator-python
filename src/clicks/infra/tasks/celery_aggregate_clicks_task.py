import asyncio
import os

import redis.asyncio as aioredis
from celery import Task

from clicks.handler.aggregate_clicks.aggregate_clicks_handler import AggregateClicksHandler
from clicks.infra.aggregator.redis_clicks_aggregator import RedisClicksAggregator
from clicks.infra.buffer.redis_clicks_buffer import RedisClicksBuffer


class CeleryAggregateClicksTask(Task):
    name = "clicks.aggregate_clicks"

    def run(self) -> None:
        async def _execute() -> None:
            client = aioredis.Redis(
                host=os.environ["REDIS_FOR_CLICKS_HOST"],
                port=int(os.getenv("REDIS_FOR_CLICKS_PORT", "6381")),
                username=os.getenv("REDIS_FOR_CLICKS_USERNAME"),
                password=os.getenv("REDIS_FOR_CLICKS_PASSWORD"),
                db=2,
                decode_responses=True,
            )
            try:
                buffer = RedisClicksBuffer(redis_client=client)
                aggregator = RedisClicksAggregator(redis_client=client)
                await AggregateClicksHandler(buffer=buffer, aggregator=aggregator).handle(None)
            finally:
                await client.aclose()

        asyncio.run(_execute())
