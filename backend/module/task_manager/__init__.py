from contextlib import asynccontextmanager
from logging import getLogger

from .task_manager_abc import TaskParams
from .task_manager_redis import RedisImplementation as _RedisImplementation

logger = getLogger(__file__)


impl = _RedisImplementation()


class AsyncTaskManager:
    @staticmethod
    async def find_task(task_id):
        return await impl.find_task(task_id)

    @asynccontextmanager
    @staticmethod
    async def manage_processing(task_id: str):
        done = False
        try:
            task = await impl.create_task(task_id)
            yield task
            done = True
        except (ValueError, KeyError, IOError):
            await impl.mark_error(task_id)
            logger.info("Processing error, %s", task_id, exc_info=True)
        except RuntimeError:
            logger.exception("Unknown task exception, %s", task_id)
            raise
        finally:
            if done:
                await impl.mark_done(task_id)
            else:
                await impl.mark_error(task_id)
