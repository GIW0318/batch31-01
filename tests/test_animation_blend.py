import pytest

import animation_blend as ab

STATE = {"current": "idle", "time": 0.0, "speed": 1.0, "root": [0.0, 0.0], "paused": False}
CLIPS = {"idle": 1.0, "run": 0.8, "attack": 0.5}


def state(**overrides):
    data = {"current": "idle", "time": 0.0, "speed": 1.0, "root": [0.0, 0.0], "paused": False}
    data.update(overrides)
    return data


def test_play_resets_time():
    assert ab.blend(state(time=0.5), {"type": "play", "clip": "run"}) == {
        "current": "run", "time": 0.0, "speed": 1.0, "root": [0.0, 0.0], "paused": False,
    }


def test_advance_increases_time():
    assert ab.blend(state(), {"type": "advance", "dt": 0.2})["time"] == 0.2


def test_negative_advance_is_rejected():
    with pytest.raises(ValueError):
        ab.blend(state(), {"type": "advance", "dt": -1})


def test_speed_scales_time():
    assert ab.blend(state(speed=2.0), {"type": "advance", "dt": 0.2})["time"] == 0.4


def test_zero_speed_is_rejected():
    with pytest.raises(ValueError):
        ab.blend(state(), {"type": "set_speed", "speed": 0})


def test_loop_wraps_time():
    out = ab.blend(state(current="run", time=0.7), {"type": "advance", "dt": 0.2})
    assert round(out["time"], 3) == 0.1


def test_root_motion_accumulates():
    assert ab.blend(state(), {"type": "root", "delta": [1.0, 2.0]})["root"] == [1.0, 2.0]


def test_interrupt_priority():
    assert ab.blend(state(current="run"), {"type": "interrupt", "clip": "attack", "priority": 5})["current"] == "attack"


def test_pause_blocks_advance():
    assert ab.blend(state(paused=True), {"type": "advance", "dt": 1})["time"] == 0.0


def test_resume_keeps_time():
    assert ab.blend(state(paused=True, time=0.4), {"type": "resume"})["time"] == 0.4


def test_unknown_clip_is_rejected():
    with pytest.raises(ValueError):
        ab.blend(state(), {"type": "play", "clip": "ghost"})


def test_state_must_be_dict():
    with pytest.raises(ValueError):
        ab.blend([], {"type": "advance", "dt": 0})


def test_missing_current_is_rejected():
    with pytest.raises(ValueError):
        ab.blend({"time": 0}, {"type": "advance", "dt": 0})


def test_blend_weight_is_clamped():
    assert ab.blend(state(), {"type": "blend", "weight": 2}) == {
        "current": "idle", "time": 0.0, "speed": 1.0, "root": [0.0, 0.0], "paused": False, "weight": 1.0,
    }


def test_unknown_event_is_rejected():
    with pytest.raises(ValueError):
        ab.blend(state(), {"type": "teleport"})
