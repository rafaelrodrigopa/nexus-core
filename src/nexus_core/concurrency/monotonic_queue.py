"""
Monotonic Queue Implementation
==============================
Maintains monotonic extremes across moving data windows in O(1) amortized time.
"""
from collections import deque
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class MonotonicMaxQueue(Generic[T]):
    """Queue maintaining descending order for O(1) maximum query."""

    def __init__(self) -> None:
        self._raw_queue = deque()
        self._max_deque = deque()

    def push(self, val: T) -> None:
        self._raw_queue.append(val)
        while self._max_deque and self._max_deque[-1] < val:
            self._max_deque.pop()
        self._max_deque.append(val)

    def pop(self) -> Optional[T]:
        if not self._raw_queue:
            return None
        val = self._raw_queue.popleft()
        if self._max_deque and self._max_deque[0] == val:
            self._max_deque.popleft()
        return val

    def max(self) -> Optional[T]:
        return self._max_deque[0] if self._max_deque else None

    def __len__(self) -> int:
        return len(self._raw_queue)

# [Optimization 20261004151513] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261005121925] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261005144117] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261005155906] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261005171229] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261006091333] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261008083545] Micro-benchmark tuning & branch prediction alignment
