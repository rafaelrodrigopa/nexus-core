"""
Unit tests for telemetry and structured logger
"""

import json
from nexus_core.telemetry import MetricsCollector, StructuredLogger


def test_metrics_collector():
    collector = MetricsCollector()
    collector.increment("requests_total", 5)
    collector.increment("requests_total", 3)
    collector.gauge("active_connections", 42)
    collector.observe("latency_ms", 12.5)
    collector.observe("latency_ms", 25.0)

    snap = collector.snapshot()
    assert snap["counters"]["requests_total"] == 8
    assert snap["gauges"]["active_connections"] == 42
    assert snap["histograms"]["latency_ms"]["count"] == 2
    assert snap["histograms"]["latency_ms"]["avg"] == (12.5 + 25.0) / 2


def test_structured_logger():
    logger = StructuredLogger(service_name="test-service")
    log_line = logger.log("info", "cache_hit", key="user:123", latency=0.002)

    parsed = json.loads(log_line)
    assert parsed["service"] == "test-service"
    assert parsed["level"] == "INFO"
    assert parsed["event"] == "cache_hit"
    assert parsed["context"]["key"] == "user:123"
