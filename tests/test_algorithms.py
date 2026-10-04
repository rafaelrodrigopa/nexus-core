"""
Unit tests for algorithms (Graph, Segment Tree, Trie)
"""

import pytest
from nexus_core.algorithms.graph import DirectedGraph
from nexus_core.algorithms.trees import SegmentTree, Trie


def test_dijkstra_shortest_path():
    g = DirectedGraph()
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("C", "B", 1)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 8)

    distances, predecessors = g.dijkstra("A")
    assert distances["A"] == 0
    assert distances["C"] == 2
    assert distances["B"] == 3
    assert distances["D"] == 8
    assert predecessors["B"] == "C"


def test_topological_sort():
    g = DirectedGraph()
    g.add_edge("Build", "Test")
    g.add_edge("Test", "Package")
    g.add_edge("Package", "Deploy")

    order = g.topological_sort()
    assert order == ["Build", "Test", "Package", "Deploy"]


def test_topological_sort_cycle():
    g = DirectedGraph()
    g.add_edge("A", "B")
    g.add_edge("B", "A")
    with pytest.raises(ValueError, match="cycle"):
        g.topological_sort()


def test_segment_tree_min_and_sum():
    data = [1, 3, 2, 7, 9, 11]
    st_min = SegmentTree(data, func=min, default=float("inf"))
    assert st_min.query(1, 4) == 2

    st_min.update(2, 10)
    assert st_min.query(1, 4) == 3

    st_sum = SegmentTree(data, func=lambda a, b: a + b, default=0)
    assert st_sum.query(0, 2) == 1 + 3 + 2


def test_trie_prefix_search():
    trie = Trie()
    trie.insert("algorithm", {"lang": "python"})
    trie.insert("algebra")
    trie.insert("align")

    assert trie.search("algorithm") is True
    assert trie.search("algo") is False
    assert trie.starts_with("alg") is True
    assert trie.starts_with("xyz") is False
