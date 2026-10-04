"""
Circuit Breaker Pattern Implementation
=======================================
Guards distributed calls against cascading failures.
"""

import time
import threading
from enum import Enum
from typing import Callable, Any, TypeVar

R = TypeVar("R")


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreakerOpenException(Exception):
    """Raised when call is rejected because circuit is open."""
    pass


class CircuitBreaker:
    """
    Standard state machine for fault tolerance:
    - CLOSED: Normal operation; tracks consecutive failure counts.
    - OPEN: Calls immediately rejected; transitions to HALF_OPEN after recovery_timeout.
    - HALF_OPEN: Probes trial calls; on success closes, on failure re-opens.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exceptions: tuple = (Exception,)
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exceptions = expected_exceptions

        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = CircuitState.CLOSED
        self._lock = threading.Lock()

    def execute(self, func: Callable[..., R], *args: Any, **kwargs: Any) -> R:
        with self._lock:
            self._evaluate_state()
            if self.state == CircuitState.OPEN:
                raise CircuitBreakerOpenException(
                    f"Circuit is OPEN. Trip cooldown remaining: {self.cooldown_remaining:.2f}s"
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exceptions as exc:
            self._on_failure()
            raise exc

    def _evaluate_state(self) -> None:
        if self.state == CircuitState.OPEN:
            now = time.time()
            if now - self.last_failure_time >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN

    def _on_success(self) -> None:
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0

    def _on_failure(self) -> None:
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN

    @property
    def cooldown_remaining(self) -> float:
        if self.state != CircuitState.OPEN:
            return 0.0
        elapsed = time.time() - self.last_failure_time
        return max(0.0, self.recovery_timeout - elapsed)
