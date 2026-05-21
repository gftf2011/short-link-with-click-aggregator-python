import asyncio
import os

import redis.asyncio as aioredis
from celery import Task
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from clicks.handler.flush_clicks.flush_clicks_handler import FlushClicksHandler
from clicks.infra.gateways.redis_clicks_gateway import RedisClicksGateway
from clicks.infra.lock.redis_clicks_lock import RedisClicksLock
from clicks.infra.repositories.sqlalchemy_clicks_repository import SqlAlchemyClicksRepository


class CeleryFlushClicksTask(Task):
    name = "clicks.flush_clicks"

    def run(self) -> None:
        async def _execute() -> None:
            redis_client = aioredis.Redis(
                host=os.environ["REDIS_FOR_CLICKS_HOST"],
                port=int(os.getenv("REDIS_FOR_CLICKS_PORT", "6381")),
                username=os.getenv("REDIS_FOR_CLICKS_USERNAME"),
                password=os.getenv("REDIS_FOR_CLICKS_PASSWORD"),
                db=2,
                decode_responses=True,
            )
            engine = create_async_engine(os.environ["DATABASE_URL"])
            session = async_sessionmaker(
                bind=engine, autoflush=False, expire_on_commit=False
            )()
            try:
                gateway = RedisClicksGateway(redis=redis_client)
                lock = RedisClicksLock(redis_client=redis_client)
                repository = SqlAlchemyClicksRepository(session=session)
                await FlushClicksHandler(
                    gateway=gateway, repository=repository, lock=lock
                ).handle(None)
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
                await engine.dispose()
                await redis_client.aclose()

        asyncio.run(_execute())
