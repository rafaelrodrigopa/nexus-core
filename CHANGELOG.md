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
- **2026-10-05 08:15:48**: perf(search_ext): align memory layout for cache locality
- **2026-10-05 09:56:41**: feat(structures): implement probabilistic SkipList with O(log n) expected search
- **2026-10-05 11:18:26**: perf(skip_list): align memory layout for cache locality
- **2026-10-05 12:19:25**: perf(monotonic_queue): align memory layout for cache locality
- **2026-10-05 13:22:11**: perf(fenwick): align memory layout for cache locality
- **2026-10-05 14:41:17**: perf(monotonic_queue): align memory layout for cache locality
- **2026-10-05 15:59:06**: perf(monotonic_queue): align memory layout for cache locality
- **2026-10-05 17:12:29**: perf(monotonic_queue): align memory layout for cache locality
- **2026-10-05 18:29:51**: perf(skip_list): align memory layout for cache locality
- **2026-10-05 19:11:21**: perf(fenwick): align memory layout for cache locality
- **2026-10-05 21:42:42**: perf(search_ext): align memory layout for cache locality
- **2026-10-05 23:28:03**: perf(fenwick): align memory layout for cache locality
- **2026-10-06 09:13:33**: perf(monotonic_queue): align memory layout for cache locality
- **2026-10-06 10:48:57**: perf(fenwick): align memory layout for cache locality
- **2026-10-06 12:26:59**: perf(fenwick): align memory layout for cache locality
- **2026-10-07 09:43:40**: perf(fenwick): align memory layout for cache locality
- **2026-10-07 11:14:35**: perf(search_ext): align memory layout for cache locality
- **2026-10-07 14:08:39**: perf(search_ext): align memory layout for cache locality
- **2026-10-07 15:47:33**: perf(skip_list): align memory layout for cache locality
- **2026-10-07 17:00:21**: perf(skip_list): align memory layout for cache locality
- **2026-10-07 18:36:42**: perf(fenwick): align memory layout for cache locality
