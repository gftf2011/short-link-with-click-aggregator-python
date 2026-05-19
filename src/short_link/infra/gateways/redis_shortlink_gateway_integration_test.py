import pytest
import pytest_asyncio
import redis.asyncio as redis
from datetime import datetime, timedelta, timezone
from testcontainers.redis import RedisContainer
from short_link.infra.gateways.redis_shortlink_gateway import RedisShortLinkGateway


@pytest.fixture(scope="module")
def redis_container():
    with RedisContainer("redis:7-alpine") as container:
        yield container


@pytest_asyncio.fixture
async def redis_client(redis_container):
    client = redis.Redis(
        host=redis_container.get_container_host_ip(),
        port=redis_container.get_exposed_port(6379),
        decode_responses=True,
    )
    yield client
    await client.aclose()


@pytest_asyncio.fixture(autouse=True)
async def clean_redis(redis_client):
    await redis_client.flushdb()
    yield


@pytest_asyncio.fixture
async def redis_shortlink_gateway(redis_client):
    return RedisShortLinkGateway(redis=redis_client)


@pytest.mark.asyncio
async def test_given_no_input_when_calls_get_code_by_the_first_time_then_should_return_None(
    redis_shortlink_gateway: RedisShortLinkGateway,
):
    counter = await redis_shortlink_gateway.get_counter()
    assert counter is None


@pytest.mark.asyncio
async def test_given_set_counter_is_called_when_calls_get_code_by_the_first_time_then_should_return_something(
    redis_shortlink_gateway: RedisShortLinkGateway,
):
    await redis_shortlink_gateway.set_counter("0000000")
    counter = await redis_shortlink_gateway.get_counter()
    assert counter == "0000000"


@pytest.mark.asyncio
async def test_given_valid_input_when_calls_get_shortlink_by_the_first_time_then_should_return_None(
    redis_shortlink_gateway: RedisShortLinkGateway,
):
    shortlink = await redis_shortlink_gateway.get_shortlink(
        url="https://example.com",
        expires_at=datetime.now(timezone.utc) + timedelta(weeks=2),
    )
    assert shortlink is None


@pytest.mark.asyncio
async def test_given_set_shortlink_codes_is_called_when_calls_get_shortlink_then_should_return_something(
    redis_shortlink_gateway: RedisShortLinkGateway,
):
    await redis_shortlink_gateway.set_shortlink_codes(
        codes=["a1b2c3d", "a1b2c3e", "a1b2c3f"]
    )
    shortlink1 = await redis_shortlink_gateway.get_shortlink(
        url="https://example.com",
        expires_at=datetime.now(timezone.utc) + timedelta(weeks=2),
    )
    shortlink2 = await redis_shortlink_gateway.get_shortlink(
        url="https://example.com",
        expires_at=datetime.now(timezone.utc) + timedelta(weeks=2),
    )
    shortlink3 = await redis_shortlink_gateway.get_shortlink(
        url="https://example.com",
        expires_at=datetime.now(timezone.utc) + timedelta(weeks=2),
    )

    assert shortlink1 is not None
    assert shortlink1.short_code == "a1b2c3d"
    assert shortlink1.url == "https://example.com"
    assert shortlink1.expires_at is not None
    assert shortlink2 is not None
    assert shortlink2.short_code == "a1b2c3e"
    assert shortlink2.url == "https://example.com"
    assert shortlink2.expires_at is not None
    assert shortlink3 is not None
    assert shortlink3.short_code == "a1b2c3f"
    assert shortlink3.url == "https://example.com"
    assert shortlink3.expires_at is not None
