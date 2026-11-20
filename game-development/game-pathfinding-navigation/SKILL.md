---
name: game-pathfinding-navigation
description: "Use when implementing or debugging game pathfinding and navigation — A*, Dijkstra, grids, navmeshes, flow fields, D* Lite replanning, hierarchical routes, clearance, local avoidance, multi-agent pathfinding, streamed worlds, engine navigation adapters."
---

# Game Pathfinding and Navigation

Choose the smallest navigation model that meets the game's observable requirements. Keep advanced search, navmeshes, crowd coordination and temporal planning optional.

Keep terrain/material/water simulation, building lifecycle, resource logistics and population needs outside this skill. Consume their geometry, constraints and goals through explicit adapters. Do not require a separate terrain skill to navigate a flat or indoor world.

## Start with the planning contract

1. Inspect the project's current graph, movement model, engine and instructions.
2. Identify agent shape/capabilities, accepted goals, cost objective, dynamic changes and workload.
3. Distinguish goal selection, route planning, path execution and coordination.
4. If details are absent, assume a finite static snapshot graph with nonnegative costs, one agent and one goal. Use Dijkstra or A* with a justified lower bound; h=0 is a valid fallback.
5. State assumptions and continue. Do not require every parameter or algorithm from this knowledge base.
6. Read [scope and representation](references/scope-and-representation.md) and only the task-relevant references below.

## Route to the relevant material

| Task | Reference |
|---|---|
| Choose a simple model, grid/graph/navmesh or richer state | [Scope and representation](references/scope-and-representation.md) |
| Define agent profiles, costs, direction, actions and goal sets | [Graphs, costs and agent profiles](references/graphs-costs-and-agent-profiles.md) |
| Implement BFS/Dijkstra/A*, lower bounds, reopening or weighted search | [Search and heuristics](references/search-and-heuristics.md) |
| Consider ALT, hierarchy, JPS, Theta* or bidirectional search | [Accelerated and hierarchical search](references/accelerated-and-hierarchical-search.md) |
| Repair changing paths or model schedules/time-dependent edges | [Incremental and time-dependent search](references/incremental-and-time-dependent-search.md) |
| Build/query polygon corridors, clearance and funnel paths | [Navmeshes and clearance](references/navmeshes-and-clearance.md) |
| Follow routes, steer, brake, avoid actors and recover from blockage | [Movement and local avoidance](references/movement-and-local-avoidance.md) |
| Share narrow spaces, reserve time or select a MAPF model | [Multi-agent planning and reservations](references/multi-agent-and-reservations.md) |
| Handle edits, async results, stale snapshots and save/load | [Dynamic worlds and runtime](references/dynamic-world-and-runtime.md) |
| Share fields, cache queries, stream regions or measure performance | [Large worlds and performance](references/large-worlds-and-performance.md) |
| Connect terrain, buildings, logistics and behavior | [Domain contracts](references/domain-contracts.md) |
| Integrate optional Recast, Unity, Unreal or Godot adapters | [Engine adapters](references/engine-adapters.md) |
| Find symbol/unit conventions and mathematical assumptions | [Formulas and units](references/formulas-and-units.md) |
| Run reference searches, fields, grids and conflict checks | [Numerical examples](references/numerical-examples.md) |
| Verify routes, heuristics, execution and benchmarks | [Validation and benchmarks](references/validation-and-benchmarks.md) |
| Consult primary papers, author code and official documentation | [Sources and models](references/sources-and-models.md) |

## Preserve correctness conditions

- Define states rich enough for future costs/legality; do not merge different headings or temporal states when they matter.
- Use one cost objective and compatible units for g, h and edge costs.
- Reject negative/nonfinite costs in the baseline Dijkstra/A* model. Represent forbidden edges as absent.
- For exact A*, use a justified admissible heuristic, zero at goals, and reopen improved states when consistency is not guaranteed.
- Stop on a valid minimum-priority goal removal, not first discovery. Skip obsolete heap entries.
- Keep graph/profile/goal semantics coherent during each query or use a correctly implemented repair method.
- For directed cost-to-go fields, reverse connectivity while retaining each original forward cost.
- Ensure extracted policies terminate even with zero-cost edges.
- Separate path feasibility from optimality; a new shortcut can invalidate an optimum without touching the old path.
- Respect finite-agent geometry and executable actions. Polygon-center adjacency is not a clearance certificate.
- State the selected corridor and cost assumptions for funnel/smoothing claims.
- Distinguish local avoidance, discrete reservation conflict checks and continuous collision safety.
- Keep found, unreachable, partial, budget exhausted, cancelled, invalid and stale outcomes distinct as applicable.
- Preserve world/intent identities and revisions; do not treat temporary engine polygon handles as durable save IDs.

Apply these conditions to included mechanisms. Do not demand a full navmesh, D* Lite, ORCA or joint multi-agent solver for a simple grid game.

## Use a bounded implementation workflow

1. Write the graph/agent/objective contract and deliberate omissions.
2. Build a small validated graph or adapter with known expected paths.
3. Implement a reference search and appropriate status handling.
4. Add heuristic or shared-field optimization only with its assumptions.
5. Connect output to movement and goal/action completion.
6. Add world-change invalidation and publication readiness.
7. Verify cost/edge validity, one failure case and one representative dynamic or geometry case when relevant.
8. Profile actual bottlenecks before adding hierarchy, incremental repair or joint scheduling.
9. Report the implemented guarantee, tests actually run and remaining model limits.

For conceptual requests, provide the design and examples without manufacturing a full engine. For implementation requests, carry through to working code and meaningful verification.

## Use the bundled utilities and data

Run from this skill's directory:

~~~bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/navigation_reference.py demo
PYTHONDONTWRITEBYTECODE=1 python3 scripts/navigation_reference.py audit
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_navigation_reference.py
~~~

The original standard-library Python utilities provide directed graph A*/Dijkstra with reopening, reverse multi-source fields, heuristic auditing, a 4/8-neighbor grid adapter and discrete schedule conflict checks. Read [numerical examples](references/numerical-examples.md) for their exact API, scope and expected outputs.

Use the assets as examples, not mandatory production schemas:

- [Search fixtures](assets/search-fixtures.json): analytical graph cases and expected outcomes.
- [Grid fixtures](assets/grid-fixtures.json): costs, diagonal rules and disconnection.
- [Agent profiles](assets/agent-profiles-example.json): synthetic shape/capability/cost records.
- [Query contract](assets/query-contract-example.json): illustrative intent, revisions and status.

The utilities do not build navmeshes, prove finite-radius trajectory safety, implement ORCA/CBS/D* Lite or replace engine integration. Synthetic speeds and dimensions are not calibrated human/vehicle data.

## Keep boundaries and evidence explicit

Let behavior choose why/where to move; let navigation find a compatible route; let movement execute it. Let terrain supply water depth and slope, while the profile determines whether and how they can be crossed.

Use primary papers/author implementations for algorithm guarantees and official documentation for engine behavior. Verify current installed API versions during implementation. Distinguish theory, a numerical approximation, a designer policy and a measured benchmark result.

Do not claim a universal fastest algorithm, global navmesh optimality from a corridor funnel, deadlock freedom from local avoidance, or global unreachability from a timeout. Keep extensions optional and document their additional state, update cost and assumptions.
