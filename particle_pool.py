def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _validate_ids(ids):
    if not all(_is_int(particle_id) for particle_id in ids):
        raise ValueError("particle ids must be integers")


def transact(pool, acquire=0, release=None, capacity=10):
    if not isinstance(pool, dict):
        raise ValueError("pool must be a dict")

    free = pool.get("free")
    active = pool.get("active")
    if not isinstance(free, list) or not isinstance(active, list):
        raise ValueError("free and active must be lists")

    if not _is_int(capacity) or capacity <= 0:
        raise ValueError("capacity must be a positive integer")
    if not _is_int(acquire) or acquire < 0:
        raise ValueError("acquire must be a non-negative integer")

    if release is None:
        release = []
    elif not isinstance(release, list):
        raise ValueError("release must be a list")

    free = list(free)
    active = list(active)

    _validate_ids(free)
    _validate_ids(active)
    _validate_ids(release)

    free_ids = set(free)
    active_ids = set(active)
    if len(free_ids) != len(free) or len(active_ids) != len(active):
        raise ValueError("particle ids must be unique")
    if free_ids & active_ids:
        raise ValueError("free and active particle ids must not overlap")
    if len(free) + len(active) > capacity:
        raise ValueError("pool exceeds capacity")

    released_ids = set()
    for particle_id in release:
        if particle_id in released_ids:
            raise ValueError("duplicate release id")
        if particle_id not in active_ids:
            raise ValueError("cannot release an inactive particle id")
        released_ids.add(particle_id)

    active = [
        particle_id for particle_id in active if particle_id not in released_ids
    ]
    free.extend(release)

    new_ids = max(free + active, default=0) + 1
    total = len(free) + len(active)
    for _ in range(acquire):
        if free:
            active.append(free.pop())
        else:
            if total >= capacity:
                raise ValueError("acquire would exceed capacity")
            active.append(new_ids)
            new_ids += 1
            total += 1

    return {"free": free, "active": active}
