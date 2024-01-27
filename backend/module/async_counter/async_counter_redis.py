"""Didn't happen, not enough time during christmas to finish this
"""
import base64
from uuid import uuid4

from module.redis_init import redis_init

from .async_counter_abc import CSVAsyncCounterABC, T

COUNT = "count"
COLS = "cols:i"


class RedisAsyncCounter(CSVAsyncCounterABC[T]):
    def __init__(self):
        self.redis = redis_init()
        self.set_name = f"set:counter:{str(uuid4())}"
        self.metadata = f"metadata:{self.set_name}"

    async def count(self, key: T, count: int):
        key = (key,) if isinstance(key, str) else key
        key = b":".join(base64.b64encode(bytes(k.encode("utf-8"))) for k in key)
        await self.redis.hincrby(self.set_name, key=key, amount=count)

    async def items(self):
        cursor = 0
        while True:
            result = await self.redis.hscan(self.set_name, cursor=cursor)
            cursor, data = result
            key: str
            value: str
            if not len(data):
                break
            for key, value in data.items():
                keys = tuple(
                    base64.b64decode(k).decode("utf-8") for k in key.split(":")
                )
                count = int(value)
                yield keys, count
            if not int(cursor):
                break
