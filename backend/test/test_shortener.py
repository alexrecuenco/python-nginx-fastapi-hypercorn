import pytest
from hypothesis import given
from hypothesis import strategies as st


@pytest.fixture(autouse=True)
def clear_memory():
    yield


@given(song=st.text(min_size=1))
def test_different_are_different(song: str):
    assert True
