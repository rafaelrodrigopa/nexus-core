import pytest
from nexus_core.structures.skip_list import SkipList


def test_skip_list_operations():
    sl = SkipList()
    elements = [(10, "ten"), (5, "five"), (30, "thirty"), (20, "twenty")]
    for k, v in elements:
        sl.insert(k, v)

    for k, v in elements:
        assert sl.search(k) == v

    assert sl.search(999) is None
    sl.insert(10, "TEN_UPDATED")
    assert sl.search(10) == "TEN_UPDATED"
