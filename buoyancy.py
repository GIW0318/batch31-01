import math
import numbers


def _number(container, field):
    if not isinstance(container, dict) or field not in container:
        raise ValueError(f"missing field: {field}")

    value = container[field]
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise ValueError(f"{field} must be a number")
    if not math.isfinite(value):
        raise ValueError(f"{field} must be finite")
    return value


def compute(body, water):
    if not isinstance(body, dict):
        raise ValueError("body must be a dict")
    if not isinstance(water, dict):
        raise ValueError("water must be a dict")

    mass = _number(body, "mass")
    volume = _number(body, "volume")
    submerged = _number(body, "submerged")
    density = _number(water, "density")
    gravity = _number(water, "gravity")

    if mass <= 0:
        raise ValueError("mass must be positive")
    if volume <= 0:
        raise ValueError("volume must be positive")
    if density <= 0:
        raise ValueError("density must be positive")
    if gravity <= 0:
        raise ValueError("gravity must be positive")
    if submerged < 0 or submerged > volume:
        raise ValueError("submerged must be between 0 and volume")

    buoyant = submerged * density * gravity
    weight = mass * gravity
    return {"buoyant": buoyant, "weight": weight, "net": buoyant - weight}
