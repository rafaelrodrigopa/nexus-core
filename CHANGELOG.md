# Changelog

All notable changes to the Nexus Core project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-04

### Added
- Core algorithms engine: `DirectedGraph` (Dijkstra, Kahn Topological Sort), `SegmentTree`, `Trie`.
- High-concurrency primitives: `RingBuffer`, `CircuitBreaker`, `TokenBucketRateLimiter`.
- Resilient data structures: `LRUCache`, `BloomFilter`, `DisjointSetUnion`.
- Observability and metrics: `MetricsCollector` and `StructuredLogger`.
- Full pytest test suite with coverage guarantees.
- Autonomous activity engine and orchestrator DAG integration.
- **2026-10-04 01:45:40**: perf(algorithms): implement exponential search with tight logarithmic boundaries
- **2026-10-04 01:56:50**: perf(search_ext): align memory layout for cache locality
- **2026-10-04 08:24:42**: feat(concurrency): implement MonotonicQueue for O(1) sliding window extremes
- **2026-10-04 10:14:59**: feat(algorithms): implement Fenwick Tree (Binary Indexed Tree) with point & range queries
- **2026-10-04 11:58:24**: perf(search_ext): align memory layout for cache locality
- **2026-10-04 13:24:40**: perf(fenwick): align memory layout for cache locality
- **2026-10-04 15:15:13**: perf(monotonic_queue): align memory layout for cache locality
- **2026-10-04 16:34:06**: perf(search_ext): align memory layout for cache locality
- **2026-10-04 19:29:02**: perf(fenwick): align memory layout for cache locality
