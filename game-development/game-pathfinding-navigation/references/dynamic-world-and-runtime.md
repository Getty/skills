# Dynamic worlds and runtime navigation

Keep route searches, navigation rebuilds and actor movement consistent without assuming that all three finish in the same frame.

## Contents

- [Classify changes](#classify-changes)
- [Search a coherent snapshot](#search-a-coherent-snapshot)
- [Invalidate the correct dependency](#invalidate-the-correct-dependency)
- [Publish geometry safely](#publish-geometry-safely)
- [Schedule bounded work](#schedule-bounded-work)
- [Handle moving starts and targets](#handle-moving-starts-and-targets)
- [Save and restore intent](#save-and-restore-intent)

## Classify changes

| Change | Typical consequence |
|---|---|
| Terrain excavation or building placement | Rebuild affected traversable geometry and connections |
| Door opens/closes | Change an action/edge or its eligibility |
| Water rises or mud forms | Change profile-specific eligibility and/or costs |
| Temporary actor in a wide corridor | Local avoidance may suffice |
| Queue at a narrow lift or doorway | Capacity/time coordination may be needed |
| Agent changes size, equipment or movement mode | Reevaluate profile-dependent graph and caches |
| Destination moves or a job is cancelled | New intent/query; old result may be irrelevant |

Choose the response based on the mechanism. A short-lived moving actor need not trigger a whole navmesh rebuild. A permanent wall cannot be handled reliably by pretending it is only a temporary steering inconvenience.

## Search a coherent snapshot

A baseline A*/Dijkstra query assumes a fixed graph, cost function, profile and goal while it runs. Provide an immutable snapshot, read lock, versioned view or another coherent read mechanism.

Do not mutate graph edges under a running search and then claim the usual optimality guarantee. Cancel/restart, validate against a declared policy, or use a correctly implemented incremental method.

Record in the result:

- Query/intent ID.
- Agent profile and relevant version.
- Graph/geometry and cost revision.
- Goal definition/version.
- Path or corridor, action IDs and actual objective cost.
- Completion status, guarantee and resource use.
- Dependency information sufficient for the chosen revalidation policy.

An agent can submit a newer intent while an old search is running. Accept only a result that still belongs to the current intent, unless explicitly reusing it. Completion order must not overwrite a newer goal with an older route.

## Invalidate the correct dependency

Distinguish **feasibility**, **stored cost** and **optimality**.

- A blocked route edge can make the path infeasible.
- A higher cost on its route changes the score, even if still passable.
- A cheaper edge elsewhere can make the path suboptimal without affecting its physical validity.
- A newly opened shortcut can invalidate a global optimality claim far outside the old route's dependency list.

Checking only whether the cached path intersects a dirty region can preserve safety under appropriate edge validation, but cannot generally prove continued optimality.

Cached heuristic lower bounds also depend on changes. For the same states and cost semantics, old shortest-path distances remain lower bounds after only cost increases or edge removals. Cost decreases or new shortcuts can make old distances overestimates. Recompute, repair or fall back to a safe lower bound when their assumptions no longer hold.

Use local geometry revisions for invalidating affected collision/corridor segments. Use broader cost/topology revisions or proved dependency tracking for fields, landmarks and optimality guarantees. Do not assume a visually local edit has only local route consequences.

**Original example:** an agent's route costs 20 s and avoids a bridge. Opening that bridge creates a 12 s route. The old route remains executable, but a cache that inspects only old path edges cannot discover the improvement. Decide whether the game requires immediate replanning or tolerates a valid older route.

## Publish geometry safely

For a terrain or building edit:

1. Receive the committed physical change and its geometry revision.
2. Determine which agent profiles, navigation tiles/edges and boundaries are affected.
3. Rebuild or update the navigation representation against that revision.
4. Coordinate collision, action geometry and navigation readiness.
5. Publish a compatible usable revision.
6. Revalidate affected followers and queued queries.

Keep areas unavailable for actions that require unfinished projections, or atomically swap compatible data. Do not let an agent step onto a visually raised floor while collision still describes the old ground.

An asynchronous tile build may finish after another edit. Reject an obsolete build result or prove that its dependencies remain valid. Stable world IDs must remain distinct from transient navmesh polygon handles and dense array indices.

When an edit covers an agent's current position, define a recovery policy: delay the edit, evacuate, place the actor at a validated safe location, or fail the construction. Do not ask the planner to begin in invalid geometry without reporting that condition.

See [engine adapters](engine-adapters.md) for optional implementation examples and [domain contracts](domain-contracts.md) for ownership.

## Schedule bounded work

Separate simulation time, path-query CPU time and rendering frames. A ten-millisecond computation budget is not a ten-millisecond movement edge.

Possible scheduling policies:

- Immediate queries for small worlds.
- Expansion-limited slices retaining frontier/state between frames.
- A job queue with priority, cancellation and starvation protection.
- Shared fields for equivalent many-to-one requests.
- Incremental repair after measured recurring changes.

Keep the graph snapshot alive for a sliced query. If it expires, return a stale/cancelled status or restart under policy. Returning an unfinished best-so-far route must identify it as partial or suboptimal unless the algorithm proves a bound.

Measure queue delay, solve time, rebuild time, memory, expanded states and movement failures separately. Frame budget spikes often come from navmesh/collision rebuilding or large request bursts rather than the shortest-path loop.

Avoid a replan storm when one building changes: coalesce edits, cancel superseded requests, prioritize agents near an affected segment, and share compatible work. Do not hide invalid paths merely to reduce queue length.

## Handle moving starts and targets

Revalidate the first segment from the agent's current position. If the agent moved while a query ran, a route starting at its old sample may require a safe connection or a new query.

For moving targets, specify an acceptance region and query cadence. A pursuit/interception problem may need a motion prediction; repeatedly planning to the last visible position is a different model.

Use hysteresis or minimum improvement before replacing a still-useful route when appropriate. Declare the tradeoff: reduced oscillation and CPU work can accept a route that is no longer the current optimum.

Keep stuck detection measurable: progress along the route, elapsed simulation time, contact/velocity limits and blockage cause. Retry/backoff, yielding, local repair and task failure are separate outcomes. Replanning every frame is not a general deadlock solution.

## Save and restore intent

Persist authoritative actor position, movement mode, current goal/task reference and required action/coordination state. Treat a route as a cache unless exact resumption requires it.

On load, rebuild or validate the navigation representation, remap stable references, check goal eligibility and replan when caches are incompatible. Do not serialize only transient engine polygon references and assume they survive a rebuild.

Persist reservations only if their time/ownership semantics require it. Resume them against the saved simulation clock; expire or reconcile abandoned claims. A resource reservation belonging to logistics is not automatically a navigation reservation.

Record solver/graph versions when deterministic replay matters. Stable ordering helps reproducibility, but cross-platform bit-identical results require deliberate engineering and testing.

### Source basis

This reference is original runtime architecture guidance. [Recast/Detour](https://github.com/recastnavigation/recastnavigation) supplies an implementation family for navmesh queries, tiles and movement; [D* Lite](https://idm-lab.org/bib/abstracts/Koen02e.html) is a primary incremental-planning reference. Neither makes arbitrary concurrent graph mutation safe by itself.
