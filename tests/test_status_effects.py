import pytest

import status_effects as se


def base(**overrides):
    data = {"active": {}, "immunities": []}
    data.update(overrides)
    return data


def eff(**overrides):
    data = {"id": "burn", "duration": 5, "max_stacks": 3, "refresh": True}
    data.update(overrides)
    return data


def test_new_effect_is_applied():
    assert se.apply_effect(base(), eff()) == {"active": {"burn": {"stacks": 1, "remaining": 5}}, "immunities": []}


def test_effect_stacks_up():
    s = se.apply_effect(base(), eff())
    assert se.apply_effect(s, eff())["active"]["burn"]["stacks"] == 2


def test_stacks_are_capped():
    s = base(active={"burn": {"stacks": 3, "remaining": 5}})
    assert se.apply_effect(s, eff())["active"]["burn"]["stacks"] == 3


def test_refresh_updates_duration():
    s = base(active={"burn": {"stacks": 1, "remaining": 2}})
    assert se.apply_effect(s, eff())["active"]["burn"]["remaining"] == 5


def test_non_refresh_keeps_duration():
    s = base(active={"burn": {"stacks": 1, "remaining": 2}})
    assert se.apply_effect(s, eff(refresh=False))["active"]["burn"]["remaining"] == 2


def test_immunity_rejects_effect():
    assert se.apply_effect(base(immunities=["burn"]), eff()) == {"active": {}, "immunities": ["burn"]}


def test_tick_reduces_duration():
    s = base(active={"burn": {"stacks": 1, "remaining": 5}})
    assert se.tick(s, 2)["active"]["burn"]["remaining"] == 3


def test_expired_effect_is_removed():
    s = base(active={"burn": {"stacks": 1, "remaining": 1}})
    assert se.tick(s, 2)["active"] == {}


def test_negative_tick_is_rejected():
    with pytest.raises(ValueError):
        se.tick(base(), -1)


def test_zero_max_stacks_is_rejected():
    with pytest.raises(ValueError):
        se.apply_effect(base(), eff(max_stacks=0))


def test_missing_effect_id_is_rejected():
    with pytest.raises(ValueError):
        se.apply_effect(base(), {"duration": 5, "max_stacks": 1})


def test_missing_duration_is_rejected():
    with pytest.raises(ValueError):
        se.apply_effect(base(), {"id": "burn", "max_stacks": 1})


def test_state_must_be_dict():
    with pytest.raises(ValueError):
        se.apply_effect([], eff())


def test_immunities_must_be_list():
    with pytest.raises(ValueError):
        se.apply_effect(base(immunities="burn"), eff())


def test_tick_order_is_stable():
    s = base(active={"b": {"stacks": 1, "remaining": 5}, "a": {"stacks": 1, "remaining": 5}})
    assert list(se.tick(s, 1)["active"]) == ["a", "b"]
