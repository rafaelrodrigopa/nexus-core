import pytest
from nexus_core.concurrency.monotonic_queue import MonotonicMaxQueue


def test_monotonic_max_queue():
    mq = MonotonicMaxQueue()
    mq.push(3)
    mq.push(1)
    assert mq.max() == 3
    mq.push(5)
    assert mq.max() == 5
    mq.push(2)
    assert mq.max() == 5
    assert mq.pop() == 3
    assert mq.max() == 5
    assert mq.pop() == 1
    assert mq.max() == 5
    assert mq.pop() == 5
    assert mq.max() == 2
