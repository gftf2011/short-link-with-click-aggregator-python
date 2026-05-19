import os
import redis.asyncio as redis

_redis_cache: redis.Redis | None = None
_redis_codes: redis.Redis | None = None


def reset_redis_clients() -> None:
    """Drop cached clients so the next access rebuilds from current env (tests / multi-app)."""
    global _redis_cache, _redis_codes
    _redis_cache = None
    _redis_codes = None


def redis_client_for_shortlink_cache() -> redis.Redis:
    global _redis_cache
    if _redis_cache is None:
        host = os.getenv("REDIS_FOR_SHORTLINK_CACHE_HOST")
        if not host:
            raise ValueError("REDIS_FOR_SHORTLINK_CACHE_HOST is not set")
        max_conns = int(os.getenv("REDIS_FOR_SHORTLINK_CACHE_MAX_CONNECTIONS", "512"))
        _redis_cache = redis.Redis(
            max_connections=max_conns,
            decode_responses=True,
            db=0,
            host=host,
            port=int(os.getenv("REDIS_FOR_SHORTLINK_CACHE_PORT", "6379")),
            username=os.getenv("REDIS_FOR_SHORTLINK_CACHE_USERNAME"),
            password=os.getenv("REDIS_FOR_SHORTLINK_CACHE_PASSWORD"),
        )
    return _redis_cache


def redis_client_for_shortlink_codes() -> redis.Redis:
    global _redis_codes
    if _redis_codes is None:
        host = os.getenv("REDIS_FOR_SHORTLINK_CODES_HOST")
        if not host:
            raise ValueError("REDIS_FOR_SHORTLINK_CODES_HOST is not set")
        max_conns = int(os.getenv("REDIS_FOR_SHORTLINK_CODES_MAX_CONNECTIONS", "512"))
        _redis_codes = redis.Redis(
            max_connections=max_conns,
            decode_responses=True,
            db=0,
            host=host,
            port=int(os.getenv("REDIS_FOR_SHORTLINK_CODES_PORT", "6380")),
            username=os.getenv("REDIS_FOR_SHORTLINK_CODES_USERNAME"),
            password=os.getenv("REDIS_FOR_SHORTLINK_CODES_PASSWORD"),
        )
    return _redis_codes
