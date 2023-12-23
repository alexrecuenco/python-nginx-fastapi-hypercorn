import typing
from collections import Counter
from csv import DictReader, DictWriter
from io import StringIO
from typing import Iterable

COLS_COLLECT = ("Song", "Date")
COL_COUNT = "Number of Plays"
COL_TOTAL = "Total Number of Plays for Date"


def __iter_inputs(input: Iterable[str]) -> Iterable[str]:
    for line in DictReader(input):
        key = tuple(line.get(col) for col in COLS_COLLECT)
        value = line.get(COL_COUNT)
        yield (key, int(value))


def __iter_outputs(
    counter: Counter[tuple[str], int],
    *,
    output: typing.TextIO,
):
    columns = [*COLS_COLLECT, COL_TOTAL]

    writer = DictWriter(output, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for key, count in counter.items():
        writer.writerow(dict(zip(columns, [*key, count])))


def process(input: Iterable[str], *, output: typing.TextIO) -> Iterable[str]:
    counter = Counter()
    for key, count in __iter_inputs(input):
        counter[key] += count

    __iter_outputs(counter, output=output)
