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
- **2026-10-06 01:15:36**: perf(fenwick): align memory layout for cache locality
- **2026-10-07 17:22:54**: perf(search_ext): align memory layout for cache locality
- **2026-10-07 22:59:16**: perf(fenwick): align memory layout for cache locality
- **2026-10-08 17:20:04**: perf(skip_list): align memory layout for cache locality
- **2026-10-08 23:13:54**: perf(skip_list): align memory layout for cache locality
- **2026-10-09 16:55:56**: perf(search_ext): align memory layout for cache locality
- **2026-10-09 22:32:10**: perf(search_ext): align memory layout for cache locality
- **2026-10-10 15:49:26**: perf(monotonic_queue): align memory layout for cache locality
- **2026-10-10 19:58:25**: perf(skip_list): align memory layout for cache locality
- **2026-10-10 23:28:02**: perf(skip_list): align memory layout for cache locality
- **2026-10-11 16:13:50**: perf(fenwick): align memory layout for cache locality
- **2026-10-11 21:45:35**: perf(fenwick): align memory layout for cache locality
- **2026-10-13 01:57:07**: perf(skip_list): align memory layout for cache locality
- **2026-10-13 17:31:04**: perf(monotonic_queue): align memory layout for cache locality
- **2026-10-13 22:34:13**: perf(skip_list): align memory layout for cache locality
- **2026-10-14 14:58:52**: perf(search_ext): align memory layout for cache locality
- **2026-10-15 00:24:17**: perf(search_ext): align memory layout for cache locality
- **2026-10-15 14:49:20**: perf(search_ext): align memory layout for cache locality
- **2026-10-16 14:43:03**: perf(search_ext): align memory layout for cache locality
- **2026-10-16 19:30:09**: perf(skip_list): align memory layout for cache locality
- **2026-10-17 13:35:22**: perf(skip_list): align memory layout for cache locality
- **2026-10-17 16:58:20**: perf(monotonic_queue): align memory layout for cache locality
- **2026-10-17 23:55:26**: perf(search_ext): align memory layout for cache locality
- **2026-10-18 17:13:41**: perf(search_ext): align memory layout for cache locality
- **2026-10-18 20:27:54**: perf(monotonic_queue): align memory layout for cache locality
- **2026-10-19 22:15:08**: perf(search_ext): align memory layout for cache locality
- **2026-10-20 19:57:13**: perf(search_ext): align memory layout for cache locality
- **2026-10-21 15:01:06**: perf(search_ext): align memory layout for cache locality
- **2026-10-22 00:34:03**: perf(search_ext): align memory layout for cache locality
- **2026-10-22 19:56:23**: perf(search_ext): align memory layout for cache locality
- **2026-10-23 14:52:43**: perf(monotonic_queue): align memory layout for cache locality
- **2026-10-23 19:54:30**: perf(skip_list): align memory layout for cache locality
- **2026-10-24 13:56:09**: perf(monotonic_queue): align memory layout for cache locality
