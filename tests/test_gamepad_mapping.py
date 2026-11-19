import pytest

import gamepad_mapping as gm

ACTIONS = ["jump", "attack", "dodge"]


def test_valid_mapping():
    bindings = [{"action": "jump", "button": "A", "chord": []}]
    assert gm.validate_mapping(bindings, ACTIONS) == {"jump": {"button": "A", "chord": []}}


def test_unknown_action_is_rejected():
    with pytest.raises(ValueError):
        gm.validate_mapping([{"action": "fly", "button": "A"}], ACTIONS)


def test_duplicate_action_is_rejected():
    bindings = [{"action": "jump", "button": "A"}, {"action": "jump", "button": "B"}]
    with pytest.raises(ValueError):
        gm.validate_mapping(bindings, ACTIONS)


def test_duplicate_binding_is_rejected():
    bindings = [{"action": "jump", "button": "A"}, {"action": "attack", "button": "A"}]
    with pytest.raises(ValueError):
        gm.validate_mapping(bindings, ACTIONS)


def test_chord_too_long_is_rejected():
    with pytest.raises(ValueError):
        gm.validate_mapping([{"action": "jump", "button": "A", "chord": ["B", "C", "D"]}], ACTIONS)


def test_duplicate_chord_button_is_rejected():
    with pytest.raises(ValueError):
        gm.validate_mapping([{"action": "jump", "button": "A", "chord": ["B", "B"]}], ACTIONS)


def test_empty_button_is_rejected():
    with pytest.raises(ValueError):
        gm.validate_mapping([{"action": "jump", "button": ""}], ACTIONS)


def test_reserved_button_is_rejected():
    with pytest.raises(ValueError):
        gm.validate_mapping([{"action": "jump", "button": "Guide"}], ACTIONS)


def test_bindings_must_be_list():
    with pytest.raises(ValueError):
        gm.validate_mapping({"action": "jump", "button": "A"}, ACTIONS)


def test_binding_must_be_dict():
    with pytest.raises(ValueError):
        gm.validate_mapping(["jump"], ACTIONS)


def test_missing_action_is_rejected():
    with pytest.raises(ValueError):
        gm.validate_mapping([{"button": "A"}], ACTIONS)


def test_missing_button_is_rejected():
    with pytest.raises(ValueError):
        gm.validate_mapping([{"action": "jump"}], ACTIONS)


def test_same_button_different_chord_is_allowed():
    bindings = [{"action": "jump", "button": "A"}, {"action": "attack", "button": "A", "chord": ["B"]}]
    assert set(gm.validate_mapping(bindings, ACTIONS)) == {"jump", "attack"}


def test_button_is_case_normalized():
    assert gm.validate_mapping([{"action": "jump", "button": "a"}], ACTIONS) == {"jump": {"button": "a", "chord": []}}


def test_mapping_is_deterministic():
    bindings = [{"action": "jump", "button": "A"}, {"action": "attack", "button": "B"}]
    expected = {"jump": {"button": "A", "chord": []}, "attack": {"button": "B", "chord": []}}
    assert gm.validate_mapping(bindings, ACTIONS) == expected
    assert gm.validate_mapping(bindings, ACTIONS) == gm.validate_mapping(bindings, ACTIONS)
