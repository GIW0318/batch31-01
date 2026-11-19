import math


_DIRECTIONS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}


def _sort_key(node):
    if isinstance(node, str):
        return (0, node)
    if isinstance(node, int) and not isinstance(node, bool):
        return (1, node)
    return (2, type(node).__name__, repr(node))


def _validate_position(value):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError("node position must contain exactly two coordinates")

    coordinates = []
    for coordinate in value:
        if isinstance(coordinate, bool) or not isinstance(coordinate, (int, float)):
            raise ValueError("node coordinates must be numbers")
        try:
            finite = math.isfinite(coordinate)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("node coordinates must be finite numbers") from exc
        if not finite:
            raise ValueError("node coordinates must be finite numbers")
        coordinates.append(coordinate)

    return tuple(coordinates)


def _validate_nodes(nodes):
    if not isinstance(nodes, dict) or not nodes:
        raise ValueError("nodes must be a non-empty dictionary")

    parsed = {}
    occupied = set()

    for node, data in nodes.items():
        if not isinstance(data, dict):
            raise ValueError("each node must be a dictionary")
        if "pos" not in data:
            raise ValueError("each node must have a position")

        position = _validate_position(data["pos"])
        if position in occupied:
            raise ValueError("node positions must be unique")
        occupied.add(position)

        disabled = data.get("disabled", False)
        if not isinstance(disabled, bool):
            raise ValueError("node disabled flag must be a boolean")

        parsed[node] = {"pos": position, "disabled": disabled}

    return parsed


def move(nodes, current, direction):
    if not isinstance(direction, str) or direction not in _DIRECTIONS:
        raise ValueError("direction must be one of: up, down, left, right")

    parsed = _validate_nodes(nodes)

    try:
        current_exists = current in parsed
    except TypeError as exc:
        raise ValueError("current node is invalid") from exc
    if not current_exists:
        raise ValueError("current node does not exist")

    current_x, current_y = parsed[current]["pos"]
    direction_x, direction_y = _DIRECTIONS[direction]

    candidates = []
    for node, data in parsed.items():
        if node == current or data["disabled"]:
            continue

        node_x, node_y = data["pos"]
        delta_x = node_x - current_x
        delta_y = node_y - current_y

        if direction_x and (delta_x * direction_x <= 0 or delta_y != 0):
            continue
        if direction_y and (delta_y * direction_y <= 0 or delta_x != 0):
            continue

        distance = abs(delta_x) + abs(delta_y)
        candidates.append((node, distance))

    if not candidates:
        return current

    return min(candidates, key=lambda item: (item[1], _sort_key(item[0])))[0]
