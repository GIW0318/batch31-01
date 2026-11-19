import numbers


KIND_PRIORITY = {"enemy": 0, "prop": 1}


def _is_real_number(value):
    return isinstance(value, numbers.Real) and not isinstance(value, bool)


def _valid_position(pos):
    if not isinstance(pos, (list, tuple)) or len(pos) != 2:
        return False
    return all(_is_real_number(coord) for coord in pos)


def select(entities, player, budget, stale_after=5000):
    if not isinstance(entities, list):
        raise ValueError("entities must be a list")

    if not isinstance(player, dict) or not _valid_position(player.get("pos")):
        raise ValueError("player must have a valid position")

    if not isinstance(budget, int) or isinstance(budget, bool) or budget < 0:
        raise ValueError("budget must be a non-negative integer")

    if not _is_real_number(stale_after) or stale_after < 0:
        raise ValueError("stale_after must be a non-negative number")

    now = player.get("now")
    if not _is_real_number(now):
        raise ValueError("player.now must be a number")

    seen_ids = []
    for entity in entities:
        if not isinstance(entity, dict):
            raise ValueError("each entity must be a dict")
        if "id" not in entity:
            raise ValueError("each entity must have an id")
        entity_id = entity["id"]
        if entity_id in seen_ids:
            raise ValueError("duplicate entity id: %r" % (entity_id,))
        seen_ids.append(entity_id)
        if not _valid_position(entity.get("pos")):
            raise ValueError("entity %r has an invalid position" % (entity_id,))
        last_seen = entity.get("last_seen")
        if not _is_real_number(last_seen):
            raise ValueError("entity %r has an invalid last_seen" % (entity_id,))

    player_x, player_y = player["pos"]

    candidates = []
    for entity in entities:
        if now - entity["last_seen"] > stale_after:
            continue
        entity_x, entity_y = entity["pos"]
        distance_sq = (entity_x - player_x) ** 2 + (entity_y - player_y) ** 2
        priority = KIND_PRIORITY.get(entity.get("kind"), len(KIND_PRIORITY))
        candidates.append((priority, distance_sq, entity["id"], entity))

    candidates.sort(key=lambda item: (item[0], item[1], item[2]))
    return [item[2] for item in candidates[:budget]]
