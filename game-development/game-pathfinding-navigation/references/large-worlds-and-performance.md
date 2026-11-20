# Large worlds, shared work and performance

Optimize a measured workload while preserving the stated route guarantees. A larger algorithm catalog does not establish a faster implementation.

## Contents

- [Measure the workload](#measure-the-workload)
- [Share compatible work](#share-compatible-work)
- [Cache with explicit validity](#cache-with-explicit-validity)
- [Use hierarchy deliberately](#use-hierarchy-deliberately)
- [Handle streaming and missing detail](#handle-streaming-and-missing-detail)
- [Bound memory and scheduling](#bound-memory-and-scheduling)

## Measure the workload

Separate costs of:

- Building/updating the navigation representation.
- Mapping world positions to valid states.
- Waiting in the query queue.
- Searching and reconstructing a route.
- Geometric corridor processing/smoothing.
- Following the route and avoiding other actors.
- Replanning after changes.

Record graph size, traversable edge count, queries per simulation interval, agent profiles, start/goal distribution, update frequency and hardware. Measure percentiles and worst relevant cases, not just average successful short routes.

A maze, an open field, a disconnected map and a highly dynamic door network stress different mechanisms. Include unsolvable cases and bursts after world edits.

Do not compare algorithms using different movement costs, corner-cutting rules, agent radii or path-quality targets and attribute the difference to the search algorithm alone.

## Share compatible work

For many agents moving toward the same goal or eligible goal set, compute a distance-to-go field by reverse traversal of the directed graph. The local policy is

\[
\pi(u)\in\arg\min_{u\to v}\{c(u,v)+D(v)\}.
\]

Here \(D(u)\) is the cost to a goal. On a weighted graph, selecting merely the neighbor with the smallest \(D(v)\) can be wrong because the transition cost also matters.

**Original example:** from \(u\), an edge to \(v\) costs 100 with \(D(v)=1\), while an edge to \(w\) costs 1 with \(D(w)=3\). Choose \(w\), total cost 4, rather than \(v\), total cost 101.

On strictly positive-cost edges, a shortest-path successor reduces distance. With zero-cost edges, equal-distance successors can cycle. Use a successor tree/rank produced during reverse search or another acyclic tie policy; do not choose arbitrary equal-valued neighbors every frame.

Share a field only when the graph eligibility and cost semantics match. Profiles can sometimes share a valid lower-bound field while requiring separate exact policies. Explain that distinction.

The [Red Blob flow-field article](https://www.redblobgames.com/pathfinding/tower-defense/) motivates shared work for many starts and one goal. The directed weighted policy and cache rules here make the contract explicit.

### Interpolation is a separate operation

A discrete policy arrow is an executable neighbor decision. Interpolating arrows into a smooth vector field can point through an obstacle or across an invalid portal. Constrain continuous steering to traversable geometry and validate the result for finite-radius agents.

## Cache with explicit validity

Key reusable results by relevant graph/topology revision, cost model, agent profile, goal definition and movement rules. A route keyed only by start and goal is insufficient if doors, water or permissions changed.

Cache different objects deliberately:

| Cached object | Main validity dependency |
|---|---|
| Path/corridor | Transition feasibility; costs/other routes if optimality matters |
| Distance field | Full graph/cost/goal set under its coverage |
| Landmark lower bounds | Lower-bound assumptions after edge/cost changes |
| Local portal-to-portal route | Local region geometry/cost/profile |
| Position-to-state lookup | Geometry and coordinate mapping |
| Connectivity summary | Directionality, profile and updated topology |

An old valid path can be useful even when suboptimal. Label that policy. Keep a safe execution check near upcoming transitions.

Avoid caching a budget failure as unreachable. A query that ran out of memory or lacked a loaded tile did not establish the absence of a route.

## Use hierarchy deliberately

Partition the navigation domain into regions and connect meaningful portals. A coarse query selects a route through regions; local queries realize portal transitions.

The abstraction must retain the routes relevant to the agent. A narrow crossing omitted at the coarse level cannot be recovered by a better local A* search.

Choose whether coarse edge costs are:

- Exact local costs for the represented portal states.
- Lower bounds used to guide a finer search.
- Approximate estimates accepted for a declared quality tradeoff.

Do not interchange these meanings. A hierarchy with reduced entrances can trade quality for speed; it is not automatically globally optimal.

Cache local routes only for matching profiles and revisions. A new wall can invalidate portal costs even if the region's outer boundary stays unchanged. A bridge can connect previously separate coarse regions.

Use [accelerated and hierarchical search](accelerated-and-hierarchical-search.md) for HPA*, landmarks and specialized algorithms. A world organized into chunks does not require hierarchical search if ordinary queries remain inexpensive.

## Handle streaming and missing detail

Keep enough coarse connectivity to plan across unloaded regions, or explicitly limit query coverage. Return “detail unavailable” or a staged route to a validated boundary when appropriate.

Do not treat an unloaded region as an impassable wall and then report global unreachability. Do not assume it is empty space either.

A useful staged policy is:

1. Plan to a stable destination using coarse region/portal data.
2. Load or generate detail ahead of movement.
3. Refine the next corridor against current geometry.
4. Replan if the detailed route cannot realize the coarse assumption.

State whether the coarse plan is guaranteed realizable or only an estimate. Keep actors out of a segment until its required detail and collision are ready.

Reattach plans using stable world/portal identities. Transient navmesh references can change when tiles are rebuilt or streamed. Preserve high-level intent rather than treating raw polygon handles as permanent save data.

## Bound memory and scheduling

Use compact node IDs/arrays where graph ownership permits it, and store query-local data without clearing the entire world unnecessarily. Generation stamps can help, but handle wraparound and concurrent query ownership.

Lazy heaps can contain duplicate stale entries. Measure memory peaks; use a different queue structure only when justified. Reopening with inconsistent heuristics can cause additional expansions, so avoid promising the simplest Dijkstra complexity bound for every A* configuration.

Cap outstanding requests, cancel superseded work and avoid starving low-priority actors. Reuse one shared field where justified rather than submitting identical searches for a crowd.

Use benchmark reports that include path validity and cost quality alongside time and memory. A planner that returns a wrong route quickly has not met the workload.

### Primary references

- [Moving AI benchmarks](https://www.movingai.com/benchmarks/) — reproducible graph-search problems.
- [Moving AI formats](https://www.movingai.com/benchmarks/formats.html) — movement assumptions and scenario interpretation.
- [Recast/Detour](https://github.com/recastnavigation/recastnavigation) — optional tiled navigation and runtime query implementation.

The scheduling, streaming and cache policies above are original engineering recommendations.
