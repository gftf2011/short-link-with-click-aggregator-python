from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from main.server.routes import healthcheck, shortlink
from main.server.loader.load import load

from shared.infra.redis_database import (
    redis_client_for_shortlink_cache,
    redis_client_for_shortlink_codes,
)
from shared.infra.sqlalchemy_database import engine


def application() -> FastAPI:

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        await load()

        yield

        await engine.dispose()
        await redis_client_for_shortlink_cache().aclose()
        await redis_client_for_shortlink_codes().aclose()

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=[os.getenv("ALLOWED_ORIGINS", "*")],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(healthcheck.router)
    app.include_router(shortlink.router)

    return app
