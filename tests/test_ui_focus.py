import pytest

import ui_focus as uf

NODES = {
    "a": {"pos": [0, 0], "disabled": False},
    "b": {"pos": [10, 0], "disabled": False},
    "c": {"pos": [0, 10], "disabled": False},
}


def test_move_right():
    assert uf.move(NODES, "a", "right") == "b"


def test_move_down():
    assert uf.move(NODES, "a", "down") == "c"


def test_disabled_node_is_skipped():
    nodes = {**NODES, "b": {"pos": [10, 0], "disabled": True}}
    assert uf.move(nodes, "a", "right") == "a"


def test_no_candidate_keeps_current():
    assert uf.move(NODES, "b", "right") == "b"


def test_invalid_direction_is_rejected():
    with pytest.raises(ValueError):
        uf.move(NODES, "a", "diagonal")


def test_missing_current_is_rejected():
    with pytest.raises(ValueError):
        uf.move(NODES, "ghost", "right")


def test_nodes_must_be_dict():
    with pytest.raises(ValueError):
        uf.move([], "a", "right")


def test_node_missing_position_is_rejected():
    with pytest.raises(ValueError):
        uf.move({"a": {"disabled": False}}, "a", "right")


def test_invalid_position_is_rejected():
    with pytest.raises(ValueError):
        uf.move({"a": {"pos": "0,0", "disabled": False}}, "a", "right")


def test_empty_nodes_is_rejected():
    with pytest.raises(ValueError):
        uf.move({}, "a", "right")


def test_nearest_in_direction_wins():
    nodes = {"a": {"pos": [0, 0], "disabled": False}, "near": {"pos": [1, 0], "disabled": False}, "far": {"pos": [9, 0], "disabled": False}}
    assert uf.move(nodes, "a", "right") == "near"


def test_diagonal_is_not_selected_for_right():
    nodes = {"a": {"pos": [0, 0], "disabled": False}, "diag": {"pos": [1, 1], "disabled": False}}
    assert uf.move(nodes, "a", "right") == "a"


def test_duplicate_position_is_rejected():
    nodes = {"a": {"pos": [0, 0], "disabled": False}, "b": {"pos": [0, 0], "disabled": False}}
    with pytest.raises(ValueError):
        uf.move(nodes, "a", "right")


def test_disabled_must_be_bool():
    with pytest.raises(ValueError):
        uf.move({"a": {"pos": [0, 0], "disabled": "no"}}, "a", "right")


def test_move_is_deterministic():
    assert uf.move(NODES, "a", "right") == "b"
