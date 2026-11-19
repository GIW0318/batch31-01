import pytest

import autotile as at

RULES = {0: "empty", 1: "end", 3: "line", 7: "tee", 15: "full"}


def test_isolated_tile():
    assert at.autotile([[1]], RULES) == ["end"]


def test_full_neighbors():
    grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    assert at.autotile(grid, RULES)[4] == "full"


def test_edge_neighbor_is_empty():
    grid = [[1, 1]]
    assert at.autotile(grid, RULES) == ["line", "line"]


def test_non_rectangular_grid_is_rejected():
    with pytest.raises(ValueError):
        at.autotile([[1], [1, 1]], RULES)


def test_empty_grid_is_rejected():
    with pytest.raises(ValueError):
        at.autotile([], RULES)


def test_invalid_cell_is_rejected():
    with pytest.raises(ValueError):
        at.autotile([[2]], RULES)


def test_missing_rule_is_rejected():
    with pytest.raises(ValueError):
        at.autotile([[1]], {})


def test_rules_must_be_dict():
    with pytest.raises(ValueError):
        at.autotile([[1]], [])


def test_tile_id_must_be_string():
    with pytest.raises(ValueError):
        at.autotile([[1]], {1: 5})


def test_single_cell_grid():
    assert at.autotile([[1]], {1: "one"}) == ["one"]


def test_full_row():
    grid = [[1, 1, 1]]
    assert at.autotile(grid, RULES) == ["line", "line", "line"]


def test_diagonal_is_ignored():
    grid = [[1, 0], [0, 1]]
    assert at.autotile(grid, {1: "one"}) == ["one", "empty", "empty", "one"]


def test_output_length_matches_cells():
    grid = [[1, 0], [0, 1]]
    assert len(at.autotile(grid, RULES)) == 4


def test_grid_must_be_list():
    with pytest.raises(ValueError):
        at.autotile("grid", RULES)


def test_autotile_is_deterministic():
    assert at.autotile([[1]], {1: "one"}) == ["one"]
    assert at.autotile([[1]], {1: "one"}) == at.autotile([[1]], {1: "one"})
