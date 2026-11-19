import math
from collections import deque
from numbers import Real


def _is_finite_number(value):
    if isinstance(value, bool) or not isinstance(value, Real):
        return False
    if isinstance(value, int):
        return True
    try:
        return math.isfinite(value)
    except OverflowError:
        return True
    except TypeError:
        return False


def _is_valid_limit(value, *, integer):
    if isinstance(value, bool):
        return False
    if integer:
        return isinstance(value, int) and value >= 0
    return _is_finite_number(value) and value >= 0


def validate_chunks(chunks, max_chunks=100, max_volume=1000):
    if not isinstance(chunks, (list, tuple)):
        raise ValueError("chunks must be a list of chunk dictionaries")
    if not chunks:
        raise ValueError("chunks must not be empty")
    if not _is_valid_limit(max_chunks, integer=True):
        raise ValueError("max_chunks must be a non-negative integer")
    if not _is_valid_limit(max_volume, integer=False):
        raise ValueError("max_volume must be a non-negative number")
    if len(chunks) > max_chunks:
        raise ValueError("chunk count exceeds max_chunks")

    ids = []
    seen_ids = set()
    chunk_ids = []
    total_volume = 0

    for chunk in chunks:
        if not isinstance(chunk, dict):
            raise ValueError("each chunk must be a dictionary")
        if "id" not in chunk or "volume" not in chunk or "neighbors" not in chunk:
            raise ValueError("each chunk requires id, volume, and neighbors")

        chunk_id = chunk["id"]
        if (
            isinstance(chunk_id, bool)
            or not isinstance(chunk_id, (str, int))
            or chunk_id == ""
        ):
            raise ValueError("chunk id must be a non-empty string or an integer")
        try:
            duplicate = chunk_id in seen_ids
        except TypeError as exc:
            raise ValueError("chunk id must be hashable") from exc
        if duplicate:
            raise ValueError("chunk ids must be unique")

        volume = chunk["volume"]
        if not _is_finite_number(volume) or volume <= 0:
            raise ValueError("chunk volume must be a positive finite number")

        neighbors = chunk["neighbors"]
        if not isinstance(neighbors, list):
            raise ValueError("chunk neighbors must be a list")
        neighbor_ids = set()
        for neighbor in neighbors:
            try:
                duplicate_neighbor = neighbor in neighbor_ids
            except TypeError as exc:
                raise ValueError("chunk neighbors must be hashable") from exc
            if duplicate_neighbor:
                raise ValueError("chunk neighbors must not contain duplicates")
            if neighbor == chunk_id:
                raise ValueError("a chunk cannot be its own neighbor")
            neighbor_ids.add(neighbor)

        seen_ids.add(chunk_id)
        ids.append(chunk_id)
        chunk_ids.append(neighbor_ids)
        total_volume += volume

    if total_volume > max_volume:
        raise ValueError("total volume exceeds max_volume")

    adjacency = {chunk_id: set() for chunk_id in ids}
    for chunk_id, neighbors in zip(ids, chunk_ids):
        for neighbor in neighbors:
            if neighbor not in adjacency:
                raise ValueError("chunk neighbor does not exist")
            adjacency[chunk_id].add(neighbor)
            adjacency[neighbor].add(chunk_id)

    visited = {ids[0]}
    queue = deque([ids[0]])
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    if len(visited) != len(ids):
        raise ValueError("chunk graph must be connected")

    try:
        return sorted(ids)
    except TypeError as exc:
        raise ValueError("chunk ids must be mutually sortable") from exc
