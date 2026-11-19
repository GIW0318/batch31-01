import math


def assign(agents, slots, obstacles=None):
    if not isinstance(agents, list) or not isinstance(slots, list):
        raise ValueError("agents and slots must both be lists")
    if obstacles is not None and not isinstance(obstacles, list):
        raise ValueError("obstacles must be a list of coordinates")

    blocked_cells = set()
    for cell in obstacles or []:
        blocked_cells.add(_validated_position(cell))

    prepared_agents = []
    seen_agent_ids = set()
    for agent in agents:
        if not isinstance(agent, dict):
            raise ValueError("each agent must be a dict")
        agent_id = _required_value(agent, "id")
        role = _required_value(agent, "role")
        position = _validated_position(agent.get("pos"))
        if agent_id in seen_agent_ids:
            raise ValueError("duplicate agent id: %r" % (agent_id,))
        seen_agent_ids.add(agent_id)
        prepared_agents.append((agent_id, role, position))

    prepared_slots = []
    seen_slot_ids = set()
    declared_roles = set()
    for slot in slots:
        if not isinstance(slot, dict):
            raise ValueError("each slot must be a dict")
        slot_id = _required_value(slot, "id")
        role = _required_value(slot, "role")
        position = _validated_position(slot.get("pos"))
        if slot_id in seen_slot_ids:
            raise ValueError("duplicate slot id: %r" % (slot_id,))
        seen_slot_ids.add(slot_id)
        declared_roles.add(role)
        if position not in blocked_cells:
            prepared_slots.append((slot_id, role, position))

    if not prepared_agents or not prepared_slots:
        return {}

    agents_by_role = {}
    for agent_id, role, position in prepared_agents:
        agents_by_role.setdefault(role, []).append((agent_id, position))

    for role in agents_by_role:
        if role not in declared_roles:
            raise ValueError("no slot matches agent role: %r" % (role,))

    slots_by_role = {}
    for slot_id, role, position in prepared_slots:
        slots_by_role.setdefault(role, []).append((slot_id, position))

    assignment = {}
    for role, role_agents in agents_by_role.items():
        if role not in slots_by_role:
            continue
        assignment.update(_match_role(role_agents, slots_by_role[role]))
    return assignment


def _required_value(record, key):
    if key not in record:
        raise ValueError("missing required field: %r" % (key,))
    value = record[key]
    try:
        hash(value)
    except TypeError:
        raise ValueError("field %r must be hashable" % (key,)) from None
    return value


def _validated_position(value):
    if isinstance(value, (str, bytes, dict)) or not hasattr(value, "__len__"):
        raise ValueError("position must be a pair of numeric coordinates")
    if len(value) != 2:
        raise ValueError("position must contain exactly two coordinates")
    coordinates = []
    for coordinate in value:
        if isinstance(coordinate, bool) or not isinstance(coordinate, (int, float)):
            raise ValueError("position coordinates must be numeric")
        coordinates.append(float(coordinate))
    return (coordinates[0], coordinates[1])


def _match_role(role_agents, role_slots):
    agent_ids = [agent_id for agent_id, _ in role_agents]
    slot_ids = [slot_id for slot_id, _ in role_slots]
    costs = [
        [math.hypot(ax - sx, ay - sy) for _, (sx, sy) in role_slots]
        for _, (ax, ay) in role_agents
    ]

    if len(agent_ids) <= len(slot_ids):
        matched_slots = _hungarian(costs)
        return {
            slot_ids[slot_index]: agent_ids[agent_index]
            for agent_index, slot_index in enumerate(matched_slots)
            if slot_index >= 0
        }

    transposed = [
        [costs[row][column] for row in range(len(agent_ids))]
        for column in range(len(slot_ids))
    ]
    matched_agents = _hungarian(transposed)
    return {
        slot_ids[slot_index]: agent_ids[agent_index]
        for slot_index, agent_index in enumerate(matched_agents)
        if agent_index >= 0
    }


def _hungarian(cost):
    rows = len(cost)
    columns = len(cost[0])
    u = [0.0] * (rows + 1)
    v = [0.0] * (columns + 1)
    p = [0] * (columns + 1)
    way = [0] * (columns + 1)

    for i in range(1, rows + 1):
        p[0] = i
        j0 = 0
        minv = [float("inf")] * (columns + 1)
        used = [False] * (columns + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = float("inf")
            j1 = 0
            for j in range(1, columns + 1):
                if not used[j]:
                    current = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if current < minv[j]:
                        minv[j] = current
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(columns + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    row_to_column = [-1] * rows
    for j in range(1, columns + 1):
        if p[j] > 0:
            row_to_column[p[j] - 1] = j - 1
    return row_to_column
