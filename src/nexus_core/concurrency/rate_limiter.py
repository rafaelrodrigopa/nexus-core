"""
Token Bucket Rate Limiter
=========================
Sub-millisecond token refill algorithm for API throughput throttling.
"""

import time
import threading


class TokenBucketRateLimiter:
    """
    Classic Token Bucket algorithm for controlling transaction burst and sustained rates.
    """

    def __init__(self, capacity: int, refill_rate_per_sec: float) -> None:
        if capacity <= 0 or refill_rate_per_sec <= 0:
            raise ValueError("Capacity and refill rate must both be positive.")
        self.capacity = float(capacity)
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last_update = time.time()
        self._lock = threading.Lock()

    def acquire(self, tokens: int = 1, block: bool = True, timeout: float = 5.0) -> bool:
        start_wait = time.time()
        with self._lock:
            while True:
                self._refill()
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True

                if not block:
                    return False

                now = time.time()
                if now - start_wait >= timeout:
                    return False

                # Calculate required sleep duration to get sufficient tokens
                needed = tokens - self.tokens
                sleep_time = min(needed / self.refill_rate, 0.05)
                time.sleep(sleep_time)

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.last_update
        self.last_update = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
