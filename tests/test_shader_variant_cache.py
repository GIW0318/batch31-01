import pytest

import shader_variant_cache as sv


def test_miss_appends_key():
    assert sv.access(["a"], "b", 3) == {"cache": ["a", "b"], "hit": False, "evicted": None}


def test_hit_moves_key_to_end():
    assert sv.access(["a", "b", "c"], "a", 3) == {"cache": ["b", "c", "a"], "hit": True, "evicted": None}


def test_capacity_evicts_oldest():
    assert sv.access(["a", "b"], "c", 2) == {"cache": ["b", "c"], "hit": False, "evicted": "a"}


def test_capacity_one():
    assert sv.access(["a"], "b", 1) == {"cache": ["b"], "hit": False, "evicted": "a"}


def test_zero_capacity_is_rejected():
    with pytest.raises(ValueError):
        sv.access([], "a", 0)


def test_negative_capacity_is_rejected():
    with pytest.raises(ValueError):
        sv.access([], "a", -1)


def test_empty_key_is_rejected():
    with pytest.raises(ValueError):
        sv.access([], "", 2)


def test_cache_must_be_list():
    with pytest.raises(ValueError):
        sv.access({"a": 1}, "b", 2)


def test_key_must_be_string():
    with pytest.raises(ValueError):
        sv.access([], 1, 2)


def test_duplicate_cache_key_is_not_duplicated():
    assert sv.access(["a", "a"], "b", 3) == {"cache": ["a", "b"], "hit": False, "evicted": None}


def test_hit_returns_no_eviction():
    assert sv.access(["a", "b"], "a", 2)["evicted"] is None


def test_miss_returns_no_eviction_when_space():
    assert sv.access(["a"], "b", 2)["evicted"] is None


def test_eviction_returns_key():
    assert sv.access(["a", "b"], "c", 2)["evicted"] == "a"


def test_non_string_cache_entry_is_rejected():
    with pytest.raises(ValueError):
        sv.access(["a", 1], "b", 3)


def test_access_is_deterministic():
    assert sv.access(["a", "b"], "c", 2) == {"cache": ["b", "c"], "hit": False, "evicted": "a"}
