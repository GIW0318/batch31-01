import pytest

import tick_scheduler as ts

TASKS = [
    {"id": "ai", "cost": 3, "priority": 1, "deadline": 100},
    {"id": "net", "cost": 2, "priority": 2, "deadline": 50},
    {"id": "fx", "cost": 4, "priority": 3, "deadline": 200},
]


def test_all_tasks_fit():
    assert ts.schedule(TASKS, 10)["ran"] == ["net", "ai", "fx"]


def test_budget_is_respected():
    out = ts.schedule(TASKS, 3)
    assert out["ran"] == ["net"]
    assert set(out["deferred"]) == {"ai", "fx"}


def test_zero_budget_defers_all():
    assert ts.schedule(TASKS, 0)["ran"] == []
    assert set(ts.schedule(TASKS, 0)["deferred"]) == {"ai", "net", "fx"}


def test_negative_budget_is_rejected():
    with pytest.raises(ValueError):
        ts.schedule(TASKS, -1)


def test_task_larger_than_budget_is_deferred():
    assert ts.schedule([{"id": "big", "cost": 9, "priority": 1, "deadline": 1}], 5)["deferred"] == ["big"]


def test_duplicate_ids_are_rejected():
    with pytest.raises(ValueError):
        ts.schedule([TASKS[0], dict(TASKS[0])], 10)


def test_missing_id_is_rejected():
    with pytest.raises(ValueError):
        ts.schedule([{"cost": 1, "priority": 1, "deadline": 1}], 10)


def test_missing_cost_is_rejected():
    with pytest.raises(ValueError):
        ts.schedule([{"id": "a", "priority": 1, "deadline": 1}], 10)


def test_negative_cost_is_rejected():
    with pytest.raises(ValueError):
        ts.schedule([{"id": "a", "cost": -1, "priority": 1, "deadline": 1}], 10)


def test_cancelled_task_is_excluded():
    tasks = TASKS + [{"id": "cancel", "cost": 1, "priority": 0, "deadline": 0, "cancelled": True}]
    out = ts.schedule(tasks, 10)
    assert "cancel" not in out["ran"]
    assert out["ran"] == ["net", "ai", "fx"]


def test_deadline_precedes_priority():
    tasks = [
        {"id": "late", "cost": 1, "priority": 0, "deadline": 100},
        {"id": "early", "cost": 1, "priority": 9, "deadline": 1},
    ]
    assert ts.schedule(tasks, 10)["ran"] == ["early", "late"]


def test_tasks_must_be_list():
    with pytest.raises(ValueError):
        ts.schedule({"id": "a"}, 10)


def test_task_must_be_dict():
    with pytest.raises(ValueError):
        ts.schedule(["a"], 10)


def test_ran_and_deferred_do_not_overlap():
    out = ts.schedule(TASKS, 3)
    assert out["ran"] == ["net"]
    assert not (set(out["ran"]) & set(out["deferred"]))


def test_schedule_is_stable():
    expected = {"ran": ["net", "ai", "fx"], "deferred": [], "overrun": False}
    assert ts.schedule(TASKS, 10) == expected
    assert ts.schedule(TASKS, 10) == expected
