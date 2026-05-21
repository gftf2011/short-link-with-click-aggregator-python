import os
from pathlib import Path
from typing import Generator

import asyncpg
import pytest
import pytest_asyncio
import redis as redis
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

pytestmark = pytest.mark.e2e

_PROJECT_ROOT = Path(__file__).resolve().parents[4]

E2E_REDIS1_DB_PASSWORD = "e2eClicksRedisDBAuthPass01"
E2E_REDIS2_DB_PASSWORD = "e2eClicksRedisDBAuthPass02"
E2E_REDIS3_DB_PASSWORD = "e2eClicksRedisDBAuthPass03"

E2E_REDIS1_USER = "e2eClicksRedisUser01"
E2E_REDIS1_USER_PASSWORD = "e2eClicksRedisUserAuthPass01"

E2E_REDIS2_USER = "e2eClicksRedisUser02"
E2E_REDIS2_USER_PASSWORD = "e2eClicksRedisUserAuthPass02"

E2E_REDIS3_USER = "e2eClicksRedisUser03"
E2E_REDIS3_USER_PASSWORD = "e2eClicksRedisUserAuthPass03"

E2E_POSTGRES_USERNAME = "admin_clicks_test"
E2E_POSTGRES_PASSWORD = "admin_clicks_test"
E2E_POSTGRES_DBNAME = "clicks_test"


async def _truncate_click_table() -> None:
    database_url = os.environ["DATABASE_URL"].replace("postgresql+asyncpg", "postgresql", 1)
    conn = await asyncpg.connect(database_url)
    try:
        await conn.execute("TRUNCATE TABLE click")
    finally:
        await conn.close()


async def _seed_clicks(short_code: str, count: int) -> None:
    database_url = os.environ["DATABASE_URL"].replace("postgresql+asyncpg", "postgresql", 1)
    conn = await asyncpg.connect(database_url)
    try:
        await conn.execute(
            "INSERT INTO click (short_code, count) VALUES ($1, $2) "
            "ON CONFLICT (short_code) DO UPDATE SET count = EXCLUDED.count",
            short_code,
            count,
        )
    finally:
        await conn.close()


@pytest.fixture(scope="module", autouse=True)
def start_clicks_database():
    with PostgresContainer(
        "postgres:17.9-alpine",
        username=E2E_POSTGRES_USERNAME,
        password=E2E_POSTGRES_PASSWORD,
        dbname=E2E_POSTGRES_DBNAME,
        driver="asyncpg",
    ) as container:
        yield container


@pytest.fixture(scope="module")
def start_shortlink_cache() -> Generator[tuple[RedisContainer, redis.Redis], None, None]:
    with RedisContainer(
        "redis:7-alpine", password=E2E_REDIS1_DB_PASSWORD, port=6379
    ).with_command(
        f"redis-server --requirepass {E2E_REDIS1_DB_PASSWORD} --port 6379"
    ) as cache:
        cache_host = cache.get_container_host_ip()
        cache_port = int(cache.get_exposed_port(6379))
        cache_admin = redis.Redis(
            host=cache_host, port=cache_port,
            password=E2E_REDIS1_DB_PASSWORD, decode_responses=True,
        )
        cache_admin.execute_command(
            f"ACL SETUSER {E2E_REDIS1_USER} ON >{E2E_REDIS1_USER_PASSWORD} "
            "resetchannels -@all +auth +client|setinfo +flushdb +ping +get +set ~*"
        )
        cache_admin.execute_command("ACL SETUSER default off")
        yield (cache, cache_admin)
        cache_admin.close()


@pytest.fixture(scope="module")
def start_shortlink_codes() -> Generator[tuple[RedisContainer, redis.Redis], None, None]:
    with RedisContainer(
        "redis:7-alpine", password=E2E_REDIS2_DB_PASSWORD, port=6380
    ).with_command(
        f"redis-server --requirepass {E2E_REDIS2_DB_PASSWORD} --port 6380"
    ) as codes:
        codes_host = codes.get_container_host_ip()
        codes_port = int(codes.get_exposed_port(6380))
        codes_admin = redis.Redis(
            host=codes_host, port=codes_port,
            password=E2E_REDIS2_DB_PASSWORD, decode_responses=True,
        )
        codes_admin.execute_command(
            f"ACL SETUSER {E2E_REDIS2_USER} ON >{E2E_REDIS2_USER_PASSWORD} "
            "resetchannels -@all +auth +client|setinfo +flushdb +ping +get +set +rpush +lpush +lpop ~shortlink:*"
        )
        codes_admin.execute_command("ACL SETUSER default off")
        yield (codes, codes_admin)
        codes_admin.close()


@pytest.fixture(scope="module")
def start_shortlink_clicks() -> Generator[tuple[RedisContainer, redis.Redis], None, None]:
    with RedisContainer(
        "redis:7-alpine", password=E2E_REDIS3_DB_PASSWORD, port=6381
    ).with_command(
        f"redis-server --requirepass {E2E_REDIS3_DB_PASSWORD} --port 6381"
    ) as clicks:
        clicks_host = clicks.get_container_host_ip()
        clicks_port = int(clicks.get_exposed_port(6381))
        clicks_admin = redis.Redis(
            host=clicks_host, port=clicks_port,
            password=E2E_REDIS3_DB_PASSWORD, decode_responses=True,
        )
        clicks_admin.execute_command(
            f"ACL SETUSER {E2E_REDIS3_USER} ON >{E2E_REDIS3_USER_PASSWORD} +@all ~* &*"
        )
        clicks_admin.execute_command("ACL SETUSER default off")
        yield (clicks, clicks_admin)
        clicks_admin.close()


@pytest.fixture(scope="module")
def set_env(
    start_shortlink_cache: tuple[RedisContainer, redis.Redis],
    start_shortlink_codes: tuple[RedisContainer, redis.Redis],
    start_shortlink_clicks: tuple[RedisContainer, redis.Redis],
    start_clicks_database: PostgresContainer,
):
    from clicks.main.factory.clicks import api_mediator
    from shared.infra.redis_database import reset_redis_clients
    from shared.infra.sqlalchemy_database import reset_engine

    reset_redis_clients()
    api_mediator.cache_clear()

    os.environ["REDIS_FOR_SHORTLINK_CACHE_HOST"] = start_shortlink_cache[0].get_container_host_ip()
    os.environ["REDIS_FOR_SHORTLINK_CACHE_PORT"] = str(start_shortlink_cache[0].get_exposed_port(6379))
    os.environ["REDIS_FOR_SHORTLINK_CACHE_USERNAME"] = E2E_REDIS1_USER
    os.environ["REDIS_FOR_SHORTLINK_CACHE_PASSWORD"] = E2E_REDIS1_USER_PASSWORD
    os.environ["REDIS_FOR_SHORTLINK_CODES_HOST"] = start_shortlink_codes[0].get_container_host_ip()
    os.environ["REDIS_FOR_SHORTLINK_CODES_PORT"] = str(start_shortlink_codes[0].get_exposed_port(6380))
    os.environ["REDIS_FOR_SHORTLINK_CODES_USERNAME"] = E2E_REDIS2_USER
    os.environ["REDIS_FOR_SHORTLINK_CODES_PASSWORD"] = E2E_REDIS2_USER_PASSWORD
    os.environ["REDIS_FOR_CLICKS_HOST"] = start_shortlink_clicks[0].get_container_host_ip()
    os.environ["REDIS_FOR_CLICKS_PORT"] = str(start_shortlink_clicks[0].get_exposed_port(6381))
    os.environ["REDIS_FOR_CLICKS_USERNAME"] = E2E_REDIS3_USER
    os.environ["REDIS_FOR_CLICKS_PASSWORD"] = E2E_REDIS3_USER_PASSWORD
    os.environ["DATABASE_URL"] = start_clicks_database.get_connection_url()

    reset_engine()

    yield start_clicks_database


@pytest.fixture(scope="module", autouse=True)
def run_clicks_database_migrations(set_env):
    alembic_cfg = Config(str(_PROJECT_ROOT / "alembic.ini"))
    command.upgrade(alembic_cfg, "head")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_click_table(set_env, run_clicks_database_migrations):
    await _truncate_click_table()


@pytest.fixture(scope="module")
def clicks_http_client(set_env, run_clicks_database_migrations):
    from main.server.app.application import application

    app = application()
    with TestClient(app) as client:
        yield client


def test_given_short_code_with_no_clicks_when_calls_get_clicks_count_then_should_return_0(
    clicks_http_client: TestClient,
):
    response = clicks_http_client.get("/v1/clicks/a1b2c3d")

    assert response.status_code == 200
    assert response.json() == {"status": 200, "data": {"short_code": "a1b2c3d", "count": 0}}


@pytest.mark.asyncio
async def test_given_short_code_with_clicks_when_calls_get_clicks_count_then_should_return_count(
    clicks_http_client: TestClient,
):
    await _seed_clicks("a1b2c3d", 42)

    response = clicks_http_client.get("/v1/clicks/a1b2c3d")

    assert response.status_code == 200
    assert response.json() == {"status": 200, "data": {"short_code": "a1b2c3d", "count": 42}}


@pytest.mark.asyncio
async def test_given_multiple_short_codes_when_calls_get_clicks_count_then_should_return_each_count(
    clicks_http_client: TestClient,
):
    await _seed_clicks("a1b2c3d", 10)
    await _seed_clicks("x9y8z7w", 250)

    response_a = clicks_http_client.get("/v1/clicks/a1b2c3d")
    response_b = clicks_http_client.get("/v1/clicks/x9y8z7w")

    assert response_a.status_code == 200
    assert response_a.json() == {"status": 200, "data": {"short_code": "a1b2c3d", "count": 10}}

    assert response_b.status_code == 200
    assert response_b.json() == {"status": 200, "data": {"short_code": "x9y8z7w", "count": 250}}
