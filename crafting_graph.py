_MISSING = object()


def _is_positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _is_non_negative_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _validate_item_name(name, field):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("%s contains an invalid item id" % field)


def _validate_item_counts(items, field, allow_empty):
    if not isinstance(items, dict):
        raise ValueError("%s must be a dict" % field)
    if not allow_empty and not items:
        raise ValueError("%s must not be empty" % field)

    for item, count in items.items():
        _validate_item_name(item, field)
        if not _is_positive_int(count):
            raise ValueError("%s counts must be positive integers" % field)


def _build_recipe_map(recipes):
    if not isinstance(recipes, list):
        raise ValueError("recipes must be a list")

    recipe_map = {}
    for recipe in recipes:
        if not isinstance(recipe, dict):
            raise ValueError("each recipe must be a dict")

        recipe_id = recipe.get("id", _MISSING)
        if recipe_id is _MISSING:
            raise ValueError("recipe is missing an id")
        if not isinstance(recipe_id, str) or not recipe_id.strip():
            raise ValueError("recipe id must be a non-empty string")
        if recipe_id in recipe_map:
            raise ValueError("duplicate recipe id: %s" % recipe_id)

        if "inputs" not in recipe:
            raise ValueError("recipe %s is missing inputs" % recipe_id)
        if "output" not in recipe:
            raise ValueError("recipe %s is missing output" % recipe_id)

        inputs = recipe["inputs"]
        output = recipe["output"]
        _validate_item_counts(inputs, "inputs", allow_empty=True)
        _validate_item_counts(output, "output", allow_empty=False)

        recipe_map[recipe_id] = recipe

    return recipe_map


def _validate_acyclic(recipe_map):
    producers = {}
    for recipe_id, recipe in recipe_map.items():
        for item in recipe["output"]:
            producers.setdefault(item, set()).add(recipe_id)

    graph = {}
    for recipe_id, recipe in recipe_map.items():
        dependencies = set()
        for item in recipe["inputs"]:
            dependencies.update(producers.get(item, ()))
        graph[recipe_id] = dependencies

    state = {}

    def visit(start):
        stack = [(start, iter(graph[start]))]
        state[start] = 1
        while stack:
            node, children = stack[-1]
            try:
                child = next(children)
            except StopIteration:
                state[node] = 2
                stack.pop()
                continue

            child_state = state.get(child, 0)
            if child_state == 1:
                raise ValueError("recipe dependencies contain a cycle")
            if child_state == 0:
                state[child] = 1
                stack.append((child, iter(graph[child])))

    for recipe_id in graph:
        if state.get(recipe_id, 0) == 0:
            visit(recipe_id)


def _validate_inventory(inventory):
    if not isinstance(inventory, dict):
        raise ValueError("inventory must be a dict")
    for item, count in inventory.items():
        _validate_item_name(item, "inventory")
        if not _is_non_negative_int(count):
            raise ValueError("inventory counts must be non-negative integers")


def craft(recipe_id, recipes, inventory, capacity):
    recipe_map = _build_recipe_map(recipes)
    if not isinstance(recipe_id, str) or not recipe_id.strip():
        raise ValueError("recipe_id must be a non-empty string")
    if recipe_id not in recipe_map:
        raise ValueError("unknown recipe: %s" % recipe_id)

    if not _is_non_negative_int(capacity):
        raise ValueError("capacity must be a non-negative integer")

    _validate_inventory(inventory)
    if sum(inventory.values()) > capacity:
        raise ValueError("inventory exceeds capacity")

    _validate_acyclic(recipe_map)

    recipe = recipe_map[recipe_id]
    updated = dict(inventory)

    for item, count in recipe["inputs"].items():
        available = updated.get(item, 0)
        if available < count:
            raise ValueError("insufficient material: %s" % item)
        remaining = available - count
        if remaining:
            updated[item] = remaining
        else:
            updated.pop(item, None)

    for item, count in recipe["output"].items():
        updated[item] = updated.get(item, 0) + count

    if sum(updated.values()) > capacity:
        raise ValueError("crafted inventory exceeds capacity")

    return {"inventory": updated, "crafted": recipe_id}
