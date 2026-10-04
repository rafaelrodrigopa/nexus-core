import pytest
from nexus_core.algorithms.search_ext import exponential_search


def test_exponential_search():
    arr = [2, 3, 4, 10, 40, 55, 70, 85, 100, 150, 200]
    assert exponential_search(arr, 10) == 3
    assert exponential_search(arr, 2) == 0
    assert exponential_search(arr, 200) == 10
    assert exponential_search(arr, 999) is None
    assert exponential_search([], 5) is None
