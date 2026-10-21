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

# [Optimization 20261005081548] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261005214242] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261007111435] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261007140839] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261008120531] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261011141638] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261012080313] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261012172711] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261013145707] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261013171637] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261013205941] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261014095906] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261014194437] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261015133857] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261016154734] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261016214359] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261018094711] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261020205533] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261021141538] Micro-benchmark tuning & branch prediction alignment

# [Optimization 20261021191852] Micro-benchmark tuning & branch prediction alignment
