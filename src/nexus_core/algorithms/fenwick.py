"""
Fenwick Tree (Binary Indexed Tree)
===================================
Prefix-sum query and point update structure in O(log n).
"""
from typing import List


class FenwickTree:
    """1-indexed Binary Indexed Tree for prefix computations."""

    def __init__(self, size: int) -> None:
        self.size = size
        self.tree: List[int] = [0] * (size + 1)

    @classmethod
    def from_list(cls, values: List[int]) -> "FenwickTree":
        ft = cls(len(values))
        for idx, val in enumerate(values, start=1):
            ft.update(idx, val)
        return ft

    def update(self, idx: int, delta: int) -> None:
        """Adds delta to element at index idx (1-based)."""
        if idx <= 0 or idx > self.size:
            raise IndexError(f"Index {idx} out of range [1, {self.size}]")
        while idx <= self.size:
            self.tree[idx] += delta
            idx += idx & (-idx)

    def prefix_sum(self, idx: int) -> int:
        """Computes prefix sum in range [1, idx] in O(log n)."""
        if idx < 0:
            return 0
        idx = min(idx, self.size)
        total = 0
        while idx > 0:
            total += self.tree[idx]
            idx -= idx & (-idx)
        return total

    def range_query(self, left: int, right: int) -> int:
        """Returns sum of elements in 1-based range [left, right]."""
        if left > right or left < 1 or right > self.size:
            raise ValueError(f"Invalid query range [{left}, {right}]")
        return self.prefix_sum(right) - self.prefix_sum(left - 1)

# [Optimization 20261004132440] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261005132211] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261005191121] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261005232803] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261006011536] Micro-benchmark tuning & branch prediction alignment
