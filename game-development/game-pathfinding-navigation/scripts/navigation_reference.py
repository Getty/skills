#!/usr/bin/env python3
"""Small finite-graph navigation references, not a game navigation engine.

Use Python 3.10+ and the standard library. Costs are nonnegative finite numbers
in one declared unit. A found route is optimal only under the documented search
assumptions; a supplied heuristic is not silently assumed to be admissible.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import heapq
import itertools
import json
import math
from numbers import Real
from pathlib import Path
from types import MappingProxyType
from typing import Mapping, Sequence


def _number(value: float, label: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{label} must be a real number")
    value = float(value)
    if not math.isfinite(value) or value < 0 or (positive and value == 0):
        raise ValueError(f"{label} must be finite and {'positive' if positive else 'nonnegative'}")
    return value


def _identifier(value: str, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a nonempty string")
    return value


@dataclass(frozen=True)
class Edge:
    edge_id: str
    source: str
    target: str
    cost: float


class Graph:
    """Validated snapshot of a directed graph; parallel edges are allowed.

    Each physical/action edge has a distinct ID. The fingerprint covers nodes,
    directed endpoints and costs; it is a reference stale-data guard rather than
    a replacement for a game's revision and publication protocol.
    """

    def __init__(self, nodes: Sequence[str], edges: Sequence[Edge]):
        if isinstance(nodes, (str, bytes)):
            raise ValueError("nodes must be a sequence of IDs")
        ordered_nodes = [_identifier(node, "node ID") for node in nodes]
        if len(set(ordered_nodes)) != len(ordered_nodes):
            raise ValueError("duplicate node ID")
        self.nodes = tuple(sorted(ordered_nodes))
        known = set(self.nodes)
        by_id: dict[str, Edge] = {}
        outgoing: dict[str, list[Edge]] = {node: [] for node in self.nodes}
        incoming: dict[str, list[Edge]] = {node: [] for node in self.nodes}
        for edge in edges:
            edge_id = _identifier(edge.edge_id, "edge ID")
            if edge_id in by_id:
                raise ValueError(f"duplicate edge ID: {edge_id}")
            if edge.source not in known or edge.target not in known:
                raise ValueError(f"edge {edge_id} references an unknown endpoint")
            normalized = Edge(edge_id, edge.source, edge.target,
                              _number(edge.cost, f"{edge_id} cost"))
            by_id[edge_id] = normalized
            outgoing[edge.source].append(normalized)
            incoming[edge.target].append(normalized)
        self.edges = MappingProxyType(dict(sorted(by_id.items())))
        self.outgoing = MappingProxyType({
            node: tuple(sorted(items, key=lambda edge: edge.edge_id))
            for node, items in outgoing.items()
        })
        self.incoming = MappingProxyType({
            node: tuple(sorted(items, key=lambda edge: edge.edge_id))
            for node, items in incoming.items()
        })
        canonical = [list(self.nodes), [
            [edge.edge_id, edge.source, edge.target, edge.cost.hex()]
            for edge in self.edges.values()
        ]]
        self.fingerprint = hashlib.sha256(
            json.dumps(canonical, separators=(",", ":")).encode("utf-8")
        ).hexdigest()


def _goals(graph: Graph, goals: Sequence[str]) -> tuple[str, ...]:
    if isinstance(goals, (str, bytes)):
        raise ValueError("goals must be a sequence, not one string")
    result = tuple(sorted(set(_identifier(goal, "goal") for goal in goals)))
    if not result or any(goal not in graph.outgoing for goal in result):
        raise ValueError("goals must contain at least one known node")
    return result


def _heuristic(graph: Graph, values: Mapping[str, float] | None) -> dict[str, float]:
    if values is None:
        return {node: 0.0 for node in graph.nodes}
    if set(values) != set(graph.nodes):
        raise ValueError("heuristic must specify exactly the graph's node IDs")
    return {node: _number(values[node], f"heuristic at {node}") for node in graph.nodes}


@dataclass(frozen=True)
class SearchResult:
    status: str
    nodes: list[str]
    edges: list[str]
    cost: float | None
    expansions: int
    reopenings: int
    heap_pushes: int
    graph_fingerprint: str


def astar(graph: Graph, start: str, goal: str,
          heuristic: Mapping[str, float] | None = None,
          max_expansions: int | None = None) -> SearchResult:
    """A* with lazy heap entries and reopening after a strictly better g-value.

    Optimal on this finite nonnegative graph when h is admissible, finite,
    nonnegative and zero at the goal. Inconsistent admissible h is supported.
    The caller must establish admissibility; heuristic_audit can check a finite
    snapshot. None supplies h=0 (Dijkstra). Stop when the goal is popped, not
    when it is first discovered.

    Budget counts non-goal expansions. A zero-budget start==goal succeeds.
    Budget exhaustion has no route/cost and is not proof of unreachability.
    Results are not resumable search state. Use immutable snapshots per query.
    """
    if start not in graph.outgoing or goal not in graph.outgoing:
        raise ValueError("start and goal must exist")
    if max_expansions is not None and (
        isinstance(max_expansions, bool) or not isinstance(max_expansions, int)
        or max_expansions < 0
    ):
        raise ValueError("max_expansions must be a nonnegative integer or None")
    h = _heuristic(graph, heuristic)
    if h[goal] != 0.0:
        raise ValueError("heuristic at goal must be zero")
    sequence = itertools.count()
    heap = [(h[start], 0.0, next(sequence), start)]
    best = {start: 0.0}
    predecessor: dict[str, Edge] = {}
    expanded_at: dict[str, float] = {}
    expansions = reopenings = 0
    pushes = 1
    while heap:
        _, g_value, _, node = heapq.heappop(heap)
        if g_value != best.get(node):
            continue
        if node == goal:
            nodes, edges = [goal], []
            seen = {goal}
            while nodes[-1] != start:
                edge = predecessor[nodes[-1]]
                edges.append(edge.edge_id)
                nodes.append(edge.source)
                if nodes[-1] in seen:
                    raise RuntimeError("cyclic predecessor chain")
                seen.add(nodes[-1])
            nodes.reverse()
            edges.reverse()
            cost = _number(math.fsum(graph.edges[key].cost for key in edges), "path cost")
            return SearchResult("found", nodes, edges, cost, expansions,
                                reopenings, pushes, graph.fingerprint)
        if max_expansions is not None and expansions >= max_expansions:
            return SearchResult("budget_exhausted", [], [], None, expansions,
                                reopenings, pushes, graph.fingerprint)
        if node in expanded_at:
            reopenings += 1
        expanded_at[node] = g_value
        expansions += 1
        for edge in graph.outgoing[node]:
            candidate = _number(g_value + edge.cost, "accumulated path cost")
            if candidate < best.get(edge.target, math.inf):
                best[edge.target] = candidate
                predecessor[edge.target] = edge
                priority = _number(candidate + h[edge.target], "search priority")
                heapq.heappush(heap, (priority, candidate, next(sequence), edge.target))
                pushes += 1
    return SearchResult("unreachable", [], [], None, expansions,
                        reopenings, pushes, graph.fingerprint)


def dijkstra(graph: Graph, start: str, goal: str,
             max_expansions: int | None = None) -> SearchResult:
    """Single-target Dijkstra using the same validated search implementation."""
    return astar(graph, start, goal, max_expansions=max_expansions)


@dataclass(frozen=True)
class ReverseField:
    goals: tuple[str, ...]
    distance: dict[str, float | None]
    next_edge: dict[str, str | None]
    settlement_rank: dict[str, int]
    graph_fingerprint: str


def reverse_cost_field(graph: Graph, goals: Sequence[str]) -> ReverseField:
    """Multi-source Dijkstra on reversed edges, retaining original edge costs.

    distance[u] is minimum cost FROM u TO any goal, including on directed graphs.
    next_edge chooses a successor already settled at assignment time. Therefore
    settlement rank decreases along the policy, even across zero-cost edges.
    Merely choosing any equal-cost neighbor afterwards can create zero cycles.
    None denotes unreachable distance, or no successor for goals/unreachable.
    """
    targets = _goals(graph, goals)
    sequence = itertools.count()
    best = {goal: 0.0 for goal in targets}
    next_edge: dict[str, str | None] = {node: None for node in graph.nodes}
    heap = [(0.0, next(sequence), goal) for goal in targets]
    heapq.heapify(heap)
    ranks: dict[str, int] = {}
    while heap:
        distance, _, node = heapq.heappop(heap)
        if node in ranks or distance != best.get(node):
            continue
        ranks[node] = len(ranks)
        for edge in graph.incoming[node]:
            if edge.source in ranks:
                continue
            candidate = _number(distance + edge.cost, "reverse distance")
            if candidate < best.get(edge.source, math.inf):
                best[edge.source] = candidate
                next_edge[edge.source] = edge.edge_id
                heapq.heappush(heap, (candidate, next(sequence), edge.source))
    return ReverseField(targets, {node: best.get(node) for node in graph.nodes},
                        next_edge, ranks, graph.fingerprint)


def follow_policy(graph: Graph, field: ReverseField, start: str) -> SearchResult:
    """Follow a reverse field on its original snapshot, checking rank descent."""
    if graph.fingerprint != field.graph_fingerprint:
        raise ValueError("reverse field belongs to another graph snapshot")
    if start not in graph.outgoing:
        raise ValueError("unknown start")
    if field.distance[start] is None:
        return SearchResult("unreachable", [], [], None, 0, 0, 0, graph.fingerprint)
    nodes, edges = [start], []
    while nodes[-1] not in field.goals:
        node = nodes[-1]
        edge_id = field.next_edge[node]
        if edge_id is None or edge_id not in graph.edges:
            raise ValueError("field lacks a valid successor")
        edge = graph.edges[edge_id]
        if edge.source != node or field.settlement_rank[edge.target] >= field.settlement_rank[node]:
            raise ValueError("field successor must descend settlement rank")
        edges.append(edge_id)
        nodes.append(edge.target)
    cost = _number(math.fsum(graph.edges[key].cost for key in edges), "policy cost")
    return SearchResult("found", nodes, edges, cost, 0, 0, 0, graph.fingerprint)


def heuristic_audit(graph: Graph, goals: Sequence[str], values: Mapping[str, float],
                    tolerance: float = 1e-12) -> dict[str, object]:
    """Compare a finite heuristic against exact-graph reverse Dijkstra distances.

    This is an offline reference check, not an optimization for each A* query.
    Tolerance is in cost units. Unreachable true distances are infinite; finite
    h there supplies no reachability proof. Floating arithmetic limits apply.
    """
    tolerance = _number(tolerance, "audit tolerance")
    h = _heuristic(graph, values)
    field = reverse_cost_field(graph, goals)
    overestimates = [
        {"node": node, "heuristic": h[node], "true_distance": distance}
        for node, distance in field.distance.items()
        if distance is not None and h[node] > distance + tolerance
    ]
    inconsistent = [
        {"edge_id": edge.edge_id, "h_source": h[edge.source],
         "edge_plus_h_target": edge.cost + h[edge.target]}
        for edge in graph.edges.values()
        if h[edge.source] > edge.cost + h[edge.target] + tolerance
    ]
    nonzero_goals = [goal for goal in field.goals if h[goal] != 0.0]
    return {
        "admissible_within_tolerance": not overestimates,
        "consistent_within_tolerance": not inconsistent,
        "zero_at_goals": not nonzero_goals,
        "overestimates": overestimates,
        "inconsistent_edges": inconsistent,
        "nonzero_goals": nonzero_goals,
        "true_cost_to_goal": field.distance,
        "cost_tolerance": tolerance,
    }


@dataclass(frozen=True)
class GridModel:
    graph: Graph
    coordinates: Mapping[str, tuple[int, int]]
    diagonals: bool
    cell_size_m: float
    minimum_time_per_m: float


def grid_graph(width: int, height: int, *,
               blocked: Sequence[Sequence[int]] = (),
               multipliers: Mapping[tuple[int, int], float] | None = None,
               diagonals: bool = False, cell_size_m: float = 1.0,
               base_speed_m_s: float = 1.0) -> GridModel:
    """Build point-agent 4/8-neighbor grid, forbidding diagonal corner cutting.

    Travel cost [s] = step length [m] / speed [m/s] * destination multiplier.
    Costs may be directed because entering different cells has different costs.
    This is not a finite-radius collision model or a physical crowd simulation.
    """
    for value in (width, height):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError("grid dimensions must be positive integers")
    if type(diagonals) is not bool:
        raise ValueError("diagonals must be Boolean")
    spacing = _number(cell_size_m, "cell size", positive=True)
    speed = _number(base_speed_m_s, "base speed", positive=True)
    def coordinate(value):
        if len(value) != 2 or any(isinstance(v, bool) or not isinstance(v, int) for v in value):
            raise ValueError("grid coordinates must contain two integers")
        point = tuple(value)
        if not (0 <= point[0] < width and 0 <= point[1] < height):
            raise ValueError("grid coordinate is outside bounds")
        return point
    walls = {coordinate(point) for point in blocked}
    factors = {}
    for position, factor in (multipliers or {}).items():
        point = coordinate(position)
        if point in walls:
            raise ValueError("blocked cells cannot have traversal multipliers")
        factors[point] = _number(factor, "traversal multiplier", positive=True)
    coords = {(x, y): f"{x},{y}" for y in range(height) for x in range(width)
              if (x, y) not in walls}
    if not coords:
        raise ValueError("grid must have a traversable cell")
    steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diagonals:
        steps += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    edges = []
    for (x, y), source in coords.items():
        for dx, dy in steps:
            destination = (x + dx, y + dy)
            if destination not in coords:
                continue
            if dx and dy and ((x + dx, y) not in coords or (x, y + dy) not in coords):
                continue
            target = coords[destination]
            cost = spacing * math.hypot(dx, dy) / speed * factors.get(destination, 1.0)
            edges.append(Edge(f"{source}>{target}", source, target, cost))
    minimum_factor = min(factors.get(point, 1.0) for point in coords)
    return GridModel(Graph(tuple(coords.values()), edges),
                     MappingProxyType({node: point for point, node in coords.items()}),
                     diagonals, spacing, minimum_factor / speed)


def grid_heuristic(model: GridModel, goal: str) -> dict[str, float]:
    """Manhattan or octile lower bound in seconds for this adapter's own graph.

    Do not reuse unchanged after adding cheaper portals, off-mesh edges or
    new costs that invalidate minimum_time_per_m. Audit the new graph instead.
    """
    if goal not in model.coordinates:
        raise ValueError("unknown grid goal")
    gx, gy = model.coordinates[goal]
    result = {}
    for node, (x, y) in model.coordinates.items():
        dx, dy = abs(gx - x), abs(gy - y)
        steps = dx + dy
        if model.diagonals:
            steps += (math.sqrt(2.0) - 2.0) * min(dx, dy)
        result[node] = steps * model.cell_size_m * model.minimum_time_per_m
    return result


def discrete_conflicts(paths: Mapping[str, Sequence[str]], *,
                       stay_at_goal: bool = True) -> list[dict[str, object]]:
    """Check unit-tick vertex and opposite-edge conflicts, not continuous safety.

    Each path gives node occupancy at t=0,1,...; repetitions mean waiting.
    stay_at_goal holds the final node to the longest supplied schedule. False
    removes the agent after its last listed occupancy. Following a vacated node
    is allowed. This does not validate graph edges, capacities, diagonal segment
    crossings, radii, acceleration, or motions between ticks.
    """
    if type(stay_at_goal) is not bool:
        raise ValueError("stay_at_goal must be Boolean")
    normalized = {}
    for agent, path in paths.items():
        _identifier(agent, "agent ID")
        if isinstance(path, (str, bytes)) or not path:
            raise ValueError("each agent needs a nonempty sequence of nodes")
        normalized[agent] = tuple(_identifier(node, "path node") for node in path)
    horizon = max((len(path) for path in normalized.values()), default=0)
    def at(agent, tick):
        path = normalized[agent]
        return path[tick] if tick < len(path) else path[-1] if stay_at_goal else None
    conflicts = []
    for tick in range(horizon):
        for first, second in itertools.combinations(sorted(normalized), 2):
            a, b = at(first, tick), at(second, tick)
            if a is not None and a == b:
                conflicts.append({"type": "vertex", "time": tick,
                                  "agents": [first, second], "node": a})
            if tick + 1 < horizon:
                a_next, b_next = at(first, tick + 1), at(second, tick + 1)
                if (None not in (a, b, a_next, b_next) and a != a_next
                        and a == b_next and b == a_next):
                    conflicts.append({"type": "edge_swap", "time": tick,
                                      "agents": [first, second], "edge": [a, a_next]})
    return conflicts


def graph_from_record(record: Mapping[str, object]) -> Graph:
    return Graph(record["nodes"], [Edge(**edge) for edge in record["edges"]])


def run_demo(fixtures_path: Path | None = None) -> dict[str, object]:
    root = Path(__file__).resolve().parents[1]
    data = json.loads((fixtures_path or root / "assets" / "search-fixtures.json")
                      .read_text(encoding="utf-8"))
    output = {"origin": data["metadata"]["origin"], "search": {}}
    for item in data["search_cases"]:
        graph = graph_from_record(item["graph"])
        result = astar(graph, item["start"], item["goal"], item.get("heuristic"))
        output["search"][item["name"]] = asdict(result)
    field_case = data["reverse_field"]
    graph = graph_from_record(field_case["graph"])
    field = reverse_cost_field(graph, field_case["goals"])
    output["reverse_field"] = asdict(field)
    zero = data["zero_cycle_field"]
    graph = graph_from_record(zero["graph"])
    field = reverse_cost_field(graph, zero["goals"])
    output["zero_cycle_policy"] = asdict(follow_policy(graph, field, zero["start"]))
    inconsistent = next(item for item in data["search_cases"]
                        if item["name"] == "admissible_inconsistent")
    output["heuristic_audit"] = heuristic_audit(
        graph_from_record(inconsistent["graph"]), [inconsistent["goal"]],
        inconsistent["heuristic"])
    output["schedule_conflicts"] = discrete_conflicts(data["schedule_example"]["paths"])
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["demo", "audit"])
    parser.add_argument("--fixtures", type=Path, help="Compatible search-fixtures JSON")
    args = parser.parse_args()
    result = run_demo(args.fixtures)
    if args.command == "audit":
        result = result["heuristic_audit"]
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
