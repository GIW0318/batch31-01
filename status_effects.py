def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate_state(state):
    if not isinstance(state, dict):
        raise ValueError("state must be a dict")
    if "active" in state and not isinstance(state["active"], dict):
        raise ValueError("state['active'] must be a dict")
    if "immunities" in state and not isinstance(state["immunities"], list):
        raise ValueError("state['immunities'] must be a list")


def _copy_state(state):
    active = state.get("active", {})
    new_state = dict(state)
    new_state["active"] = {key: dict(entry) for key, entry in active.items()}
    new_state["immunities"] = list(state.get("immunities", []))
    return new_state


def apply_effect(state, effect):
    _validate_state(state)
    if not isinstance(effect, dict):
        raise ValueError("effect must be a dict")

    effect_id = effect.get("id")
    if not isinstance(effect_id, str) or not effect_id:
        raise ValueError("effect 'id' must be a non-empty string")

    if "duration" not in effect:
        raise ValueError("effect 'duration' is required")
    duration = effect["duration"]
    if not _is_number(duration) or duration < 0:
        raise ValueError("effect 'duration' must be a non-negative number")

    if "max_stacks" not in effect:
        raise ValueError("effect 'max_stacks' is required")
    max_stacks = effect["max_stacks"]
    if not isinstance(max_stacks, int) or isinstance(max_stacks, bool) or max_stacks <= 0:
        raise ValueError("effect 'max_stacks' must be a positive integer")

    if effect_id in state.get("immunities", []):
        return _copy_state(state)

    new_state = _copy_state(state)
    active = new_state["active"]

    if effect_id in active:
        entry = active[effect_id]
        entry["stacks"] = min(entry["stacks"] + 1, max_stacks)
        if effect.get("refresh", True):
            entry["remaining"] = duration
    else:
        active[effect_id] = {"stacks": 1, "remaining": duration}

    return new_state


def tick(state, dt):
    _validate_state(state)
    if not _is_number(dt) or dt < 0:
        raise ValueError("dt must be a non-negative number")

    active = {}
    for effect_id in sorted(state.get("active", {})):
        entry = state["active"][effect_id]
        remaining = entry["remaining"] - dt
        if remaining > 0:
            active[effect_id] = {"stacks": entry["stacks"], "remaining": remaining}

    new_state = dict(state)
    new_state["active"] = active
    new_state["immunities"] = list(state.get("immunities", []))
    return new_state
