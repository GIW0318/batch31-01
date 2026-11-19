def access(cache, key, capacity):
    if not isinstance(cache, list):
        raise ValueError("cache must be a list")
    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
        raise ValueError("capacity must be a positive integer")
    if not isinstance(key, str) or not key:
        raise ValueError("key must be a non-empty string")

    ordered = []
    for entry in cache:
        if not isinstance(entry, str) or not entry:
            raise ValueError("cache entries must be non-empty strings")
        if entry not in ordered:
            ordered.append(entry)

    if key in ordered:
        ordered.remove(key)
        ordered.append(key)
        return {"cache": ordered, "hit": True, "evicted": None}

    ordered.append(key)
    evicted = None
    while len(ordered) > capacity:
        evicted = ordered.pop(0)

    return {"cache": ordered, "hit": False, "evicted": evicted}
