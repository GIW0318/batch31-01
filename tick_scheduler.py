def schedule(tasks, tick_budget):
    if not isinstance(tasks, list):
        raise ValueError("tasks must be a list")
    if not isinstance(tick_budget, (int, float)) or isinstance(tick_budget, bool):
        raise ValueError("tick_budget must be a number")
    if tick_budget < 0:
        raise ValueError("tick_budget must be non-negative")

    seen_ids = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("each task must be a dict")
        if "id" not in task:
            raise ValueError("task is missing 'id'")
        if "cost" not in task:
            raise ValueError("task is missing 'cost'")
        cost = task["cost"]
        if not isinstance(cost, (int, float)) or isinstance(cost, bool) or cost <= 0:
            raise ValueError("task cost must be a positive number")
        if task["id"] in seen_ids:
            raise ValueError("duplicate task id: %r" % (task["id"],))
        seen_ids.add(task["id"])

    active = [t for t in tasks if not t.get("cancelled", False)]
    ordered = sorted(active, key=lambda t: (t.get("deadline", 0), t.get("priority", 0)))

    ran = []
    deferred = []
    remaining = tick_budget
    for task in ordered:
        if task["cost"] <= remaining:
            ran.append(task["id"])
            remaining -= task["cost"]
        else:
            deferred.append(task["id"])

    return {"ran": ran, "deferred": deferred, "overrun": bool(deferred)}
