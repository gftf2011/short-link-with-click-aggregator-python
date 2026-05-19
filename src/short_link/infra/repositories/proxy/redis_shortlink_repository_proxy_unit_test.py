from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from short_link.infra.repositories.proxy.dtos.shortlink_cache_value import (
    ShortLinkCacheValueDTO,
)
from short_link.infra.repositories.proxy.redis_shortlink_repository import (
    RedisShortLinkRepositoryProxy,
)


@pytest.mark.asyncio
async def test_given_cached_json_when_get_by_code_then_should_not_hit_db():
    now = datetime.now(timezone.utc)
    dto = ShortLinkCacheValueDTO(
        id=uuid4(),
        short_code="0010011",
        url="https://example.com",
        created_at=now,
        expires_at=now + timedelta(weeks=2),
        is_custom=False,
    )
    redis = AsyncMock()
    redis.get = AsyncMock(return_value=dto.model_dump_json())
    inner = AsyncMock()
    inner.get_by_code = AsyncMock()

    repo = RedisShortLinkRepositoryProxy(short_link_repository=inner, redis=redis)
    out = await repo.get_by_code("0010011")

    assert out is not None
    assert out.short_code == "0010011"
    assert out.url == "https://example.com"
    assert out.created_at == now
    assert out.expires_at == now + timedelta(weeks=2)
    assert out.is_custom == False
    inner.get_by_code.assert_not_called()


@pytest.mark.asyncio
async def test_given_not_cached_json_when_get_by_code_then_should_hit_db():
    now = datetime.now(timezone.utc)
    dto = ShortLinkCacheValueDTO(
        id=uuid4(),
        short_code="0010011",
        url="https://example.com",
        created_at=now,
        expires_at=now + timedelta(weeks=2),
        is_custom=False,
    )
    redis = AsyncMock()
    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock()
    inner = AsyncMock()
    inner.get_by_code = AsyncMock(return_value=dto)

    repo = RedisShortLinkRepositoryProxy(short_link_repository=inner, redis=redis)
    out = await repo.get_by_code("0010011")

    assert out is not None
    assert out.short_code == "0010011"
    assert out.url == "https://example.com"
    assert out.created_at == now
    assert out.expires_at == now + timedelta(weeks=2)
    assert out.is_custom == False
    redis.get.assert_called_once_with("0010011")
    redis.set.assert_called_once_with("0010011", dto.model_dump_json(), ex=3600)
    inner.get_by_code.assert_called_once_with("0010011")
