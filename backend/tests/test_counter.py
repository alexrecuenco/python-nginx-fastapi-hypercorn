from io import StringIO
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st
from module import process


def local_path(fname: str):
    return Path(__file__).parent / fname


@pytest.fixture
def input_path():
    return local_path("test.input.csv")


@pytest.fixture
def output_path():
    return local_path("test.output.csv")


def test_given_example(input_path: Path, output_path: Path):
    processedIO = StringIO()
    process(input_path.open(), output=processedIO)
    processedIO.seek(0)
    processed = list(processedIO)
    expected = list(output_path.open())
    processed.sort()
    expected.sort()
    assert processed == expected
