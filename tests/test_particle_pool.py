import pytest

import particle_pool as pp


def pool(free=None, active=None):
    return {"free": list(free or []), "active": list(active or [])}


def test_acquire_from_free():
    assert pp.transact(pool([1, 2]), 1, None, 10) == {"free": [1], "active": [2]}


def test_acquire_new_ids_when_free_empty():
    assert pp.transact(pool([], [1]), 1, None, 10) == {"free": [], "active": [1, 2]}


def test_release_returns_to_free():
    assert pp.transact(pool([], [1]), 0, [1], 10) == {"free": [1], "active": []}


def test_release_unknown_is_rejected():
    with pytest.raises(ValueError):
        pp.transact(pool(), 0, [9], 10)


def test_double_release_is_rejected():
    with pytest.raises(ValueError):
        pp.transact(pool([1], []), 0, [1], 10)


def test_capacity_is_enforced():
    with pytest.raises(ValueError):
        pp.transact(pool([], [1]), 1, None, 1)


def test_negative_acquire_is_rejected():
    with pytest.raises(ValueError):
        pp.transact(pool(), -1, None, 10)


def test_zero_acquire_is_allowed():
    assert pp.transact(pool([1]), 0, None, 10) == {"free": [1], "active": []}


def test_pool_must_be_dict():
    with pytest.raises(ValueError):
        pp.transact([], 1, None, 10)


def test_free_must_be_list():
    with pytest.raises(ValueError):
        pp.transact({"free": "1", "active": []}, 1, None, 10)


def test_active_must_be_list():
    with pytest.raises(ValueError):
        pp.transact({"free": [], "active": "1"}, 1, None, 10)


def test_duplicate_free_id_is_rejected():
    with pytest.raises(ValueError):
        pp.transact(pool([1, 1]), 0, None, 10)


def test_free_and_active_overlap_is_rejected():
    with pytest.raises(ValueError):
        pp.transact({"free": [1], "active": [1]}, 0, None, 10)


def test_zero_capacity_is_rejected():
    with pytest.raises(ValueError):
        pp.transact(pool(), 0, None, 0)


def test_transact_is_deterministic():
    assert pp.transact(pool([1, 2]), 1, None, 10) == {"free": [1], "active": [2]}
