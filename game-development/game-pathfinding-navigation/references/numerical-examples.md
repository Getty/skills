# Executable navigation examples

## Contents

- [Scope and execution](#scope-and-execution)
- [API and result contract](#api-and-result-contract)
- [Graph costs and path identity](#graph-costs-and-path-identity)
- [A-star and heuristic checks](#a-star-and-heuristic-checks)
- [Reverse fields on directed graphs](#reverse-fields-on-directed-graphs)
- [Grid costs and lower bounds](#grid-costs-and-lower-bounds)
- [Discrete schedule conflicts](#discrete-schedule-conflicts)
- [Verification and limits](#verification-and-limits)

## Scope and execution

Use the bundled original Python implementation for small finite-graph calculations, analytical fixtures and regression examples. It requires Python 3.10 or later and the standard library.

Run from the skill directory:

~~~bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/navigation_reference.py demo
PYTHONDONTWRITEBYTECODE=1 python3 scripts/navigation_reference.py audit
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_navigation_reference.py
~~~

The CLI reads `assets/search-fixtures.json` relative to the script and prints finite JSON to stdout. It does not modify a game, build a navmesh or write persistent state. `--fixtures /absolute/path/search-fixtures.json` replaces the supplied fixture collection with the same structure and named cases. The `audit` command displays the collection's inconsistent-heuristic example; use the Python `heuristic_audit` function to audit a different graph.

`assets/grid-fixtures.json` supplies analytical grid cases used by the test suite. Every fixture is explicitly synthetic. They are not measured gameplay data, a benchmark score, or a production save schema.

## API and result contract

| API | Purpose | Important boundary |
|---|---|---|
| `Graph(nodes, edges)` | Validate a finite directed graph and snapshot fingerprint | Requires unique node/edge IDs and finite nonnegative costs |
| `Edge(id, source, target, cost)` | Identify one action or connection | Parallel edges need distinct IDs |
| `astar(graph, start, goal, heuristic, max_expansions)` | Goal-directed search with reopening | Caller establishes admissibility; default h=0 |
| `dijkstra(graph, start, goal, max_expansions)` | Nonnegative-cost shortest path | Uses the same search kernel with zero heuristic |
| `reverse_cost_field(graph, goals)` | Cost from each node to its cheapest reachable goal | Traverses incoming edges with original directed costs |
| `follow_policy(graph, field, start)` | Recover a route from that reverse field | Rejects a changed graph fingerprint and non-descending rank |
| `heuristic_audit(graph, goals, values, tolerance)` | Check finite-snapshot lower bounds and consistency | Offline reference calculation, not a cheap per-query check |
| `grid_graph(...)` | Build a 4/8-neighbor point-agent graph | No finite-radius or continuous-motion collision model |
| `grid_heuristic(model, goal)` | Manhattan/octile lower bound in seconds | Valid for the adapter's generated transitions and cost floor |
| `discrete_conflicts(paths, stay_at_goal=...)` | Detect vertex collisions and opposite-edge swaps | Unit-tick graph occupancy only; not a planner |

Search results distinguish:

- **found:** an actual sequence of node and edge IDs, with its recomputed cost.
- **unreachable:** the frontier was exhausted on this snapshot.
- **budget_exhausted:** the allowed non-goal expansions were used; no reachability conclusion or partial route is returned.

A found path is feasible under the graph. Optimality additionally requires the documented heuristic assumptions. A deliberately excessive heuristic can produce a feasible but nonoptimal result; a test demonstrates this rather than giving all successful searches an unconditional optimality label.

The expansion budget counts expanded non-goal nodes. Returning an already popped goal does not consume an expansion. Therefore start=goal succeeds with cost zero even at budget zero. The implementation does not return resumable search state.

## Graph costs and path identity

For a route \(P=(e_1,\ldots,e_k)\), evaluate

\[
C(P)=\sum_{j=1}^{k}c(e_j).
\]

Every edge and the heuristic use one cost unit. It can be seconds, distance, energy or a deliberately defined game utility. Do not add seconds to metres without explicit conversion.

The weighted-detour fixture has:

- Route S → A → G: \(1+10=11\).
- Route S → B → C → G: \(2+2+2=6\).

The longer route in edge count is cheaper. A breadth-first result is not generally a minimum-cost result on such a graph.

Store actual edge IDs in a path. Two edges joining the same pair of nodes may represent a door and a jump, or have different permissions and costs. A node sequence alone cannot uniquely identify the chosen action in that case.

The graph fingerprint includes the complete sorted node set and every directed edge's ID, endpoints and floating-point cost. A changed edge invalidates a stored reverse field even if the previously selected route did not use it. A newly cheaper alternative can change optimality. This is a small stale-data guard; a production game normally uses its own revisions, profile identity and publication protocol.

## A-star and heuristic checks

Use

\[
f(v)=g(v)+h(v).
\]

The implementation returns the goal when it is removed from the minimum-priority queue with its current best label. Returning it when first discovered would fail the fixture S → G costing 10 versus S → A → G costing \(1+1=2\).

For exact A-star on the supported finite graph, require nonnegative costs and a finite, nonnegative heuristic satisfying:

\[
h(v)\le d^*(v,G),\qquad h(G)=0.
\]

Consistency is the stronger edge condition

\[
h(u)\le c(u,v)+h(v).
\]

The kernel permits an admissible but inconsistent heuristic by reopening a previously expanded node when a strictly better \(g\) arrives. It discards obsolete heap entries, uses strict improvement for relaxation, and never treats first discovery as permanent closure. Zero-cost edges and self-loops are supported.

### Original reopening example

Use edges S → A=3, S → B=1, B → A=1, A → G=3, B → G=100, and heuristic:

| Node | h | True cost to G |
|---|---:|---:|
| S | 5 | 5 |
| A | 0 | 3 |
| B | 4 | 4 |
| G | 0 | 0 |

The heuristic is admissible. It is inconsistent on B → A because \(4>1+0\).

A is initially expanded with \(g=3\), producing a goal candidate of 6. B later improves A to \(g=2\); A must be expanded again, producing the optimal route S → B → A → G with cost 5. The fixture expects one reopening.

`heuristic_audit` computes true cost-to-go with reverse Dijkstra, checks every reachable node for overestimation, checks every directed edge for consistency, and checks exact zero at goals. Its numerical tolerance is stated in cost units. Finite heuristic values at nodes with no route to a goal do not prove those nodes reachable.

For a cheap portal, a previously valid geometric heuristic can overestimate. The tests add a cost-0.1 connection across a grid where the old distance lower bound was 2; the audit correctly rejects that lower bound for the modified graph.

Primary background: [Red Blob's A-star introduction](https://www.redblobgames.com/pathfinding/a-star/introduction.html) and [implementation discussion](https://www.redblobgames.com/pathfinding/a-star/implementation.html). The code and fixtures here are original small reference implementations.

## Reverse fields on directed graphs

For a set of goals \(T\), calculate

\[
D(u)=\min_{t\in T}d(u,t).
\]

Start Dijkstra from all goals at distance zero and traverse incoming edges. When relaxing original edge \(u\to v\), use

\[
D(u)\leftarrow \min(D(u),\,c(u,v)+D(v)).
\]

Retain the original edge cost. Reversing endpoints and then recomputing a destination-entry terrain cost would change the modeled graph.

In the directed fixture A → B costs 2, B → G costs 3, G → A costs 100, A → H costs 9, and C → H costs 1. With goals G and H, the field is:

| Node | Cost to nearest goal |
|---|---:|
| A | 5 |
| B | 3 |
| C | 1 |
| G | 0 |
| H | 0 |
| U | Unreachable |

Running ordinary forward search outward from G would not answer these directed cost-to-go queries.

### Zero-cost cycles

The zero-cycle fixture contains A ↔ B and B ↔ C with cost zero, plus C → G costing 2. A, B and C all have distance 2. Choosing an arbitrary neighbor of equal distance after computing the field can produce an endless A ↔ B policy.

Instead, the kernel assigns successors during reverse Dijkstra relaxation, toward an already settled node. It preserves the first equal-cost successor. Following a successor strictly decreases settlement rank, including on zero-cost edges. The fixture follows A → B → C → G and terminates with cost 2.

The field returns null distance for unreachable nodes. Both a goal and an unreachable node have no successor; distinguish them by distance and goal membership.

## Grid costs and lower bounds

For generated grid edges:

\[
c(u,v)=\frac{\ell(u,v)}{v_0}m(v),
\]

where step length \(\ell\) is metres, reference speed \(v_0\) is m/s, and the positive destination multiplier \(m(v)\) is dimensionless. Cost is seconds. Different destination multipliers make opposite directions potentially have different costs.

Let cell size be \(a\), and \(m_{\min}\) the minimum multiplier across traversable cells. Define \(D=a\,m_{\min}/v_0\), the minimum cardinal-step time.

For integer coordinate differences \(\Delta x,\Delta y\):

\[
h_4=D(\Delta x+\Delta y),
\]

\[
h_8=D\left[\max(\Delta x,\Delta y)
+(\sqrt2-1)\min(\Delta x,\Delta y)\right].
\]

These bounds ignore obstacles and expensive cells, which can only increase cost under this adapter's rules. They include multipliers below one; using an assumed floor of one would overestimate on faster terrain.

Diagonal moves require both side-adjacent orthogonal cells to be traversable. In a 2×2 grid with the upper/right side cell blocked, the diagonal from one corner to the opposite is forbidden, and the remaining two-step route costs 2 instead of \(\sqrt2\).

The adapter represents point agents with a declared corner rule. It does not prove that a character of finite radius fits, handle headroom or slope, construct a navmesh, or guarantee that interpolating between waypoints remains collision-free.

## Discrete schedule conflicts

Each agent path lists occupancy at ticks 0,1,2,…; repeated nodes mean waiting. The checker reports:

- A vertex conflict when two agents occupy the same node at the same tick.
- An edge-swap conflict when two agents exchange endpoints over one tick.

By default an agent remains at its last node until the longest supplied schedule ends. With `stay_at_goal=False`, it disappears after its last listed occupancy. Choose this policy explicitly when comparing algorithms.

The example Alice: A → B and Bob: B → A has an edge swap at tick 0. The paths Alice: A → B and Bob: B → C are allowed by this checker, because following into a vacated node is allowed in its conflict model.

The checker does not validate graph connectivity, positive travel duration, edge capacity, diagonal geometric crossings, finite body size, acceleration or continuous-time collisions. No conflict reported means only that the selected discrete checks passed. It is not a guarantee of safe movement and is not a cooperative pathfinding solver.

## Verification and limits

The supplied suite contains 41 test methods. It checks analytical fixture results, edge identity, input-order stability, directed fields, zero-cost termination, stale-snapshot rejection, budget outcomes, invalid/nonfinite inputs, grid corner rules, heuristic failures and discrete conflicts.

One test generates 60 small directed graphs with a fixed seed and compares searches from every node against an independent Bellman–Ford relaxation oracle. This checks both Dijkstra and A-star with varied admissible heuristics. It is reproducible testing, not a performance benchmark or proof over every possible input.

The module uses ordinary floating-point arithmetic and rejects nonfinite accumulated costs. The theoretical optimality conditions assume exact comparisons; extremely close costs and large magnitude ranges require a deliberate numerical policy. The snapshot hash and deterministic insertion order do not establish cross-platform deterministic gameplay.

For a real implementation, add geometry, agent-profile constraints, world revisions, update scheduling, cancellation/resumption, memory budgets and scenario tests appropriate to that game. Add navmesh/funnel, dynamic-search or multi-agent solvers only when the required behavior calls for them.
