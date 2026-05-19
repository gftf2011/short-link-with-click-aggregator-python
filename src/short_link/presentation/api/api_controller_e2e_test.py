from datetime import datetime, timedelta, timezone
import os
import subprocess
import sys
from pathlib import Path
from typing import Generator

import asyncpg
import pytest
import pytest_asyncio
import redis as redis
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from freezegun import freeze_time
from short_link.domain.utils.shortlink_code_list import ShortLinkCodeList
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

pytestmark = pytest.mark.e2e

_PROJECT_ROOT = Path(__file__).resolve().parents[4]

E2E_REDIS1_DB_PASSWORD = "e2eRedisDBAuthPass01"
E2E_REDIS2_DB_PASSWORD = "e2eRedisDBAuthPass02"

E2E_REDIS1_USER = "e2eRedisUser01"
E2E_REDIS1_USER_PASSWORD = "e2eRedisUserAuthPass01"

E2E_REDIS2_USER = "e2eRedisUser02"
E2E_REDIS2_USER_PASSWORD = "e2eRedisUserAuthPass02"

E2E_POSTGRES_USERNAME = "admin_test"
E2E_POSTGRES_PASSWORD = "admin_test"
E2E_POSTGRES_DBNAME = "shortlink_test"


async def _truncate_short_link_tables() -> None:
    database_url = os.environ["DATABASE_URL"].replace(
        "postgresql+asyncpg", "postgresql", 1
    )
    conn = await asyncpg.connect(database_url)
    try:
        await conn.execute("TRUNCATE TABLE short_link CASCADE")
    finally:
        await conn.close()


@pytest.fixture(scope="module", autouse=True)
def start_shortlink_database():
    with PostgresContainer(
        "postgres:17.9-alpine",
        username=E2E_POSTGRES_USERNAME,
        password=E2E_POSTGRES_PASSWORD,
        dbname=E2E_POSTGRES_DBNAME,
        driver="asyncpg",
    ) as container:
        yield container


@pytest.fixture(scope="module")
def start_shortlink_cache() -> (
    Generator[tuple[RedisContainer, redis.Redis], None, None]
):
    with RedisContainer(
        "redis:7-alpine", password=E2E_REDIS1_DB_PASSWORD, port=6379
    ).with_command(
        f"redis-server --requirepass {E2E_REDIS1_DB_PASSWORD} --port 6379"
    ) as cache:
        cache_host = cache.get_container_host_ip()
        cache_port = int(cache.get_exposed_port(6379))

        cache_admin = redis.Redis(
            host=cache_host,
            port=cache_port,
            password=E2E_REDIS1_DB_PASSWORD,
            decode_responses=True,
        )
        cache_admin.execute_command(
            f"ACL SETUSER {E2E_REDIS1_USER} ON >{E2E_REDIS1_USER_PASSWORD} resetchannels -@all +auth +client|setinfo +flushdb +ping +get +set ~*"
        )
        cache_admin.execute_command("ACL SETUSER default off")

        yield (cache, cache_admin)

        cache_admin.close()


@pytest.fixture(scope="module")
def start_shortlink_codes() -> (
    Generator[tuple[RedisContainer, redis.Redis], None, None]
):
    with RedisContainer(
        "redis:7-alpine", password=E2E_REDIS2_DB_PASSWORD, port=6380
    ).with_command(
        f"redis-server --requirepass {E2E_REDIS2_DB_PASSWORD} --port 6380"
    ) as codes:
        codes_host = codes.get_container_host_ip()
        codes_port = int(codes.get_exposed_port(6380))

        codes_admin = redis.Redis(
            host=codes_host,
            port=codes_port,
            password=E2E_REDIS2_DB_PASSWORD,
            decode_responses=True,
        )
        codes_admin.execute_command(
            f"ACL SETUSER {E2E_REDIS2_USER} ON >{E2E_REDIS2_USER_PASSWORD} resetchannels -@all +auth +client|setinfo +flushdb +ping +get +set +rpush +lpush +lpop ~shortlink:*"
        )

        codes_admin.execute_command("ACL SETUSER default off")

        yield (codes, codes_admin)

        codes_admin.close()


@pytest.fixture(scope="module")
def set_env(
    start_shortlink_cache: tuple[RedisContainer, redis.Redis],
    start_shortlink_codes: tuple[RedisContainer, redis.Redis],
    start_shortlink_database: PostgresContainer,
):
    from shared.infra.redis_database import reset_redis_clients

    reset_redis_clients()

    os.environ["REDIS_FOR_SHORTLINK_CACHE_HOST"] = start_shortlink_cache[
        0
    ].get_container_host_ip()
    os.environ["REDIS_FOR_SHORTLINK_CACHE_PORT"] = str(
        start_shortlink_cache[0].get_exposed_port(6379)
    )
    os.environ["REDIS_FOR_SHORTLINK_CACHE_USERNAME"] = E2E_REDIS1_USER
    os.environ["REDIS_FOR_SHORTLINK_CACHE_PASSWORD"] = E2E_REDIS1_USER_PASSWORD
    os.environ["REDIS_FOR_SHORTLINK_CODES_HOST"] = start_shortlink_codes[
        0
    ].get_container_host_ip()
    os.environ["REDIS_FOR_SHORTLINK_CODES_PORT"] = str(
        start_shortlink_codes[0].get_exposed_port(6380)
    )
    os.environ["REDIS_FOR_SHORTLINK_CODES_USERNAME"] = E2E_REDIS2_USER
    os.environ["REDIS_FOR_SHORTLINK_CODES_PASSWORD"] = E2E_REDIS2_USER_PASSWORD
    os.environ["DATABASE_URL"] = start_shortlink_database.get_connection_url()
    yield start_shortlink_database


@pytest.fixture(scope="module", autouse=True)
def run_shortlink_database_migrations(set_env):
    alembic_cfg = Config(str(_PROJECT_ROOT / "alembic.ini"))
    command.upgrade(alembic_cfg, "head")
    subprocess.run(
        [
            sys.executable,
            str(_PROJECT_ROOT / "scripts" / "create_short_link_partitions.py"),
            "--ahead",
            "2",
        ],
        check=True,
        env=os.environ,
    )


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_shortlink_postgresql(set_env, run_shortlink_database_migrations):
    await _truncate_short_link_tables()


@pytest.fixture(scope="function", autouse=True)
def clean_shortlink_cache(set_env):
    cache_admin = redis.Redis(
        host=os.environ["REDIS_FOR_SHORTLINK_CACHE_HOST"],
        port=int(os.environ["REDIS_FOR_SHORTLINK_CACHE_PORT"]),
        username=E2E_REDIS1_USER,
        password=E2E_REDIS1_USER_PASSWORD,
        decode_responses=True,
    )
    try:
        cache_admin.flushdb()
    finally:
        cache_admin.close()


@pytest.fixture(scope="function", autouse=True)
def clean_shortlink_codes(set_env):
    codes_admin = redis.Redis(
        host=os.environ["REDIS_FOR_SHORTLINK_CODES_HOST"],
        port=int(os.environ["REDIS_FOR_SHORTLINK_CODES_PORT"]),
        username=E2E_REDIS2_USER,
        password=E2E_REDIS2_USER_PASSWORD,
        decode_responses=True,
    )
    try:
        codes_admin.flushdb()
        codes_admin.lpush("shortlink:codes", "0010010")
    finally:
        codes_admin.close()
    ShortLinkCodeList.reset()


@pytest.fixture(scope="module")
def shortlink_http_client(set_env, run_shortlink_database_migrations):
    from main.server.app.application import application

    app = application()
    with TestClient(app) as client:
        yield client


def test_given_valid_url_when_calls_create_then_should_return_201(
    shortlink_http_client: TestClient,
):
    response = shortlink_http_client.post(
        "/v1/shortlink", json={"url": "https://www.google.com"}
    )
    assert response.status_code == 201
    assert response.json() == {"status": 201, "data": {"code": "0010010"}}


def test_given_valid_url_and_expires_at_when_calls_create_then_should_return_201(
    shortlink_http_client: TestClient,
):
    response = shortlink_http_client.post(
        "/v1/shortlink",
        json={
            "url": "https://www.google.com",
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        },
    )
    assert response.status_code == 201
    assert response.json() == {"status": 201, "data": {"code": "0010010"}}


def test_given_valid_url_and_alias_when_calls_create_then_should_return_201(
    shortlink_http_client: TestClient,
):
    response = shortlink_http_client.post(
        "/v1/shortlink",
        json={
            "url": "https://www.google.com",
            "alias": "my-brand",
        },
    )
    assert response.status_code == 201
    assert response.json() == {"status": 201, "data": {"code": "my-brand"}}


def test_given_invalid_url_when_calls_create_then_should_return_400(
    shortlink_http_client: TestClient,
):
    response = shortlink_http_client.post("/v1/shortlink", json={"url": "invalid-url"})
    assert response.status_code == 400
    assert response.json() == {
        "status": 400,
        "data": {"error": "url is not a valid URL"},
    }


def test_given_existing_code_when_calls_redirect_then_should_return_http_redirect(
    shortlink_http_client: TestClient,
):
    shortlink_http_client.post("/v1/shortlink", json={"url": "https://www.google.com"})
    response = shortlink_http_client.get(
        "/v1/shortlink/0010010", follow_redirects=False
    )
    assert response.status_code == 302
    assert response.headers["location"] == "https://www.google.com"
    assert response.text == ""


def test_given_code_which_does_not_exists_when_calls_redirect_then_should_return_404(
    shortlink_http_client: TestClient,
):
    response = shortlink_http_client.get("/v1/shortlink/a1b2c3d")
    assert response.status_code == 404
    assert response.json() == {
        "status": 404,
        "data": {"error": "Short link not found for code: a1b2c3d"},
    }


def test_given_code_which_expires_at_is_in_the_past_when_calls_redirect_then_should_return_400(
    shortlink_http_client: TestClient,
):
    now = datetime.now(timezone.utc)
    with freeze_time(now) as frozen_time:
        get_response = shortlink_http_client.post(
            "/v1/shortlink",
            json={
                "url": "https://www.google.com",
                "expires_at": (now + timedelta(seconds=4)).isoformat(),
            },
        )
        assert get_response.status_code == 201
        code = get_response.json()["data"]["code"]

        frozen_time.tick(delta=timedelta(seconds=5))
        response = shortlink_http_client.get(f"/v1/shortlink/{code}")

    assert response.status_code == 400
    assert response.json() == {
        "status": 400,
        "data": {"error": "expires_at cannot be in the past"},
    }
