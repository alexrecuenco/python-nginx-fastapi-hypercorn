from enum import Enum

from .async_counter_abc import CSVAsyncCounterABC as __AsyncCounterType
from .async_counter_basic import BasicAsyncCounter
from .async_counter_redis import RedisAsyncCounter


class CounterType(str, Enum):
    redis = "redis"
    basic = "basic"


def CSVAsyncCounter(*, counter_type: CounterType) -> __AsyncCounterType:
    match counter_type:
        case CounterType.redis:
            return RedisAsyncCounter()
        case CounterType.basic:
            return BasicAsyncCounter()
        case _:
            raise NotImplementedError()
