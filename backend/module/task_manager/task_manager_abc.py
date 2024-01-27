from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal


@dataclass
class TaskParams:
    task_id: str
    """Unique id
    """
    output_filename: str
    """PATH relative to the downloads folder
    """
    status: Literal["done", "error", "unknown_error", "processing"] = "processing"


class TaskManager(ABC):
    @abstractmethod
    async def mark_done(self, task_id: str) -> None:
        pass

    async def mark_error(self, task_id: str) -> None:
        pass

    async def create_task(self, task_id: str) -> TaskParams:
        pass

    async def find_task(self, task_id: str) -> TaskParams | None:
        pass
