from collections import Counter

from .async_counter_abc import CSVAsyncCounterABC, T


class BasicAsyncCounter(CSVAsyncCounterABC[T]):
    def __init__(self):
        self.counter = Counter()

    async def count(self, key: T, count: int):
        self.counter[key] += count

    async def items(self):
        for key, count in self.counter.items():
            yield key, count
