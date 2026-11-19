import math
import numbers


def _require_mapping(value, name):
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a dict")
    return value


def _require_number(value, name):
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise ValueError(f"{name} must be a number")

    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _require_position(value, name):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"{name} must contain exactly two axes")
    return tuple(_require_number(axis, f"{name}[{index}]") for index, axis in enumerate(value))


def _require_time(value, name):
    timestamp = _require_number(value, name)
    if timestamp < 0:
        raise ValueError(f"{name} must not be negative")
    return timestamp


def _require_config(config):
    config = _require_mapping(config, "config")

    try:
        max_speed = _require_number(config["max_speed"], "max_speed")
        lag_window = _require_number(config["lag_window"], "lag_window")
    except KeyError as exc:
        raise ValueError(f"config is missing {exc.args[0]}") from exc

    if max_speed <= 0:
        raise ValueError("max_speed must be greater than zero")
    if lag_window <= 0:
        raise ValueError("lag_window must be greater than zero")

    return max_speed, lag_window


def validate_move(prev, move, config):
    prev = _require_mapping(prev, "prev")
    move = _require_mapping(move, "move")
    max_speed, lag_window = _require_config(config)

    try:
        prev_pos = _require_position(prev["pos"], "prev.pos")
        move_pos = _require_position(move["pos"], "move.pos")
        prev_time = _require_time(prev["time"], "prev.time")
        move_time = _require_time(move["time"], "move.time")
    except KeyError as exc:
        raise ValueError(f"missing field {exc.args[0]}") from exc

    if move_time <= prev_time:
        raise ValueError("move time must be greater than previous time")

    elapsed_ms = move_time - prev_time
    if elapsed_ms > lag_window:
        return {"ok": False, "reason": "lag"}

    distance = math.hypot(move_pos[0] - prev_pos[0], move_pos[1] - prev_pos[1])
    speed = distance / (elapsed_ms / 1000.0)

    if speed > max_speed:
        if speed > max_speed * 10:
            return {"ok": False, "reason": "teleport"}
        return {"ok": False, "reason": "speed"}

    return {"ok": True, "reason": "ok"}
