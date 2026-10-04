import pytest
from nexus_core.algorithms.fenwick import FenwickTree


def test_fenwick_tree_prefix_and_range():
    data = [2, 1, 4, 6, -1, 5, -3]
    ft = FenwickTree.from_list(data)
    assert ft.prefix_sum(1) == 2
    assert ft.prefix_sum(4) == 2 + 1 + 4 + 6
    assert ft.range_query(2, 5) == 1 + 4 + 6 + (-1)

    ft.update(3, 5) # 4 becomes 9
    assert ft.range_query(2, 5) == 1 + 9 + 6 + (-1)
