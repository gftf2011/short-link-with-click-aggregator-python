import os
from typing import Generator
import pytest
import redis as redis

from testcontainers.redis import RedisContainer
from short_link.domain.utils.shortlink_code_list import ShortLinkCodeList

E2E_REDIS_DB_PASSWORD = "e2eRedisDBAuthPass02"
E2E_REDIS_USER = "e2eRedisUser02"
E2E_REDIS_USER_PASSWORD = "e2eRedisUserAuthPass02"


@pytest.fixture(scope="module")
def start_shortlink_codes() -> (
    Generator[tuple[RedisContainer, redis.Redis], None, None]
):
    with RedisContainer(
        "redis:7-alpine", password=E2E_REDIS_DB_PASSWORD, port=6380
    ).with_command(
        f"redis-server --requirepass {E2E_REDIS_DB_PASSWORD} --port 6380"
    ) as codes:
        codes_host = codes.get_container_host_ip()
        codes_port = int(codes.get_exposed_port(6380))

        codes_admin = redis.Redis(
            host=codes_host,
            port=codes_port,
            password=E2E_REDIS_DB_PASSWORD,
            decode_responses=True,
        )
        codes_admin.execute_command(
            f"ACL SETUSER {E2E_REDIS_USER} ON >{E2E_REDIS_USER_PASSWORD} resetchannels -@all +auth +client|setinfo +flushdb +ping +get +set +rpush +lpop ~shortlink:*"
        )

        codes_admin.execute_command("ACL SETUSER default off")

        yield (codes, codes_admin)

        codes_admin.close()


@pytest.fixture(scope="module")
def set_env(
    start_shortlink_codes: tuple[RedisContainer, redis.Redis],
) -> Generator[tuple[RedisContainer, redis.Redis], None, None]:
    from shared.infra.redis_database import reset_redis_clients

    reset_redis_clients()

    os.environ["REDIS_FOR_SHORTLINK_CODES_HOST"] = start_shortlink_codes[
        0
    ].get_container_host_ip()
    os.environ["REDIS_FOR_SHORTLINK_CODES_PORT"] = str(
        start_shortlink_codes[0].get_exposed_port(6380)
    )
    os.environ["REDIS_FOR_SHORTLINK_CODES_USERNAME"] = E2E_REDIS_USER
    os.environ["REDIS_FOR_SHORTLINK_CODES_PASSWORD"] = E2E_REDIS_USER_PASSWORD
    yield start_shortlink_codes


@pytest.fixture(scope="module")
def redis_codes(
    set_env: tuple[RedisContainer, redis.Redis],
) -> tuple[RedisContainer, redis.Redis]:
    os.environ["MAX_SHORTLINK_CODES"] = "15000001"
    os.environ["SHORTLINK_CODES_BATCH_SIZE"] = "4000"
    return set_env


@pytest.fixture(autouse=True)
def clean_redis_codes_each_test(redis_codes: tuple[RedisContainer, redis.Redis]):
    client = redis_codes[1]
    client.flushdb()
    client.lpush("shortlink:codes", "0010010")
    ShortLinkCodeList.reset()


@pytest.mark.asyncio
async def test_given_no_input_when_calls_run_then_should_process_all_shortlink_codes(
    redis_codes: tuple[RedisContainer, redis.Redis],
):
    from short_link.main.factory.shortlink import batch

    controller = batch()
    await controller.run()
    counter = redis_codes[1].get("shortlink:counter")
    first_code = redis_codes[1].lindex("shortlink:codes", 0)
    last_code = redis_codes[1].lindex("shortlink:codes", -1)
    assert counter == "0010Wbu"
    assert first_code == "0010010"
    assert last_code == "0010Wbu"
