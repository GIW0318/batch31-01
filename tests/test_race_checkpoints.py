import pytest

import race_checkpoints as rc

TRACK = ["start", "cp1", "cp2", "finish"]


def events():
    return [
        {"checkpoint": "start", "time": 0},
        {"checkpoint": "cp1", "time": 1000},
        {"checkpoint": "cp2", "time": 2000},
        {"checkpoint": "finish", "time": 3000},
    ]


def test_valid_lap():
    assert rc.validate_lap(events(), TRACK, 5000) == {"valid": True, "reason": "ok", "lap_time": 3000}


def test_missing_checkpoint_is_invalid():
    assert rc.validate_lap(events()[:3], TRACK, 5000)["valid"] is False


def test_out_of_order_checkpoint_is_invalid():
    e = events()
    e[1], e[2] = e[2], e[1]
    assert rc.validate_lap(e, TRACK, 5000)["valid"] is False


def test_duplicate_start_is_invalid():
    e = events()
    e.insert(1, {"checkpoint": "start", "time": 500})
    assert rc.validate_lap(e, TRACK, 5000)["valid"] is False


def test_finish_before_start_is_invalid():
    e = events()
    e[0], e[3] = e[3], e[0]
    assert rc.validate_lap(e, TRACK, 5000)["valid"] is False


def test_time_regression_is_rejected():
    e = events()
    e[2]["time"] = 500
    with pytest.raises(ValueError):
        rc.validate_lap(e, TRACK, 5000)


def test_negative_time_is_rejected():
    e = events()
    e[0]["time"] = -1
    with pytest.raises(ValueError):
        rc.validate_lap(e, TRACK, 5000)


def test_unknown_checkpoint_is_rejected():
    e = events()
    e[2]["checkpoint"] = "cp9"
    with pytest.raises(ValueError):
        rc.validate_lap(e, TRACK, 5000)


def test_empty_events_are_rejected():
    with pytest.raises(ValueError):
        rc.validate_lap([], TRACK, 5000)


def test_lap_over_max_time_is_invalid():
    assert rc.validate_lap(events(), TRACK, 2999)["valid"] is False


def test_missing_start_is_invalid():
    e = events()[1:]
    assert rc.validate_lap(e, TRACK, 5000)["valid"] is False


def test_missing_finish_is_invalid():
    e = events()[:-1]
    assert rc.validate_lap(e, TRACK, 5000)["valid"] is False


def test_duplicate_checkpoint_is_invalid():
    e = events()
    e.insert(2, {"checkpoint": "cp1", "time": 1500})
    assert rc.validate_lap(e, TRACK, 5000)["valid"] is False


def test_non_dict_event_is_rejected():
    with pytest.raises(ValueError):
        rc.validate_lap(["start"], TRACK, 5000)


def test_non_integer_time_is_rejected():
    e = events()
    e[1]["time"] = 1000.5
    with pytest.raises(ValueError):
        rc.validate_lap(e, TRACK, 5000)
