VALID_STATUSES = frozenset({"locked", "available", "active", "completed", "failed"})
VALID_EVENTS = frozenset({"accept", "progress", "choose", "complete", "fail", "reset"})


def _canonical_state(state):
    if not isinstance(state, dict):
        raise ValueError("state must be a dictionary")

    required = {"id", "status", "steps", "branch", "rewards", "version"}
    if not required.issubset(state):
        raise ValueError("state is missing required fields")

    status = state["status"]
    if not isinstance(status, str) or status not in VALID_STATUSES:
        raise ValueError("unknown quest status")

    steps = state["steps"]
    if not isinstance(steps, (list, tuple)):
        raise ValueError("steps must be a sequence")
    if any(not isinstance(done, bool) for done in steps):
        raise ValueError("steps must contain booleans")

    branch = state["branch"]
    if branch is not None and (not isinstance(branch, str) or not branch):
        raise ValueError("branch must be None or a non-empty string")

    rewards = state["rewards"]
    if not isinstance(rewards, (list, tuple)):
        raise ValueError("rewards must be a sequence")

    version = state["version"]
    if isinstance(version, bool) or not isinstance(version, int) or version < 0:
        raise ValueError("version must be a non-negative integer")

    return {
        "id": state["id"],
        "status": status,
        "steps": list(steps),
        "branch": branch,
        "rewards": list(rewards),
        "version": version,
    }


def _require_status(state, allowed):
    if state["status"] not in allowed:
        raise ValueError(
            f"event is not allowed while quest is {state['status']}"
        )


def transition(state, event):
    current = _canonical_state(state)

    if not isinstance(event, dict):
        raise ValueError("event must be a dictionary")

    event_type = event.get("type")
    if not isinstance(event_type, str) or event_type not in VALID_EVENTS:
        raise ValueError("unknown event type")

    if event_type == "accept":
        _require_status(current, {"available"})
        current["status"] = "active"

    elif event_type == "progress":
        _require_status(current, {"active"})

        step = event.get("step")
        if isinstance(step, bool) or not isinstance(step, int):
            raise ValueError("step must be an integer")
        if step < 0 or step >= len(current["steps"]):
            raise ValueError("step is out of range")
        if current["steps"][step]:
            raise ValueError("step has already been completed")
        if not all(current["steps"][:step]):
            raise ValueError("steps must be completed in order")

        current["steps"][step] = True

    elif event_type == "choose":
        _require_status(current, {"active"})
        if current["branch"] is not None:
            raise ValueError("branch has already been chosen")

        choice = event.get("choice")
        if not isinstance(choice, str) or not choice:
            raise ValueError("choice must be a non-empty string")
        current["branch"] = choice

    elif event_type == "complete":
        if current["status"] == "completed":
            return current

        _require_status(current, {"active"})
        if not all(current["steps"]):
            raise ValueError("all steps must be completed first")

        current["status"] = "completed"
        if "xp" not in current["rewards"]:
            current["rewards"].append("xp")

    elif event_type == "fail":
        _require_status(current, {"active"})
        current["status"] = "failed"

    elif event_type == "reset":
        _require_status(current, {"active"})
        current["status"] = "available"
        current["steps"] = [False] * len(current["steps"])
        current["branch"] = None
        current["rewards"] = []

    current["version"] += 1
    return current
