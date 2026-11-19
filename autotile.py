EMPTY_TILE = "empty"

# Four-neighborhood topology classes, encoded as unary bitmasks:
# 0 neighbors -> 1 (end), 1-2 -> 3 (line), 3 -> 7 (tee), 4 -> 15 (full).
_MASK_BY_NEIGHBOR_COUNT = (1, 3, 3, 7, 15)


def _validate_grid(grid):
    if not isinstance(grid, list):
        raise ValueError("grid must be a list of rows")
    if not grid:
        raise ValueError("grid must not be empty")
    width = len(grid[0])
    if width == 0:
        raise ValueError("grid rows must not be empty")
    for row in grid:
        if not isinstance(row, list) or len(row) != width:
            raise ValueError("grid must be rectangular (all rows must have the same length)")
        for cell in row:
            if cell not in (0, 1):
                raise ValueError("grid cells must be 0 or 1")
    return len(grid), width


def _validate_rules(rules):
    if not isinstance(rules, dict):
        raise ValueError("rules must be a dict mapping bitmask to tile id")
    for tile_id in rules.values():
        if not isinstance(tile_id, str):
            raise ValueError("tile ids in rules must be strings")


def _solid_neighbor_count(grid, row, col, height, width):
    count = 0
    if row > 0 and grid[row - 1][col] == 1:
        count += 1
    if row + 1 < height and grid[row + 1][col] == 1:
        count += 1
    if col > 0 and grid[row][col - 1] == 1:
        count += 1
    if col + 1 < width and grid[row][col + 1] == 1:
        count += 1
    return count


def autotile(grid, rules):
    """Stitch tiles for a 0/1 grid using a four-neighborhood bitmask.

    Cells outside the map boundary count as empty ground. Returns tile ids
    in row-major order. Raises ValueError on any invalid input.
    """
    height, width = _validate_grid(grid)
    _validate_rules(rules)

    result = []
    for row in range(height):
        for col in range(width):
            if grid[row][col] == 0:
                result.append(EMPTY_TILE)
                continue
            neighbors = _solid_neighbor_count(grid, row, col, height, width)
            mask = _MASK_BY_NEIGHBOR_COUNT[neighbors]
            if mask not in rules:
                raise ValueError("missing tile rule for bitmask %d" % mask)
            result.append(rules[mask])
    return result
