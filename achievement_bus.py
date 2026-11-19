def _validate_event(event):
    if not isinstance(event, dict):
        raise ValueError("event must be a dict")

    event_type = event.get("type")
    if not isinstance(event_type, str) or not event_type:
        raise ValueError("event type is required")

    count = event.get("count", 1)
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise ValueError("event count must be a non-negative integer")

    return event_type, count


def _validate_rules(rules):
    if not isinstance(rules, list):
        raise ValueError("rules must be a list")

    validated = []
    seen_ids = set()
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError("each rule must be a dict")

        rule_id = rule.get("id")
        event_type = rule.get("event")
        count = rule.get("count")
        reward = rule.get("reward")

        if not isinstance(rule_id, str) or not rule_id:
            raise ValueError("rule id is required")
        if rule_id in seen_ids:
            raise ValueError("rule ids must be unique")
        if not isinstance(event_type, str) or not event_type:
            raise ValueError("rule event is required")
        if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
            raise ValueError("rule count must be a positive integer")
        if not isinstance(reward, str) or not reward:
            raise ValueError("rule reward is required")

        seen_ids.add(rule_id)
        validated.append(rule)

    return validated


def _validate_state(state):
    if not isinstance(state, dict):
        raise ValueError("state must be a dict")

    counts = state.get("counts", {})
    unlocked = state.get("unlocked", [])
    delivered = state.get("delivered", [])

    if not isinstance(counts, dict):
        raise ValueError("state counts must be a dict")
    if not isinstance(unlocked, list):
        raise ValueError("state unlocked must be a list")
    if not isinstance(delivered, list):
        raise ValueError("state delivered must be a list")
    for rule_id, count in counts.items():
        if not isinstance(rule_id, str):
            raise ValueError("state count keys must be strings")
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ValueError("state counts must be non-negative integers")

    return counts, unlocked, delivered


def process(event, rules, state):
    event_type, event_count = _validate_event(event)
    rules = _validate_rules(rules)
    counts, unlocked, delivered = _validate_state(state)

    counts = dict(counts)
    unlocked = list(unlocked)
    delivered = list(delivered)

    known_events = {rule["event"] for rule in rules}
    if event_type not in known_events:
        return {"counts": counts, "unlocked": unlocked, "delivered": delivered}

    for rule in rules:
        if rule["event"] != event_type:
            continue

        rule_id = rule["id"]
        current = counts.get(rule_id, 0)
        counts[rule_id] = current + event_count

        if rule_id not in unlocked and counts[rule_id] >= rule["count"]:
            unlocked.append(rule_id)
            if rule["reward"] not in delivered:
                delivered.append(rule["reward"])

    return {"counts": counts, "unlocked": unlocked, "delivered": delivered}
