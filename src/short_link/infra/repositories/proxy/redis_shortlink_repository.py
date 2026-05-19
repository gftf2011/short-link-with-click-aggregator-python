from redis.asyncio import Redis
from pydantic import ValidationError

from short_link.domain.repositories.shortlink_repository import ShortLinkRepository
from short_link.domain.shortlink_aggregate import ShortLinkAggregate
from short_link.infra.repositories.proxy.dtos.shortlink_cache_value import (
    ShortLinkCacheValueDTO,
)


class RedisShortLinkRepositoryProxy(ShortLinkRepository):
    _CACHE_TTL_SECONDS = 3600

    def __init__(self, short_link_repository: ShortLinkRepository, redis: Redis):
        self.short_link_repository = short_link_repository
        self.redis = redis

    @staticmethod
    def _aggregate_from_cached_json(raw: str | bytes) -> ShortLinkAggregate | None:
        try:
            cached = ShortLinkCacheValueDTO.model_validate_json(raw)
        except ValidationError:
            return None
        return ShortLinkAggregate.create_from_datasource(
            id=cached.id,
            short_code=cached.short_code,
            url=cached.url,
            created_at=cached.created_at,
            expires_at=cached.expires_at,
            is_custom=cached.is_custom,
        )

    async def _cache_aggregate(self, code: str, shortlink: ShortLinkAggregate) -> None:
        shortlink_cache_value = ShortLinkCacheValueDTO(
            id=shortlink.id,
            short_code=shortlink.short_code,
            url=shortlink.url,
            created_at=shortlink.created_at,
            expires_at=shortlink.expires_at,
            is_custom=shortlink.is_custom,
        )
        await self.redis.set(
            code, shortlink_cache_value.model_dump_json(), ex=self._CACHE_TTL_SECONDS
        )

    async def get_by_code(self, code: str) -> ShortLinkAggregate | None:
        raw = await self.redis.get(code)
        if raw is not None:
            cached = self._aggregate_from_cached_json(raw)
            if cached is not None:
                return cached

        shortlink = await self.short_link_repository.get_by_code(code)
        if shortlink is None:
            return None

        await self._cache_aggregate(code, shortlink)
        return shortlink

    def create(self, short_link: ShortLinkAggregate) -> None:
        self.short_link_repository.create(short_link)
