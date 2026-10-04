"""
Unit tests for concurrency modules (RingBuffer, CircuitBreaker, RateLimiter)
"""

import time
import pytest
from nexus_core.concurrency import RingBuffer, CircuitBreaker, CircuitBreakerOpenException, TokenBucketRateLimiter


def test_ring_buffer_fifo():
    buf = RingBuffer(3)
    assert buf.is_empty()
    assert buf.put(10)
    assert buf.put(20)
    assert buf.put(30)
    assert buf.is_full()
    assert not buf.put(40, block=False)

    assert buf.get() == 10
    assert buf.get() == 20
    assert buf.put(50)
    assert len(buf) == 2
    assert buf.get() == 30
    assert buf.get() == 50
    assert buf.is_empty()


def test_circuit_breaker_transitions():
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)

    def faulty():
        raise RuntimeError("Network timeout")

    def healthy():
        return "success"

    with pytest.raises(RuntimeError):
        cb.execute(faulty)
    with pytest.raises(RuntimeError):
        cb.execute(faulty)

    # Circuit should now be OPEN
    with pytest.raises(CircuitBreakerOpenException):
        cb.execute(healthy)

    # Wait for recovery cooldown
    time.sleep(0.15)

    # Probe call succeeds, circuit transitions back to CLOSED
    assert cb.execute(healthy) == "success"


def test_token_bucket_rate_limiter():
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate_per_sec=10.0)
    assert limiter.acquire(1) is True
    assert limiter.acquire(1) is True
    # Bucket is empty, instant non-blocking request fails
    assert limiter.acquire(1, block=False) is False
