MAX_CHORD_SIZE = 2

RESERVED_BUTTONS = frozenset({"guide", "home"})


def _normalize(value):
    if not isinstance(value, str):
        raise ValueError(f"button must be a string, got {type(value).__name__}")
    return value.casefold()


def validate_mapping(bindings, actions):
    if not isinstance(bindings, list):
        raise ValueError("bindings must be a list of binding dicts")

    allowed_actions = frozenset(actions)
    seen_actions = set()
    seen_combos = set()
    mapping = {}

    for binding in bindings:
        if not isinstance(binding, dict):
            raise ValueError(f"each binding must be a dict, got {type(binding).__name__}")

        action = binding.get("action")
        if action is None:
            raise ValueError("binding is missing required 'action'")
        if action not in allowed_actions:
            raise ValueError(f"unknown action: {action!r}")
        if action in seen_actions:
            raise ValueError(f"action is bound more than once: {action!r}")

        button = binding.get("button")
        if button is None:
            raise ValueError("binding is missing required 'button'")
        normalized_button = _normalize(button)
        if not normalized_button:
            raise ValueError("button must not be empty")
        if normalized_button in RESERVED_BUTTONS:
            raise ValueError(f"reserved button cannot be mapped: {button!r}")

        chord = binding.get("chord", [])
        if not isinstance(chord, list):
            raise ValueError("chord must be a list of buttons")
        if len(chord) > MAX_CHORD_SIZE:
            raise ValueError(
                f"chord may contain at most {MAX_CHORD_SIZE} buttons, got {len(chord)}"
            )

        normalized_chord = []
        for chord_button in chord:
            normalized_chord_button = _normalize(chord_button)
            if not normalized_chord_button:
                raise ValueError("chord button must not be empty")
            if normalized_chord_button in RESERVED_BUTTONS:
                raise ValueError(
                    f"reserved button cannot be used in chord: {chord_button!r}"
                )
            normalized_chord.append(normalized_chord_button)

        if normalized_button in normalized_chord:
            raise ValueError(f"chord must not repeat the main button: {button!r}")
        if len(set(normalized_chord)) != len(normalized_chord):
            raise ValueError(f"chord contains duplicate buttons: {chord!r}")

        combo = (normalized_button, frozenset(normalized_chord))
        if combo in seen_combos:
            raise ValueError(
                f"button {button!r} with chord {chord!r} is already bound to another action"
            )

        seen_actions.add(action)
        seen_combos.add(combo)
        mapping[action] = {"button": button, "chord": chord}

    return mapping
