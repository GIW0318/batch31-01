PITY_THRESHOLD = 10


def roll(table, ticket, pity=0):
    if not table:
        raise ValueError("loot table must not be empty")

    seen_ids = set()
    total_weight = 0
    for entry in table:
        entry_id = entry.get("id")
        weight = entry.get("weight")
        rarity = entry.get("rarity")
        if entry_id is None or rarity is None:
            raise ValueError("loot entry is missing required fields")
        if not isinstance(weight, int) or isinstance(weight, bool) or weight < 0:
            raise ValueError("loot entry has an invalid weight")
        if entry_id in seen_ids:
            raise ValueError("duplicate loot id: %r" % (entry_id,))
        seen_ids.add(entry_id)
        total_weight += weight

    if not isinstance(ticket, int) or isinstance(ticket, bool):
        raise ValueError("ticket must be an integer")
    if ticket < 0 or ticket >= total_weight:
        raise ValueError("ticket %d is outside the weight range [0, %d)" % (ticket, total_weight))

    if pity >= PITY_THRESHOLD:
        forced_epic = next((entry for entry in table if entry["rarity"] == "epic"), None)
        if forced_epic is not None:
            return {"id": forced_epic["id"], "rarity": forced_epic["rarity"], "pity": 0}

    cumulative = 0
    for entry in table:
        cumulative += entry["weight"]
        if ticket < cumulative:
            next_pity = pity + 1 if entry["rarity"] == "common" else 0
            return {"id": entry["id"], "rarity": entry["rarity"], "pity": next_pity}

    raise ValueError("ticket %d could not be matched to a loot entry" % ticket)
