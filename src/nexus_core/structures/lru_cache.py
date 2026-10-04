"""
High-Performance Data Structures
================================
LRU Cache, Bloom Filter, Disjoint-Set Union.
"""

from typing import Dict, Generic, Optional, TypeVar, Any
import hashlib
import math

K = TypeVar("K")
V = TypeVar("V")


class _DListNode(Generic[K, V]):
    def __init__(self, key: Optional[K] = None, val: Optional[V] = None) -> None:
        self.key = key
        self.val = val
        self.prev: Optional["_DListNode[K, V]"] = None
        self.next: Optional["_DListNode[K, V]"] = None


class LRUCache(Generic[K, V]):
    """
    Constant time O(1) Least Recently Used (LRU) Cache backed by doubly-linked hash map.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError(f"Cache capacity must be strictly positive, got {capacity}")
        self.capacity = capacity
        self.cache: Dict[K, _DListNode[K, V]] = {}
        self.head: _DListNode[K, V] = _DListNode()
        self.tail: _DListNode[K, V] = _DListNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _DListNode[K, V]) -> None:
        prev_node = node.prev
        next_node = node.next
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node

    def _add_to_front(self, node: _DListNode[K, V]) -> None:
        node.next = self.head.next
        node.prev = self.head
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def get(self, key: K) -> Optional[V]:
        if key not in self.cache:
            return None
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.val

    def put(self, key: K, val: V) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = val
            self._remove(node)
            self._add_to_front(node)
            return

        if len(self.cache) >= self.capacity:
            lru = self.tail.prev
            if lru and lru.key is not None:
                self._remove(lru)
                del self.cache[lru.key]

        new_node = _DListNode(key, val)
        self.cache[key] = new_node
        self._add_to_front(new_node)

    def __len__(self) -> int:
        return len(self.cache)


class BloomFilter:
    """
    Space-efficient probabilistic data structure to test set membership.
    False positive rate is tunable via expected insertions and error rate.
    """

    def __init__(self, expected_elements: int = 1000, false_positive_rate: float = 0.01) -> None:
        self.expected_elements = expected_elements
        self.error_rate = false_positive_rate
        # Optimal bit array size m = - (n * ln(p)) / (ln(2)^2)
        self.size = int(-1 * (expected_elements * math.log(false_positive_rate)) / (math.log(2) ** 2))
        # Optimal hash count k = (m / n) * ln(2)
        self.hash_count = max(1, int((self.size / expected_elements) * math.log(2)))
        self.bit_array = [0] * self.size

    def _hashes(self, item: str) -> list[int]:
        res = []
        for i in range(self.hash_count):
            seed_data = f"{i}:{item}".encode("utf-8")
            digest = int(hashlib.sha256(seed_data).hexdigest(), 16)
            res.append(digest % self.size)
        return res

    def add(self, item: str) -> None:
        for idx in self._hashes(item):
            self.bit_array[idx] = 1

    def contains(self, item: str) -> bool:
        return all(self.bit_array[idx] == 1 for idx in self._hashes(item))


class DisjointSetUnion:
    """
    Disjoint-Set Union (DSU) / Union-Find with path compression and rank optimization.
    Nearly O(1) amortized operations (Inverse Ackermann complexity α(n)).
    """

    def __init__(self) -> None:
        self.parent: Dict[Any, Any] = {}
        self.rank: Dict[Any, int] = {}

    def find(self, item: Any) -> Any:
        if item not in self.parent:
            self.parent[item] = item
            self.rank[item] = 0
            return item

        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, a: Any, b: Any) -> bool:
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False

        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1
        return True
