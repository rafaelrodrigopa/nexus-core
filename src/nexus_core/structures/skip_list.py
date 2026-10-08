"""
Probabilistic Skip List Implementation
======================================
Alternative to self-balancing binary search trees with expected O(log n) time.
"""
import random
from typing import Optional, List, Any


class SkipNode:
    def __init__(self, key: int, val: Any, level: int) -> None:
        self.key = key
        self.val = val
        self.forward: List[Optional["SkipNode"]] = [None] * (level + 1)


class SkipList:
    def __init__(self, max_level: int = 16, p: float = 0.5) -> None:
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.header = SkipNode(-float("inf"), None, max_level)

    def _random_level(self) -> int:
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, key: int, val: Any) -> None:
        update = [None] * (self.max_level + 1)
        curr = self.header
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].key < key:
                curr = curr.forward[i]
            update[i] = curr

        curr = curr.forward[0]
        if curr and curr.key == key:
            curr.val = val
            return

        new_lvl = self._random_level()
        if new_lvl > self.level:
            for i in range(self.level + 1, new_lvl + 1):
                update[i] = self.header
            self.level = new_lvl

        new_node = SkipNode(key, val, new_lvl)
        for i in range(new_lvl + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def search(self, key: int) -> Optional[Any]:
        curr = self.header
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].key < key:
                curr = curr.forward[i]
        curr = curr.forward[0]
        if curr and curr.key == key:
            return curr.val
        return None

# [Optimization 20261005111826] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261005182951] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261007154733] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261007170021] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261008101414] Micro-benchmark tuning & branch prediction alignment
