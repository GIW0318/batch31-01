import pytest

import interest_management as im

PLAYER = {"pos": [0, 0], "now": 10000}


def ent(eid, x, y, kind="enemy", seen=9000):
    return {"id": eid, "pos": [x, y], "kind": kind, "last_seen": seen}


def test_budget_zero_returns_empty():
    assert im.select([ent("a", 1, 1)], PLAYER, 0) == []
    assert im.select([ent("a", 1, 1)], PLAYER, 1) == ["a"]


def test_negative_budget_is_rejected():
    with pytest.raises(ValueError):
        im.select([ent("a", 1, 1)], PLAYER, -1)


def test_duplicate_ids_are_rejected():
    with pytest.raises(ValueError):
        im.select([ent("a", 1, 1), ent("a", 2, 2)], PLAYER, 10)


def test_missing_id_is_rejected():
    with pytest.raises(ValueError):
        im.select([{"pos": [1, 1], "kind": "enemy", "last_seen": 9000}], PLAYER, 10)


def test_invalid_position_is_rejected():
    with pytest.raises(ValueError):
        im.select([{"id": "a", "pos": "x", "kind": "enemy", "last_seen": 9000}], PLAYER, 10)


def test_stale_entity_is_excluded():
    assert im.select([ent("old", 1, 1, seen=0)], PLAYER, 10) == []
    assert im.select([ent("fresh", 1, 1, seen=9999)], PLAYER, 10) == ["fresh"]


def test_enemy_precedes_prop():
    assert im.select([ent("prop", 1, 1, kind="prop"), ent("enemy", 10, 10, kind="enemy")], PLAYER, 10) == ["enemy", "prop"]


def test_tie_is_sorted_by_id():
    assert im.select([ent("b", 3, 4), ent("a", 3, 4)], PLAYER, 10) == ["a", "b"]


def test_budget_is_respected():
    assert len(im.select([ent("a", 1, 1), ent("b", 2, 2), ent("c", 3, 3)], PLAYER, 2)) == 2


def test_player_missing_position_is_rejected():
    with pytest.raises(ValueError):
        im.select([ent("a", 1, 1)], {"now": 10000}, 10)


def test_entities_must_be_list():
    with pytest.raises(ValueError):
        im.select({"id": "a"}, PLAYER, 10)


def test_entity_must_be_dict():
    with pytest.raises(ValueError):
        im.select(["a"], PLAYER, 10)


def test_distance_boundary_is_included():
    assert im.select([ent("edge", 5, 0)], PLAYER, 10) == ["edge"]


def test_stale_threshold_is_configurable():
    assert im.select([ent("old", 1, 1, seen=0)], PLAYER, 10, stale_after=20000) == ["old"]


def test_selection_is_deterministic():
    entities = [ent("b", 2, 0), ent("a", 2, 0)]
    assert im.select(entities, PLAYER, 10) == ["a", "b"]
    assert im.select(entities, PLAYER, 10) == im.select(entities, PLAYER, 10)
