import os
import redis
import redis.asyncio as aioredis

_redis_cache: aioredis.Redis | None = None
_redis_codes: aioredis.Redis | None = None
_redis_clicks: aioredis.Redis | None = None
_redis_clicks_sync: redis.Redis | None = None


def reset_redis_clients() -> None:
    global _redis_cache, _redis_codes, _redis_clicks, _redis_clicks_sync
    _redis_cache = None
    _redis_codes = None
    _redis_clicks = None
    _redis_clicks_sync = None


def redis_client_for_shortlink_cache() -> aioredis.Redis:
    global _redis_cache
    if _redis_cache is None:
        host = os.getenv("REDIS_FOR_SHORTLINK_CACHE_HOST")
        if not host:
            raise ValueError("REDIS_FOR_SHORTLINK_CACHE_HOST is not set")
        max_conns = int(os.getenv("REDIS_FOR_SHORTLINK_CACHE_MAX_CONNECTIONS", "512"))
        _redis_cache = aioredis.Redis(
            max_connections=max_conns,
            decode_responses=True,
            db=0,
            host=host,
            port=int(os.getenv("REDIS_FOR_SHORTLINK_CACHE_PORT", "6379")),
            username=os.getenv("REDIS_FOR_SHORTLINK_CACHE_USERNAME"),
            password=os.getenv("REDIS_FOR_SHORTLINK_CACHE_PASSWORD"),
        )
    return _redis_cache


def redis_client_for_shortlink_codes() -> aioredis.Redis:
    global _redis_codes
    if _redis_codes is None:
        host = os.getenv("REDIS_FOR_SHORTLINK_CODES_HOST")
        if not host:
            raise ValueError("REDIS_FOR_SHORTLINK_CODES_HOST is not set")
        max_conns = int(os.getenv("REDIS_FOR_SHORTLINK_CODES_MAX_CONNECTIONS", "512"))
        _redis_codes = aioredis.Redis(
            max_connections=max_conns,
            decode_responses=True,
            db=0,
            host=host,
            port=int(os.getenv("REDIS_FOR_SHORTLINK_CODES_PORT", "6380")),
            username=os.getenv("REDIS_FOR_SHORTLINK_CODES_USERNAME"),
            password=os.getenv("REDIS_FOR_SHORTLINK_CODES_PASSWORD"),
        )
    return _redis_codes


def redis_client_for_clicks() -> aioredis.Redis:
    global _redis_clicks
    if _redis_clicks is None:
        host = os.getenv("REDIS_FOR_CLICKS_HOST")
        if not host:
            raise ValueError("REDIS_FOR_CLICKS_HOST is not set")
        max_conns = int(os.getenv("REDIS_FOR_CLICKS_MAX_CONNECTIONS", "512"))
        _redis_clicks = aioredis.Redis(
            max_connections=max_conns,
            decode_responses=True,
            db=2,
            host=host,
            port=int(os.getenv("REDIS_FOR_CLICKS_PORT", "6381")),
            username=os.getenv("REDIS_FOR_CLICKS_USERNAME"),
            password=os.getenv("REDIS_FOR_CLICKS_PASSWORD"),
        )
    return _redis_clicks


def sync_redis_client_for_clicks() -> redis.Redis:
    global _redis_clicks_sync
    if _redis_clicks_sync is None:
        host = os.getenv("REDIS_FOR_CLICKS_HOST")
        if not host:
            raise ValueError("REDIS_FOR_CLICKS_HOST is not set")
        max_conns = int(os.getenv("REDIS_FOR_CLICKS_MAX_CONNECTIONS", "512"))
        _redis_clicks_sync = redis.Redis(
            max_connections=max_conns,
            decode_responses=True,
            db=2,
            host=host,
            port=int(os.getenv("REDIS_FOR_CLICKS_PORT", "6381")),
            username=os.getenv("REDIS_FOR_CLICKS_USERNAME"),
            password=os.getenv("REDIS_FOR_CLICKS_PASSWORD"),
        )
    return _redis_clicks_sync
