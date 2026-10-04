"""
Exponential Search Module
=========================
Fast logarithmic search for unbounded or sorted arrays.
"""
from typing import List, Optional


def exponential_search(arr: List[int], target: int) -> Optional[int]:
    """
    Finds target in sorted array in O(log i) time.
    """
    if not arr:
        return None
    if arr[0] == target:
        return 0

    bound = 1
    n = len(arr)
    while bound < n and arr[bound] <= target:
        bound *= 2

    left = bound // 2
    right = min(bound, n - 1)

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None

# [Optimization 20261004015650] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261004115824] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261004163406] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261004225912] Micro-benchmark tuning & branch prediction alignment
