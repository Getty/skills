# Scope and representation selection

Choose the smallest navigation model that supplies the requested behavior. A broad algorithm library is useful reference knowledge; it is not a list of mandatory features.

## Contents

- [Separate the decisions](#separate-the-decisions)
- [Define the query](#define-the-query)
- [Choose the representation](#choose-the-representation)
- [Select an initial algorithm](#select-an-initial-algorithm)
- [Build a small complete implementation](#build-a-small-complete-implementation)
- [Extend for a demonstrated requirement](#extend-for-a-demonstrated-requirement)

## Separate the decisions

Keep four responsibilities explicit:

| Responsibility | Question |
|---|---|
| Goal/task selection | Where should this agent go, and why? |
| Route planning | Which valid sequence of states/actions reaches an accepted goal? |
| Path execution | How should the agent follow the route while obeying movement constraints? |
| Coordination | How should agents share scarce space or scheduled connections? |

Terrain supplies physical facts. Buildings supply geometry, doors and access state. Logistics supplies destinations and resource reservations. Population/behavior chooses goals and urgency. Navigation supplies routes, reachability, travel estimates and execution status.

These responsibilities may live in one process or ECS. They do not require services, message brokers or separate threads. Keep the knowledge skill independent of any terrain, logistics or population skill; use ordinary typed inputs or adapters.

Red Blob's [A* introduction](https://www.redblobgames.com/pathfinding/a-star/introduction.html) emphasizes that search operates on a graph rather than directly understanding the visible world. The separation above is an engineering application of that principle.

## Define the query

Record the following before choosing an algorithm:

- **State:** location only, or location plus orientation, movement mode, time or another necessary variable.
- **Agent profile:** radius/shape, height, permitted movement, relevant capability and cost parameters.
- **Goal:** exact point, one of several entrances, interaction range, a region or an acceptable set of states.
- **Objective:** shortest distance, least time, movement points, a specified weighted score or a lexicographic objective.
- **World behavior:** static during a query, revised between queries, or explicitly time-dependent.
- **Workload:** few unrelated routes, many agents sharing a goal, repeated similar searches, or joint scheduling.
- **Guarantee:** exact graph optimum, stated bounded suboptimality, approximate route, or merely feasible route.
- **Budget:** query latency, expansions, memory and update cost on the actual target.

If unspecified, assume a finite snapshot graph with nonnegative costs, one agent, one goal and no temporal reservations. Use Dijkstra as a reference and A* with a justified heuristic if available. Treat h=0 as a correct fallback, not a failure.

## Choose the representation

| Representation | Useful cases | Important limitation |
|---|---|---|
| Four/eight-neighbor grid | Tile games, simple editable worlds, easy test oracles | Direction bias, resolution and corner rules |
| Hex grid | Hex-based movement rules | Use its actual adjacency and metric |
| Waypoint/road graph | Designed routes, doors, transport networks | Missing connections remain unreachable regardless of search quality |
| Room/portal graph | Indoor connectivity, coarse planning | Needs local traversal and actual portal geometry |
| Navigation mesh | Continuous walkable surfaces | Agent clearance, corridor construction and dynamic rebuilds |
| Coarse regions plus local graph | Large maps with local detail | Abstraction/portal choices affect path quality |
| Action/state lattice | Vehicles, jumps, turning constraints | More state and movement primitive validation |
| Volumetric graph | Flight, swimming or complex 3D voids | A surface navmesh cannot represent all free-space motion |

A polygon terrain simulation does not force navigation to reuse its cell centers. A visually small doorway can be important to navigation but unresolved by a large terrain cell. Conversely, political regions and decorative terrain triangles need not add search states.

For a simple colony prototype, use a grid or modest waypoint graph whose resolution can represent its passages. Validate one building entrance, one blocked route, one terrain change and one loaded save before introducing hierarchy or crowd algorithms.

## Select an initial algorithm

| Query pattern | Suitable starting point | Conditions |
|---|---|---|
| Equal-cost steps | BFS | All traversable edges have the same cost |
| Varying nonnegative costs, uncertain heuristic | Dijkstra | Finite graph/snapshot and explicit directed edges |
| One goal, useful lower bound | A* | Heuristic and reopening/termination rules must match the guarantee |
| Many starts, shared goal/profile/costs | Reverse Dijkstra field | Reverse directed arcs correctly; store an executable successor policy |
| Several interchangeable goals | Multi-source reverse field or goal-set A* | Goal eligibility is provided by the caller |
| Repeated changing graph | Fresh A* first; consider incremental repair | Compare repair bookkeeping with observed rebuild/search costs |
| Congested narrow passage | Local queue/capacity reservation first | Add time/coordination only where conflict matters |

Use [search and heuristics](search-and-heuristics.md) for exact conditions. The presence of many agents does not by itself require multi-agent optimal planning.

## Build a small complete implementation

1. Define graph construction and the agent profile.
2. Give every edge a meaning that the movement system can execute.
3. Implement nonnegative costs and a reference shortest-path query.
4. Return explicit found/unreachable/budget/cancelled/stale outcomes.
5. Validate every returned transition and reconstruct its actual cost.
6. Follow the route with an arrival definition and stuck detection.
7. React to an obstacle or cost change by revision and revalidation.
8. Preserve stable goals and authoritative world state on save/load.

Do not require a navmesh if a grid satisfies the game. Do not require material simulation merely because mud affects walking speed: the navigation adapter can consume a supplied speed map.

## Extend for a demonstrated requirement

### Many agents travel to one destination

Share a reverse distance field only when their eligibility and cost objective match. Different radii, door permissions or movement speeds may require separate fields or a proved shared lower-bound field. Congestion changes can make fields stale.

### Buildings alter passages

Invalidate the affected navigation representation and any unsafe route segments. Publish a usable geometry revision when collision and navigation agree. Replanning from scratch can remain sufficient for a modest world.

### Long routes dominate query cost

Measure graph construction, search and movement separately. Consider coarser abstraction, portal hierarchy, landmarks or caching before selecting an algorithm based on its name. Check the resulting route quality and update cost.

### Vehicles cannot turn in place

Add heading/kinematic state or validated motion primitives. A point route through a narrow right-angle passage is not evidence that the vehicle can execute it.

### One-lane doorways deadlock

Add a queue, yield rule or time reservation for that resource. Joint MAPF algorithms are optional when the required coordination and guarantees justify their cost.

### Teleports, elevators or ferries exist

Model their transitions, direction, eligibility, wait and action semantics. Recheck heuristics: Euclidean distance may cease to be a lower bound when cheap long-distance connections exist.

### Sources and interpretation

Use [Red Blob's implementation guide](https://www.redblobgames.com/pathfinding/a-star/implementation.html) for accessible graph/search structure and [Recast/Detour](https://github.com/recastnavigation/recastnavigation) as an optional navigation implementation reference. The selection tables and workflow are original engineering recommendations, not benchmark claims.
