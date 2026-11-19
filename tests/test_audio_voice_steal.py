import pytest

import audio_voice_steal as av

VOICES = [
    {"id": "a", "priority": 3, "start": 0, "protected": False},
    {"id": "b", "priority": 1, "start": 1, "protected": False},
    {"id": "c", "priority": 2, "start": 2, "protected": False},
]


def test_keeps_top_priority():
    assert av.select(VOICES, 1) == {"keep": ["a"], "steal": ["b", "c"]}


def test_limit_zero_steals_all():
    assert av.select(VOICES, 0) == {"keep": [], "steal": ["a", "b", "c"]}


def test_negative_limit_is_rejected():
    with pytest.raises(ValueError):
        av.select(VOICES, -1)


def test_duplicate_id_is_rejected():
    with pytest.raises(ValueError):
        av.select([VOICES[0], dict(VOICES[0])], 2)


def test_invalid_priority_is_rejected():
    with pytest.raises(ValueError):
        av.select([{"id": "x", "priority": 1.5, "start": 0, "protected": False}], 1)


def test_missing_id_is_rejected():
    with pytest.raises(ValueError):
        av.select([{"priority": 1, "start": 0, "protected": False}], 1)


def test_missing_priority_is_rejected():
    with pytest.raises(ValueError):
        av.select([{"id": "x", "start": 0, "protected": False}], 1)


def test_negative_start_is_rejected():
    with pytest.raises(ValueError):
        av.select([{"id": "x", "priority": 1, "start": -1, "protected": False}], 1)


def test_protected_voice_is_kept():
    voices = [{"id": "p", "priority": 1, "start": 9, "protected": True}, {"id": "q", "priority": 9, "start": 0, "protected": False}]
    assert av.select(voices, 1) == {"keep": ["p"], "steal": ["q"]}


def test_equal_priority_oldest_is_kept():
    voices = [{"id": "old", "priority": 1, "start": 0, "protected": False}, {"id": "new", "priority": 1, "start": 1, "protected": False}]
    assert av.select(voices, 1)["keep"] == ["old"]


def test_voices_must_be_list():
    with pytest.raises(ValueError):
        av.select({"id": "a"}, 1)


def test_voice_must_be_dict():
    with pytest.raises(ValueError):
        av.select(["a"], 1)


def test_limit_above_count_keeps_all():
    assert av.select(VOICES, 10) == {"keep": ["a", "c", "b"], "steal": []}


def test_keep_and_steal_do_not_overlap():
    out = av.select(VOICES, 2)
    assert not (set(out["keep"]) & set(out["steal"]))


def test_select_is_deterministic():
    expected = {"keep": ["a", "c"], "steal": ["b"]}
    assert av.select(VOICES, 2) == expected
    assert av.select(VOICES, 2) == av.select(VOICES, 2)
