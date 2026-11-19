def validate_lap(events, checkpoints, max_time):
    if not isinstance(events, (list, tuple)) or len(events) == 0:
        raise ValueError("events must be a non-empty list")

    validated = []
    for event in events:
        if not isinstance(event, dict):
            raise ValueError("each event must be a dict")
        if "checkpoint" not in event or "time" not in event:
            raise ValueError("event must contain checkpoint and time")

        checkpoint = event["checkpoint"]
        if not isinstance(checkpoint, str) or checkpoint not in checkpoints:
            raise ValueError("unknown checkpoint: %r" % (checkpoint,))

        time = event["time"]
        if isinstance(time, bool) or not isinstance(time, int):
            raise ValueError("event time must be an integer")
        if time < 0:
            raise ValueError("event time must not be negative")
        validated.append((checkpoint, time))

    sequence = [checkpoint for checkpoint, _ in validated]
    if sequence != list(checkpoints):
        return {
            "valid": False,
            "reason": "checkpoints must be complete and pass in track order exactly once",
            "lap_time": None,
        }

    for (_, previous_time), (_, current_time) in zip(validated, validated[1:]):
        if current_time <= previous_time:
            raise ValueError("event times must be strictly increasing")

    lap_time = validated[-1][1] - validated[0][1]
    if lap_time > max_time:
        return {
            "valid": False,
            "reason": "lap time %d exceeds max time %d" % (lap_time, max_time),
            "lap_time": lap_time,
        }

    return {"valid": True, "reason": "ok", "lap_time": lap_time}
