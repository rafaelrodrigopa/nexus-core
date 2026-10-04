"""
Segment Tree & Trie Implementations
===================================
Advanced balanced structures for range queries and prefix searches.
"""

from typing import List, Callable, Optional, Dict, Any


class SegmentTree:
    """
    Segment Tree with arbitrary associative associative binary operators (Sum, Min, Max, GCD).
    Time Complexity:
        - Build: O(n)
        - Query: O(log n)
        - Update: O(log n)
    """

    def __init__(self, data: List[int], func: Callable[[int, int], int] = min, default: int = 0) -> None:
        self.n = len(data)
        self.func = func
        self.default = default
        self.tree = [default] * (4 * self.n if self.n > 0 else 1)
        if self.n > 0:
            self._build(data, 0, 0, self.n - 1)

    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        self._build(data, left_child, start, mid)
        self._build(data, right_child, mid + 1, end)
        self.tree[node] = self.func(self.tree[left_child], self.tree[right_child])

    def update(self, idx: int, value: int) -> None:
        if idx < 0 or idx >= self.n:
            raise IndexError(f"Index {idx} out of range [0, {self.n - 1}]")
        self._update(0, 0, self.n - 1, idx, value)

    def _update(self, node: int, start: int, end: int, idx: int, value: int) -> None:
        if start == end:
            self.tree[node] = value
            return
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        if idx <= mid:
            self._update(left_child, start, mid, idx, value)
        else:
            self._update(right_child, mid + 1, end, idx, value)
        self.tree[node] = self.func(self.tree[left_child], self.tree[right_child])

    def query(self, l: int, r: int) -> int:
        if l < 0 or r >= self.n or l > r:
            raise ValueError(f"Invalid range query bounds [{l}, {r}]")
        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or end < l:
            return self.default
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        left_res = self._query(2 * node + 1, start, mid, l, r)
        right_res = self._query(2 * node + 2, mid + 1, end, l, r)
        if left_res == self.default:
            return right_res
        if right_res == self.default:
            return left_res
        return self.func(left_res, right_res)


class TrieNode:
    """Trie node for fast prefix exploration."""

    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.is_terminal: bool = False
        self.metadata: Optional[Dict[str, Any]] = None


class Trie:
    """
    Prefix Tree for fast lexical lookups.
    Time Complexity: O(L) where L is the length of the string key.
    """

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_terminal = True
        curr.metadata = metadata

    def search(self, word: str) -> bool:
        curr = self._traverse(word)
        return curr is not None and curr.is_terminal

    def starts_with(self, prefix: str) -> bool:
        return self._traverse(prefix) is not None

    def _traverse(self, text: str) -> Optional[TrieNode]:
        curr = self.root
        for char in text:
            if char not in curr.children:
                return None
            curr = curr.children[char]
        return curr
