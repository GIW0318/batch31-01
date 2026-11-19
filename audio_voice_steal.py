def _require_int(value, name):
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer")
    return value


def select(voices, limit):
    if not isinstance(voices, list):
        raise ValueError("voices must be a list")
    if type(limit) is not int or limit < 0:
        raise ValueError("limit must be a non-negative integer")

    seen_ids = set()
    prepared = []
    for index, voice in enumerate(voices):
        if not isinstance(voice, dict):
            raise ValueError(f"voice at index {index} must be a dict")

        if "id" not in voice:
            raise ValueError(f"voice at index {index} is missing id")
        voice_id = voice["id"]
        if not isinstance(voice_id, str) or not voice_id:
            raise ValueError(f"voice at index {index} has an invalid id")
        if voice_id in seen_ids:
            raise ValueError(f"duplicate voice id: {voice_id}")
        seen_ids.add(voice_id)

        if "priority" not in voice:
            raise ValueError(f"voice {voice_id} is missing priority")
        priority = _require_int(voice["priority"], f"voice {voice_id} priority")
        if priority < 0:
            raise ValueError(f"voice {voice_id} has a negative priority")

        if "start" not in voice:
            raise ValueError(f"voice {voice_id} is missing start")
        start = _require_int(voice["start"], f"voice {voice_id} start")
        if start < 0:
            raise ValueError(f"voice {voice_id} has a negative start")

        protected = voice.get("protected", False)
        if type(protected) is not bool:
            raise ValueError(f"voice {voice_id} protected must be a boolean")

        prepared.append((voice_id, priority, start, protected, index))

    ranked = sorted(
        prepared,
        key=lambda item: (not item[3], -item[1], item[2], item[4]),
    )
    kept_ids = {item[0] for item in ranked[:limit]}

    keep = [item[0] for item in ranked[:limit]]
    steal = [item[0] for item in prepared if item[0] not in kept_ids]
    return {"keep": keep, "steal": steal}
