from dataclasses import asdict
from pathlib import Path

from ..redis_init import redis_init
from .task_manager_abc import TaskParams


class RedisImplementation:
    def __init__(self) -> None:
        self.redis = redis_init()

    def key(self, task_id: str):
        return f"task:{task_id}"

    async def mark_done(self, task_id: str) -> None:
        await self.redis.hset(self.key(task_id), "status", "done")

    async def mark_error(self, task_id: str) -> None:
        await self.redis.hset(self.key(task_id), "status", "error")

    async def create_task(self, task_id: str) -> TaskParams:
        fname = Path(task_id).with_suffix(".csv")
        task = TaskParams(task_id, str(fname))
        await self.redis.hmset(name=self.key(task_id), mapping=asdict(task))
        return task

    async def find_task(self, task_id: str) -> TaskParams | None:
        task = await self.redis.hgetall(self.key(task_id))
        if len(task) == 0:
            return None
        return TaskParams(**task)
