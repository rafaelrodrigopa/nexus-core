"""
Micro-Benchmark Suite for Nexus Core Components
"""

import time
import random
from nexus_core.structures import LRUCache, BloomFilter
from nexus_core.algorithms import SegmentTree


def benchmark_lru_cache(iterations: int = 100_000) -> float:
    cache = LRUCache(1000)
    start = time.perf_counter()
    for i in range(iterations):
        key = i % 1500
        cache.put(key, i)
        _ = cache.get(key)
    elapsed = time.perf_counter() - start
    ops_sec = (iterations * 2) / elapsed
    print(f"[LRU Cache] {iterations * 2} ops in {elapsed:.4f}s ({ops_sec:,.0f} ops/sec)")
    return elapsed


def benchmark_bloom_filter(iterations: int = 50_000) -> float:
    bf = BloomFilter(expected_elements=iterations, false_positive_rate=0.01)
    start = time.perf_counter()
    for i in range(iterations):
        bf.add(f"token_{i}")
    for i in range(iterations):
        _ = bf.contains(f"token_{i}")
    elapsed = time.perf_counter() - start
    ops_sec = (iterations * 2) / elapsed
    print(f"[Bloom Filter] {iterations * 2} ops in {elapsed:.4f}s ({ops_sec:,.0f} ops/sec)")
    return elapsed


def benchmark_segment_tree(n: int = 10_000, queries: int = 50_000) -> float:
    data = [random.randint(1, 1000) for _ in range(n)]
    st = SegmentTree(data, func=min, default=float("inf"))
    start = time.perf_counter()
    for _ in range(queries):
        l = random.randint(0, n - 2)
        r = random.randint(l, n - 1)
        _ = st.query(l, r)
    elapsed = time.perf_counter() - start
    ops_sec = queries / elapsed
    print(f"[Segment Tree] {queries} queries in {elapsed:.4f}s ({ops_sec:,.0f} ops/sec)")
    return elapsed


if __name__ == "__main__":
    print("=" * 60)
    print("NEXUS CORE MICRO-BENCHMARKS")
    print("=" * 60)
    benchmark_lru_cache()
    benchmark_bloom_filter()
    benchmark_segment_tree()
