import asyncio
import os

import redis
import redis.asyncio as aioredis
from celery import Task

from clicks.handler.aggregate_clicks.aggregate_clicks_handler import AggregateClicksHandler
from clicks.infra.aggregator.redis_clicks_aggregator import RedisClicksAggregator
from clicks.infra.buffer.redis_clicks_buffer import RedisClicksBuffer


class CeleryAggregateClicksTask(Task):
    name = "clicks.aggregate_clicks"

    def run(self) -> None:
        host = os.environ["REDIS_FOR_CLICKS_HOST"]
        port = int(os.getenv("REDIS_FOR_CLICKS_PORT", "6381"))
        username = os.getenv("REDIS_FOR_CLICKS_USERNAME")
        password = os.getenv("REDIS_FOR_CLICKS_PASSWORD")

        sync_client = redis.Redis(
            host=host, port=port, username=username, password=password,
            db=2, decode_responses=True,
        )

        async def _execute() -> None:
            async_client = aioredis.Redis(
                host=host, port=port, username=username, password=password,
                db=2, decode_responses=True,
            )
            try:
                buffer = RedisClicksBuffer(redis_client=sync_client)
                aggregator = RedisClicksAggregator(redis_client=async_client)
                await AggregateClicksHandler(buffer=buffer, aggregator=aggregator).handle(None)
            finally:
                await async_client.aclose()

        try:
            asyncio.run(_execute())
        finally:
            sync_client.close()
