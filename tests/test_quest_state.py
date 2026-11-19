import pytest

import quest_state as qs

BASE = {"id": "q1", "status": "locked", "steps": [False, False], "branch": None, "rewards": [], "version": 0}


def state(**overrides):
    data = {**BASE, "steps": list(BASE["steps"]), "rewards": list(BASE["rewards"])}
    data.update(overrides)
    return data


def test_accept_locked_is_rejected():
    with pytest.raises(ValueError):
        qs.transition(state(), {"type": "accept"})


def test_accept_available_starts_quest():
    assert qs.transition(state(status="available"), {"type": "accept"}) == {
        "id": "q1", "status": "active", "steps": [False, False], "branch": None, "rewards": [], "version": 1,
    }


def test_accept_active_is_rejected():
    with pytest.raises(ValueError):
        qs.transition(state(status="active"), {"type": "accept"})


def test_progress_first_step():
    assert qs.transition(state(status="active"), {"type": "progress", "step": 0}) == {
        "id": "q1", "status": "active", "steps": [True, False], "branch": None, "rewards": [], "version": 1,
    }


def test_progress_out_of_order_is_rejected():
    with pytest.raises(ValueError):
        qs.transition(state(status="active"), {"type": "progress", "step": 1})


def test_choose_branch_once():
    assert qs.transition(state(status="active"), {"type": "choose", "choice": "a"}) == {
        "id": "q1", "status": "active", "steps": [False, False], "branch": "a", "rewards": [], "version": 1,
    }


def test_choose_branch_twice_is_rejected():
    with pytest.raises(ValueError):
        qs.transition(state(status="active", branch="a"), {"type": "choose", "choice": "b"})


def test_complete_with_incomplete_steps_is_rejected():
    with pytest.raises(ValueError):
        qs.transition(state(status="active"), {"type": "complete"})


def test_complete_grants_reward_once():
    done = state(status="active", steps=[True, True])
    assert qs.transition(done, {"type": "complete"}) == {
        "id": "q1", "status": "completed", "steps": [True, True], "branch": None, "rewards": ["xp"], "version": 1,
    }


def test_complete_twice_does_not_duplicate_reward():
    done = state(status="completed", steps=[True, True], rewards=["xp"])
    assert qs.transition(done, {"type": "complete"})["rewards"] == ["xp"]


def test_fail_sets_terminal_state():
    assert qs.transition(state(status="active"), {"type": "fail"}) == {
        "id": "q1", "status": "failed", "steps": [False, False], "branch": None, "rewards": [], "version": 1,
    }


def test_progress_after_fail_is_rejected():
    with pytest.raises(ValueError):
        qs.transition(state(status="failed"), {"type": "progress", "step": 0})


def test_reset_active_only():
    assert qs.transition(state(status="active", steps=[True, False], branch="a"), {"type": "reset"}) == {
        "id": "q1", "status": "available", "steps": [False, False], "branch": None, "rewards": [], "version": 1,
    }


def test_reset_completed_is_rejected():
    with pytest.raises(ValueError):
        qs.transition(state(status="completed", steps=[True, True], rewards=["xp"]), {"type": "reset"})


def test_unknown_event_is_rejected():
    with pytest.raises(ValueError):
        qs.transition(state(status="active"), {"type": "teleport"})
