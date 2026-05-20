import pytest
import redis as sync_redis
from testcontainers.redis import RedisContainer

from clicks.infra.buffer.redis_clicks_buffer import RedisClicksBuffer


@pytest.fixture(scope="module")
def redis_container():
    with RedisContainer("redis:7-alpine") as container:
        yield container


@pytest.fixture
def redis_client(redis_container):
    client = sync_redis.Redis(
        host=redis_container.get_container_host_ip(),
        port=redis_container.get_exposed_port(6379),
        decode_responses=True,
    )
    yield client
    client.close()


@pytest.fixture(autouse=True)
def clean_redis(redis_client):
    redis_client.flushdb()
    yield


@pytest.fixture
def buffer(redis_client):
    return RedisClicksBuffer(redis_client=redis_client)


def test_given_short_code_when_calls_add_then_should_push_to_buffer(
    buffer: RedisClicksBuffer, redis_client: sync_redis.Redis
):
    buffer.add("a1b2c3d")

    items = redis_client.lrange("clicks:buffer", 0, -1)
    assert items == ["a1b2c3d"]


def test_given_multiple_short_codes_when_calls_add_then_should_preserve_insertion_order(
    buffer: RedisClicksBuffer, redis_client: sync_redis.Redis
):
    buffer.add("a1b2c3d")
    buffer.add("b2c3d4e")
    buffer.add("c3d4e5f")

    items = redis_client.lrange("clicks:buffer", 0, -1)
    assert items == ["a1b2c3d", "b2c3d4e", "c3d4e5f"]


def test_given_duplicate_short_codes_when_calls_add_then_should_keep_all_entries(
    buffer: RedisClicksBuffer, redis_client: sync_redis.Redis
):
    buffer.add("a1b2c3d")
    buffer.add("a1b2c3d")

    items = redis_client.lrange("clicks:buffer", 0, -1)
    assert items == ["a1b2c3d", "a1b2c3d"]
