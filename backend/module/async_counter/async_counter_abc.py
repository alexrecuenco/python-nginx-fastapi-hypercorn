from abc import ABC, abstractmethod
from typing import AsyncIterable, Generic, TypeVar

T = TypeVar("T", str, tuple[str])


class CSVAsyncCounterABC(Generic[T], ABC):
    @abstractmethod
    async def count(self, key: T, count: int):
        pass

    @abstractmethod
    async def items(self) -> AsyncIterable[tuple[T, int]]:
        pass
