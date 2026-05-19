import asyncio

from main.batch.loader.load import load
from main.batch.runner.run import run
from main.server.bootstrap.boot import boot
from shared.infra.redis_database import redis_client_for_shortlink_codes


async def main() -> None:
    boot()
    await load()
    await run()
    await redis_client_for_shortlink_codes().aclose()


def run_batch() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run_batch()
