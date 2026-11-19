import pytest

import loot_table as lt

TABLE = [
    {"id": "common", "weight": 70, "rarity": "common"},
    {"id": "rare", "weight": 25, "rarity": "rare"},
    {"id": "epic", "weight": 5, "rarity": "epic"},
]


def test_ticket_zero_is_first_item():
    assert lt.roll(TABLE, 0) == {"id": "common", "rarity": "common", "pity": 1}


def test_ticket_69_is_common():
    assert lt.roll(TABLE, 69) == {"id": "common", "rarity": "common", "pity": 1}


def test_ticket_70_is_rare():
    assert lt.roll(TABLE, 70) == {"id": "rare", "rarity": "rare", "pity": 0}


def test_ticket_94_is_rare():
    assert lt.roll(TABLE, 94) == {"id": "rare", "rarity": "rare", "pity": 0}


def test_ticket_95_is_epic():
    assert lt.roll(TABLE, 95) == {"id": "epic", "rarity": "epic", "pity": 0}


def test_ticket_99_is_epic():
    assert lt.roll(TABLE, 99) == {"id": "epic", "rarity": "epic", "pity": 0}


def test_ticket_100_is_rejected():
    with pytest.raises(ValueError):
        lt.roll(TABLE, 100)


def test_negative_ticket_is_rejected():
    with pytest.raises(ValueError):
        lt.roll(TABLE, -1)


def test_empty_table_is_rejected():
    with pytest.raises(ValueError):
        lt.roll([], 0)


def test_negative_weight_is_rejected():
    with pytest.raises(ValueError):
        lt.roll([{"id": "bad", "weight": -1, "rarity": "common"}], 0)


def test_duplicate_ids_are_rejected():
    with pytest.raises(ValueError):
        lt.roll([{"id": "same", "weight": 1, "rarity": "common"}, {"id": "same", "weight": 1, "rarity": "rare"}], 0)


def test_pity_threshold_forces_epic():
    assert lt.roll(TABLE, 0, pity=10) == {"id": "epic", "rarity": "epic", "pity": 0}


def test_pity_below_threshold_does_not_force():
    assert lt.roll(TABLE, 0, pity=9) == {"id": "common", "rarity": "common", "pity": 10}


def test_missing_rarity_is_rejected():
    with pytest.raises(ValueError):
        lt.roll([{"id": "bad", "weight": 1}], 0)


def test_same_ticket_is_deterministic():
    first = lt.roll(TABLE, 70)
    assert first == {"id": "rare", "rarity": "rare", "pity": 0}
    assert first == lt.roll(TABLE, 70)
