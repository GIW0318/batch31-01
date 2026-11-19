import pytest

import destruction as ds

CHUNKS = [
    {"id": "a", "volume": 10, "neighbors": ["b"]},
    {"id": "b", "volume": 20, "neighbors": ["a", "c"]},
    {"id": "c", "volume": 30, "neighbors": ["b"]},
]


def test_valid_chunks_are_returned_sorted():
    assert ds.validate_chunks(CHUNKS) == ["a", "b", "c"]


def test_empty_chunks_are_rejected():
    with pytest.raises(ValueError):
        ds.validate_chunks([])


def test_duplicate_ids_are_rejected():
    with pytest.raises(ValueError):
        ds.validate_chunks([CHUNKS[0], dict(CHUNKS[0])])


def test_non_positive_volume_is_rejected():
    with pytest.raises(ValueError):
        ds.validate_chunks([{"id": "a", "volume": 0, "neighbors": []}])


def test_missing_neighbor_is_rejected():
    with pytest.raises(ValueError):
        ds.validate_chunks([{"id": "a", "volume": 1, "neighbors": ["ghost"]}])


def test_self_neighbor_is_rejected():
    with pytest.raises(ValueError):
        ds.validate_chunks([{"id": "a", "volume": 1, "neighbors": ["a"]}])


def test_duplicate_neighbor_is_rejected():
    with pytest.raises(ValueError):
        ds.validate_chunks([{"id": "a", "volume": 1, "neighbors": ["b", "b"]}, {"id": "b", "volume": 1, "neighbors": ["a"]}])


def test_disconnected_graph_is_rejected():
    with pytest.raises(ValueError):
        ds.validate_chunks([{"id": "a", "volume": 1, "neighbors": []}, {"id": "b", "volume": 1, "neighbors": []}])


def test_total_volume_limit_is_rejected():
    with pytest.raises(ValueError):
        ds.validate_chunks(CHUNKS, max_volume=59)


def test_chunk_count_limit_is_rejected():
    with pytest.raises(ValueError):
        ds.validate_chunks(CHUNKS, max_chunks=2)


def test_non_dict_chunk_is_rejected():
    with pytest.raises(ValueError):
        ds.validate_chunks(["a"])


def test_neighbors_must_be_list():
    with pytest.raises(ValueError):
        ds.validate_chunks([{"id": "a", "volume": 1, "neighbors": "b"}])


def test_single_chunk_is_valid():
    assert ds.validate_chunks([{"id": "a", "volume": 1, "neighbors": []}]) == ["a"]


def test_cycle_is_valid():
    ring = [
        {"id": "a", "volume": 1, "neighbors": ["b"]},
        {"id": "b", "volume": 1, "neighbors": ["c"]},
        {"id": "c", "volume": 1, "neighbors": ["a"]},
    ]
    assert ds.validate_chunks(ring) == ["a", "b", "c"]


def test_result_is_sorted():
    assert ds.validate_chunks(list(reversed(CHUNKS))) == ["a", "b", "c"]
