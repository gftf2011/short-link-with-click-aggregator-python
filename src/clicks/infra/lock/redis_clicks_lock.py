import uuid

from redis.asyncio import Redis

from clicks.domain.lock.clicks_lock import ClicksLock

_LOCK_KEY = "clicks:aggregator:lock"
_LOCK_TTL_MS = 8_000

# Atomically releases the lock only if the caller still owns it.
_RELEASE_SCRIPT = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
"""


class RedisClicksLock(ClicksLock):
    def __init__(self, redis_client: Redis) -> None:
        self._redis = redis_client
        self._token: str | None = None
        self._release = redis_client.register_script(_RELEASE_SCRIPT)

    async def __aenter__(self) -> "RedisClicksLock":
        token = str(uuid.uuid4())
        acquired = await self._redis.set(_LOCK_KEY, token, nx=True, px=_LOCK_TTL_MS)
        if acquired:
            self._token = token
        return self

    async def __aexit__(self, *_: object) -> None:
        if self._token:
            await self._release(keys=[_LOCK_KEY], args=[self._token])
            self._token = None

    @property
    def acquired(self) -> bool:
        return self._token is not None
