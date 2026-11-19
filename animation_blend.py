CLIPS = {"idle": 1.0, "run": 0.8, "attack": 0.5}


def _validate_state(state):
    if not isinstance(state, dict):
        raise ValueError("state must be a dict")
    if "current" not in state:
        raise ValueError("state is missing 'current'")
    if state["current"] not in CLIPS:
        raise ValueError(f"unknown clip: {state['current']!r}")


def blend(state, event):
    _validate_state(state)
    if not isinstance(event, dict) or "type" not in event:
        raise ValueError("event must be a dict with a 'type'")

    out = dict(state)
    out["root"] = list(state.get("root", [0.0, 0.0]))
    kind = event["type"]

    if kind == "play":
        clip = event.get("clip")
        if clip not in CLIPS:
            raise ValueError(f"unknown clip: {clip!r}")
        out["current"] = clip
        out["time"] = 0.0
    elif kind == "advance":
        dt = event.get("dt")
        if not isinstance(dt, (int, float)) or dt < 0:
            raise ValueError("dt must be a non-negative number")
        if not out.get("paused", False):
            speed = out.get("speed", 1.0)
            if speed <= 0:
                raise ValueError("speed must be positive")
            out["time"] = (out.get("time", 0.0) + dt * speed) % CLIPS[out["current"]]
    elif kind == "set_speed":
        speed = event.get("speed")
        if not isinstance(speed, (int, float)) or speed <= 0:
            raise ValueError("speed must be a positive number")
        out["speed"] = speed
    elif kind == "root":
        delta = event.get("delta")
        if (
            not isinstance(delta, (list, tuple))
            or len(delta) != 2
            or not all(isinstance(v, (int, float)) for v in delta)
        ):
            raise ValueError("delta must be a pair of numbers")
        out["root"] = [out["root"][0] + delta[0], out["root"][1] + delta[1]]
    elif kind == "interrupt":
        clip = event.get("clip")
        if clip not in CLIPS:
            raise ValueError(f"unknown clip: {clip!r}")
        priority = event.get("priority", 0)
        if priority >= out.get("priority", 0):
            out["current"] = clip
            out["time"] = 0.0
            out["priority"] = priority
    elif kind == "pause":
        out["paused"] = True
    elif kind == "resume":
        out["paused"] = False
    elif kind == "blend":
        weight = event.get("weight")
        if not isinstance(weight, (int, float)):
            raise ValueError("weight must be a number")
        out["weight"] = min(1.0, max(0.0, weight))
    else:
        raise ValueError(f"unknown event type: {kind!r}")

    return out
