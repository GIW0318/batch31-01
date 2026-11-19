import pytest

import movement_anticheat as ma

CONFIG = {"max_speed": 10, "lag_window": 2000}


def prev(**overrides):
    data = {"pos": [0, 0], "time": 0}
    data.update(overrides)
    return data


def move(**overrides):
    data = {"pos": [10, 0], "time": 1000}
    data.update(overrides)
    return data


def test_valid_move():
    assert ma.validate_move(prev(), move(), CONFIG) == {"ok": True, "reason": "ok"}


def test_too_fast_move_is_rejected():
    assert ma.validate_move(prev(), move(pos=[30, 0], time=1000), CONFIG)["ok"] is False


def test_teleport_is_rejected():
    assert ma.validate_move(prev(), move(pos=[1000, 0], time=1000), CONFIG)["reason"] == "teleport"


def test_equal_time_is_rejected():
    with pytest.raises(ValueError):
        ma.validate_move(prev(), move(time=0), CONFIG)


def test_time_regression_is_rejected():
    with pytest.raises(ValueError):
        ma.validate_move(prev(time=1000), move(time=500), CONFIG)


def test_negative_time_is_rejected():
    with pytest.raises(ValueError):
        ma.validate_move(prev(time=-1), move(), CONFIG)


def test_missing_axis_is_rejected():
    with pytest.raises(ValueError):
        ma.validate_move(prev(), move(pos=[1]), CONFIG)


def test_string_position_is_rejected():
    with pytest.raises(ValueError):
        ma.validate_move(prev(), move(pos=["1", "2"]), CONFIG)


def test_zero_max_speed_is_rejected():
    with pytest.raises(ValueError):
        ma.validate_move(prev(), move(), {"max_speed": 0, "lag_window": 2000})


def test_negative_max_speed_is_rejected():
    with pytest.raises(ValueError):
        ma.validate_move(prev(), move(), {"max_speed": -1, "lag_window": 2000})


def test_lag_window_is_enforced():
    assert ma.validate_move(prev(), move(time=5000), {"max_speed": 10, "lag_window": 2000})["reason"] == "lag"


def test_diagonal_distance_is_euclidean():
    assert ma.validate_move(prev(), move(pos=[3, 4], time=1000), CONFIG)["ok"] is True


def test_nan_position_is_rejected():
    with pytest.raises(ValueError):
        ma.validate_move(prev(), move(pos=[float("nan"), 0]), CONFIG)


def test_move_must_be_dict():
    with pytest.raises(ValueError):
        ma.validate_move(prev(), [], CONFIG)


def test_boundary_speed_is_allowed():
    assert ma.validate_move(prev(), move(pos=[10, 0], time=1000), CONFIG)["ok"] is True
