import pytest

import buoyancy as by

BODY = {"mass": 500, "volume": 1, "submerged": 1}
WATER = {"density": 1000, "gravity": 10}


def body(**overrides):
    data = dict(BODY)
    data.update(overrides)
    return data


def water(**overrides):
    data = dict(WATER)
    data.update(overrides)
    return data


def test_fully_submerged_net_force():
    assert by.compute(BODY, WATER) == {"buoyant": 10000, "weight": 5000, "net": 5000}


def test_half_submerged_net_force():
    assert by.compute(body(submerged=0.5), WATER) == {"buoyant": 5000, "weight": 5000, "net": 0}


def test_above_water_has_no_buoyancy():
    assert by.compute(body(submerged=0), WATER) == {"buoyant": 0, "weight": 5000, "net": -5000}


def test_submerged_above_volume_is_rejected():
    with pytest.raises(ValueError):
        by.compute(body(submerged=2), WATER)


def test_negative_mass_is_rejected():
    with pytest.raises(ValueError):
        by.compute(body(mass=-1), WATER)


def test_zero_mass_is_rejected():
    with pytest.raises(ValueError):
        by.compute(body(mass=0), WATER)


def test_zero_density_is_rejected():
    with pytest.raises(ValueError):
        by.compute(BODY, water(density=0))


def test_negative_density_is_rejected():
    with pytest.raises(ValueError):
        by.compute(BODY, water(density=-1))


def test_zero_gravity_is_rejected():
    with pytest.raises(ValueError):
        by.compute(BODY, water(gravity=0))


def test_missing_mass_is_rejected():
    with pytest.raises(ValueError):
        by.compute({"volume": 1, "submerged": 1}, WATER)


def test_missing_volume_is_rejected():
    with pytest.raises(ValueError):
        by.compute({"mass": 500, "submerged": 1}, WATER)


def test_non_dict_body_is_rejected():
    with pytest.raises(ValueError):
        by.compute([], WATER)


def test_non_dict_water_is_rejected():
    with pytest.raises(ValueError):
        by.compute(BODY, [])


def test_negative_submerged_is_rejected():
    with pytest.raises(ValueError):
        by.compute(body(submerged=-1), WATER)


def test_zero_submerged_boundary():
    assert by.compute(body(submerged=0), WATER)["buoyant"] == 0
