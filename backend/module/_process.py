from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterable, Iterable

from aiocsv import AsyncDictReader, AsyncDictWriter
from aiofiles import open as aio_open

from .async_counter import CounterType, CSVAsyncCounter

COLS_COLLECT = ("Song", "Date")
COL_COUNT = "Number of Plays"
COL_TOTAL = "Total Number of Plays for Date"


async def __iter_inputs(input: AsyncIterable[str]) -> Iterable[str]:
    async for line in AsyncDictReader(input):
        key = tuple(line.get(col) for col in COLS_COLLECT)
        value = line.get(COL_COUNT)
        yield (key, int(value))


@dataclass
class ProcessCSVConfig:
    output_path: str | Path
    counter_type: CounterType = CounterType.basic


async def process_csv(
    input: AsyncIterable[str], *, config: ProcessCSVConfig
) -> Iterable[str]:
    # Right now the counter is a local object and this won't scale if the number of days and clients is maximal,
    # In that case, this counter would need to be made an async counter with some database as backend
    counter = CSVAsyncCounter(counter_type=config.counter_type)
    async for key, count in __iter_inputs(input):
        await counter.count(key, count)

    columns = [*COLS_COLLECT, COL_TOTAL]
    async with aio_open(config.output_path, "w") as output:
        writer = AsyncDictWriter(output, fieldnames=columns, lineterminator="\n")
        await writer.writeheader()
        async for key, count in counter.items():
            await writer.writerow(dict(zip(columns, [*key, count])))
