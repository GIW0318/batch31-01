import pytest

import achievement_bus as ab

RULES = [{"id": "kills3", "event": "kill", "count": 3, "reward": "gold"}]
EMPTY = {"counts": {}, "unlocked": [], "delivered": []}


def state(**overrides):
    data = {"counts": {}, "unlocked": [], "delivered": []}
    data.update(overrides)
    return data


def test_unknown_event_returns_unchanged_state():
    assert ab.process({"type": "jump", "count": 1}, RULES, state()) == state()


def test_kill_increments_count():
    assert ab.process({"type": "kill", "count": 1}, RULES, state()) == {
        "counts": {"kills3": 1}, "unlocked": [], "delivered": [],
    }


def test_threshold_unlocks_achievement():
    assert ab.process({"type": "kill", "count": 3}, RULES, state()) == {
        "counts": {"kills3": 3}, "unlocked": ["kills3"], "delivered": ["gold"],
    }


def test_reward_is_delivered_once():
    s = state(counts={"kills3": 3}, unlocked=["kills3"], delivered=["gold"])
    assert ab.process({"type": "kill", "count": 1}, RULES, s) == {
        "counts": {"kills3": 4}, "unlocked": ["kills3"], "delivered": ["gold"],
    }


def test_duplicate_event_after_unlock_does_not_duplicate():
    s = state(counts={"kills3": 3}, unlocked=["kills3"], delivered=["gold"])
    assert ab.process({"type": "kill", "count": 2}, RULES, s)["delivered"] == ["gold"]


def test_negative_event_count_is_rejected():
    with pytest.raises(ValueError):
        ab.process({"type": "kill", "count": -1}, RULES, state())


def test_missing_event_type_is_rejected():
    with pytest.raises(ValueError):
        ab.process({"count": 1}, RULES, state())


def test_rule_count_zero_is_rejected():
    with pytest.raises(ValueError):
        ab.process({"type": "kill", "count": 1}, [{"id": "bad", "event": "kill", "count": 0, "reward": "x"}], state())


def test_duplicate_rule_ids_are_rejected():
    with pytest.raises(ValueError):
        ab.process({"type": "kill", "count": 1}, [RULES[0], dict(RULES[0])], state())


def test_rule_missing_id_is_rejected():
    with pytest.raises(ValueError):
        ab.process({"type": "kill", "count": 1}, [{"event": "kill", "count": 1, "reward": "x"}], state())


def test_rules_must_be_list():
    with pytest.raises(ValueError):
        ab.process({"type": "kill", "count": 1}, {"id": "x"}, state())


def test_state_must_be_dict():
    with pytest.raises(ValueError):
        ab.process({"type": "kill", "count": 1}, RULES, [])


def test_multiple_rules_same_event_evaluate():
    rules = RULES + [{"id": "kills1", "event": "kill", "count": 1, "reward": "medal"}]
    assert ab.process({"type": "kill", "count": 1}, rules, state())["unlocked"] == ["kills1"]


def test_count_above_threshold_unlocks_once():
    assert ab.process({"type": "kill", "count": 5}, RULES, state()) == {
        "counts": {"kills3": 5}, "unlocked": ["kills3"], "delivered": ["gold"],
    }


def test_unlock_order_is_stable():
    rules = [{"id": "a", "event": "kill", "count": 1, "reward": "x"}, {"id": "b", "event": "kill", "count": 1, "reward": "y"}]
    assert ab.process({"type": "kill", "count": 1}, rules, state())["unlocked"] == ["a", "b"]
