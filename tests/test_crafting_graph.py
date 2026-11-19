import pytest

import crafting_graph as cg

RECIPES = [
    {"id": "plank", "inputs": {"wood": 2}, "output": {"plank": 1}},
    {"id": "chair", "inputs": {"plank": 4}, "output": {"chair": 1}},
]


def inv(**items):
    return dict(items)


def test_valid_craft():
    assert cg.craft("plank", RECIPES, inv(wood=4), 10) == {"inventory": {"wood": 2, "plank": 1}, "crafted": "plank"}


def test_missing_recipe_is_rejected():
    with pytest.raises(ValueError):
        cg.craft("ghost", RECIPES, inv(wood=4), 10)


def test_insufficient_material_is_rejected():
    with pytest.raises(ValueError):
        cg.craft("plank", RECIPES, inv(wood=1), 10)


def test_capacity_is_checked():
    with pytest.raises(ValueError):
        cg.craft("plank", RECIPES, inv(wood=4), 2)


def test_negative_input_count_is_rejected():
    with pytest.raises(ValueError):
        cg.craft("plank", [{"id": "bad", "inputs": {"wood": -1}, "output": {"plank": 1}}], inv(wood=4), 10)


def test_zero_input_count_is_rejected():
    with pytest.raises(ValueError):
        cg.craft("plank", [{"id": "bad", "inputs": {"wood": 0}, "output": {"plank": 1}}], inv(wood=4), 10)


def test_duplicate_recipe_ids_are_rejected():
    with pytest.raises(ValueError):
        cg.craft("plank", [RECIPES[0], dict(RECIPES[0])], inv(wood=4), 10)


def test_missing_recipe_id_is_rejected():
    with pytest.raises(ValueError):
        cg.craft("plank", [{"inputs": {"wood": 1}, "output": {"plank": 1}}], inv(wood=4), 10)


def test_missing_output_is_rejected():
    with pytest.raises(ValueError):
        cg.craft("plank", [{"id": "bad", "inputs": {"wood": 1}}], inv(wood=4), 10)


def test_self_reference_is_rejected():
    with pytest.raises(ValueError):
        cg.craft("a", [{"id": "a", "inputs": {"a": 1}, "output": {"a": 2}}], inv(a=2), 10)


def test_dependency_cycle_is_rejected():
    cyclic = [
        {"id": "a", "inputs": {"b": 1}, "output": {"a": 1}},
        {"id": "b", "inputs": {"a": 1}, "output": {"b": 1}},
    ]
    with pytest.raises(ValueError):
        cg.craft("a", cyclic, inv(a=1, b=1), 10)


def test_failed_craft_does_not_mutate_inventory():
    inventory = inv(wood=1)
    with pytest.raises(ValueError):
        cg.craft("plank", RECIPES, inventory, 10)
    assert inventory == {"wood": 1}


def test_duplicate_input_material_is_merged():
    assert cg.craft("plank", [{"id": "plank", "inputs": {"wood": 2}, "output": {"plank": 1}}], inv(wood=2), 10)["inventory"]["plank"] == 1


def test_recipes_must_be_list():
    with pytest.raises(ValueError):
        cg.craft("plank", {"id": "plank"}, inv(wood=4), 10)


def test_recipe_must_be_dict():
    with pytest.raises(ValueError):
        cg.craft("plank", ["plank"], inv(wood=4), 10)
