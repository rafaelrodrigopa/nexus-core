"""
Structured Telemetry & Observability
====================================
Lightweight metrics tracking and JSON structured event logging.
"""

from typing import Dict, Any, List
import time
import json
import threading


class MetricsCollector:
    """Thread-safe telemetry metrics aggregator."""

    def __init__(self) -> None:
        self._counters: Dict[str, float] = {}
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def increment(self, metric: str, value: float = 1.0) -> None:
        with self._lock:
            self._counters[metric] = self._counters.get(metric, 0.0) + value

    def gauge(self, metric: str, value: float) -> None:
        with self._lock:
            self._gauges[metric] = value

    def observe(self, metric: str, value: float) -> None:
        with self._lock:
            if metric not in self._histograms:
                self._histograms[metric] = []
            self._histograms[metric].append(value)
            if len(self._histograms[metric]) > 1000:
                self._histograms[metric].pop(0)

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "timestamp": time.time(),
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": {
                    k: {
                        "count": len(v),
                        "avg": sum(v) / len(v) if v else 0.0,
                        "min": min(v) if v else 0.0,
                        "max": max(v) if v else 0.0,
                    }
                    for k, v in self._histograms.items()
                },
            }


class StructuredLogger:
    """JSON structured event logger for observability pipelines."""

    def __init__(self, service_name: str = "nexus-core") -> None:
        self.service_name = service_name

    def log(self, level: str, event: str, **kwargs: Any) -> str:
        record = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "service": self.service_name,
            "level": level.upper(),
            "event": event,
            "context": kwargs,
        }
        output = json.dumps(record)
        return output
