import pytest

import formation_steering as fs

AGENTS = [
    {"id": "t", "role": "tank", "pos": [0, 0]},
    {"id": "h", "role": "healer", "pos": [10, 0]},
]
SLOTS = [
    {"id": "s1", "role": "tank", "pos": [1, 0]},
    {"id": "s2", "role": "healer", "pos": [9, 0]},
]


def test_valid_assignment():
    assert fs.assign(AGENTS, SLOTS) == {"s1": "t", "s2": "h"}


def test_role_mismatch_is_rejected():
    with pytest.raises(ValueError):
        fs.assign([{"id": "t", "role": "tank", "pos": [0, 0]}], [{"id": "s1", "role": "healer", "pos": [0, 0]}])


def test_duplicate_agent_id_is_rejected():
    with pytest.raises(ValueError):
        fs.assign([AGENTS[0], dict(AGENTS[0])], SLOTS)


def test_duplicate_slot_id_is_rejected():
    with pytest.raises(ValueError):
        fs.assign(AGENTS, [SLOTS[0], dict(SLOTS[0])])


def test_missing_role_is_rejected():
    with pytest.raises(ValueError):
        fs.assign([{"id": "t", "pos": [0, 0]}], SLOTS)


def test_invalid_position_is_rejected():
    with pytest.raises(ValueError):
        fs.assign([{"id": "t", "role": "tank", "pos": "x"}], SLOTS)


def test_obstacle_blocks_slot():
    assert fs.assign(AGENTS, SLOTS, obstacles=[[1, 0]]) == {"s2": "h"}


def test_empty_slots_returns_empty():
    assert fs.assign(AGENTS, []) == {}
    assert fs.assign(AGENTS, SLOTS) == {"s1": "t", "s2": "h"}


def test_empty_agents_returns_empty():
    assert fs.assign([], SLOTS) == {}
    assert fs.assign(AGENTS, SLOTS) == {"s1": "t", "s2": "h"}


def test_agents_must_be_list():
    with pytest.raises(ValueError):
        fs.assign({"id": "t"}, SLOTS)


def test_slots_must_be_list():
    with pytest.raises(ValueError):
        fs.assign(AGENTS, {"id": "s1"})


def test_agent_must_be_dict():
    with pytest.raises(ValueError):
        fs.assign(["t"], SLOTS)


def test_slot_must_be_dict():
    with pytest.raises(ValueError):
        fs.assign(AGENTS, ["s1"])


def test_nearest_slot_is_chosen():
    agents = [{"id": "t", "role": "tank", "pos": [0, 0]}]
    slots = [{"id": "far", "role": "tank", "pos": [20, 0]}, {"id": "near", "role": "tank", "pos": [1, 0]}]
    assert fs.assign(agents, slots) == {"near": "t"}


def test_assignment_is_deterministic():
    assert fs.assign(AGENTS, SLOTS) == {"s1": "t", "s2": "h"}
    assert fs.assign(AGENTS, SLOTS) == fs.assign(AGENTS, SLOTS)
