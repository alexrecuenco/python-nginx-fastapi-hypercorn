from pathlib import Path

import pytest
from aiofiles import open as aio_open
from aiofiles.tempfile import TemporaryDirectory

# from hypothesis import given
# from hypothesis import strategies as st
from module import ProcessCSVConfig, process_csv


def local_path(fname: str):
    return Path(__file__).parent / fname


@pytest.fixture
def input_path():
    return local_path("test.input.csv")


@pytest.fixture
def expect_path():
    return local_path("test.output.csv")


@pytest.mark.asyncio
async def test_given_example(input_path: Path, expect_path: Path):
    dir: str
    async with aio_open(input_path) as aio_f, TemporaryDirectory("w") as dir:
        output_path = Path(dir) / "output.csv"
        await process_csv(aio_f, config=ProcessCSVConfig(output_path))
        with output_path.open() as out, expect_path.open() as expected:
            assert sorted(out) == sorted(expected)
