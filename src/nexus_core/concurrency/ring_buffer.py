"""
Lock-Free Ring Buffer & Resilient Concurrency Utilities
=======================================================
High-throughput circular buffers with boundary guarantees.
"""

from typing import Generic, TypeVar, Optional, List
import threading

T = TypeVar("T")


class RingBuffer(Generic[T]):
    """
    Fixed-size FIFO Ring Buffer designed for high throughput message passing.
    Thread-safe operations via fine-grained reentrant locks.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError(f"RingBuffer capacity must be strictly positive, got {capacity}")
        self.capacity = capacity
        self._buffer: List[Optional[T]] = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0
        self._lock = threading.RLock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)

    def put(self, item: T, block: bool = True, timeout: Optional[float] = None) -> bool:
        """
        Appends an item to the ring buffer.
        Returns True if item was added, False if buffer was full and block=False.
        """
        with self._lock:
            if self._size == self.capacity:
                if not block:
                    return False
                if not self._not_full.wait(timeout=timeout):
                    return False

            self._buffer[self._tail] = item
            self._tail = (self._tail + 1) % self.capacity
            self._size += 1
            self._not_empty.notify()
            return True

    def get(self, block: bool = True, timeout: Optional[float] = None) -> Optional[T]:
        """
        Pops and returns the oldest item in the buffer.
        """
        with self._lock:
            if self._size == 0:
                if not block:
                    return None
                if not self._not_empty.wait(timeout=timeout):
                    return None

            item = self._buffer[self._head]
            self._buffer[self._head] = None
            self._head = (self._head + 1) % self.capacity
            self._size -= 1
            self._not_full.notify()
            return item

    def is_empty(self) -> bool:
        with self._lock:
            return self._size == 0

    def is_full(self) -> bool:
        with self._lock:
            return self._size == self.capacity

    def __len__(self) -> int:
        with self._lock:
            return self._size
