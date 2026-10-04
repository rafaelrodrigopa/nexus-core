"""
Unit tests for data structures (LRUCache, BloomFilter, DisjointSetUnion)
"""

import pytest
from nexus_core.structures import LRUCache, BloomFilter, DisjointSetUnion


def test_lru_cache_eviction():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1  # 'a' is now most recently used

    cache.put("c", 3)  # should evict 'b'
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_bloom_filter_membership():
    bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
    keys = ["user_101", "user_102", "order_500"]
    for k in keys:
        bf.add(k)

    for k in keys:
        assert bf.contains(k) is True

    assert bf.contains("definitely_not_present_9999") is False


def test_disjoint_set_union():
    dsu = DisjointSetUnion()
    dsu.union(1, 2)
    dsu.union(2, 3)
    dsu.union(4, 5)

    assert dsu.find(1) == dsu.find(3)
    assert dsu.find(1) != dsu.find(4)

    dsu.union(3, 5)
    assert dsu.find(1) == dsu.find(5)
