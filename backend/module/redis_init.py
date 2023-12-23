from contextvars import ContextVar

from redis import asyncio as aioredis

redis_ctx = ContextVar[aioredis.Redis | None]("redis")


def redis_init() -> aioredis.Redis:
    try:
        redis = redis_ctx.get()
    except LookupError:
        # No concurrency issue, because this is already only shared for each task environment
        redis = aioredis.Redis(host="db", decode_responses=True)
        redis_ctx.set(redis)
    return redis
