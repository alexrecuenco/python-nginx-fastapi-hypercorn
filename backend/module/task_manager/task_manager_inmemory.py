from pathlib import Path

from .task_manager_abc import TaskManager, TaskParams

# Some fancy database somewhere we connect to
Memory = dict[str, TaskParams]()


class BasicImplementation(TaskManager):
    async def mark_done(self, task_id: str) -> None:
        task = Memory.get(task_id)
        if task:
            task.status = "done"

    async def mark_error(self, task_id: str) -> None:
        task = Memory.get(task_id)
        if task:
            task.status = "error"

    async def create_task(self, task_id: str) -> TaskParams:
        fname = Path(task_id).with_suffix(".csv")
        task = TaskParams(task_id, str(fname))
        Memory[task_id] = task
        return task

    async def find_task(self, task_id: str) -> TaskParams | None:
        return Memory.get(task_id, None)
