# Graphs, costs and agent profiles

Define a correct planning problem before optimizing its search. Shortest-path correctness applies to the represented graph and objective; it does not establish that the graph matches the physical world.

## Contents

- [Represent sufficient state](#represent-sufficient-state)
- [Separate facts from eligibility](#separate-facts-from-eligibility)
- [Define the cost objective](#define-the-cost-objective)
- [Make direction and actions explicit](#make-direction-and-actions-explicit)
- [Choose valid lower bounds](#choose-valid-lower-bounds)
- [Represent goals and failure](#represent-goals-and-failure)
- [Validate the graph contract](#validate-the-graph-contract)

## Represent sufficient state

Let a directed graph be \(G=(V,E)\). Each edge \(u\to v\) represents an allowed state transition with finite nonnegative cost \(c(u,v)\) for the baseline algorithms.

Use location-only nodes when future legality and costs depend only on current location and fixed query parameters. Add state when that assumption fails:

- Heading or steering state for turning constraints.
- Movement mode for walking, swimming, flying or riding.
- Time when reservations or non-FIFO availability affect future choices.
- A bounded resource state when fuel or a consumable materially changes which transitions remain possible.

Do not put every personality trait or inventory item into the search node. Behavior selects a task and relevant constraints; navigation carries only what is necessary to evaluate its transitions. Complex world-changing action planning may need a separate planner.

Two routes reaching the same position are not interchangeable if one leaves a vehicle facing the wrong way or consumes the key needed later. Merging those states can discard the only feasible solution.

Red Blob's [implementation guide](https://www.redblobgames.com/pathfinding/a-star/implementation.html) explicitly treats locations as potentially richer search states and supports directed connections. The design examples here are original applications.

## Separate facts from eligibility

Terrain/buildings supply geometry and observed state. Navigation evaluates them for the query's agent:

| Supplied fact | Agent-dependent interpretation |
|---|---|
| Passage width and shape | Does the body footprint fit throughout the motion? |
| Ceiling/overhang | Is headroom sufficient for this posture? |
| Rise, run and step geometry | Does this movement mode support the slope/step? |
| Water depth and current | Wading, swimming, boating or impassable |
| Door state and available action | Pass, open with an action, wait, or reject |
| Surface/road condition | Speed/cost and perhaps traction constraints |
| Bridge/loading limit | Eligibility for this vehicle/load |

Store a stable profile ID and a version/hash of relevant properties in cache keys. A profile's name is not sufficient if its radius, capabilities or speed table changes.

For horizontal run \(r>0\) and rise \(\Delta z\),

\[
s=\frac{\Delta z}{r},\qquad \theta=\arctan(s).
\]

The signed grade \(s\) is dimensionless; the angle is in radians internally. Uphill and downhill cost can differ. A slope at cell centers does not certify a clear route through an unresolved cliff, stair or narrow obstacle.

**Synthetic example:** a 1 m rise over 4 m horizontal distance has grade 0.25 and angle approximately \(14.04^\circ\). Eligibility still depends on the actual surface and agent movement model. These numbers do not establish a universal walkable angle.

## Define the cost objective

For travel time along an executable edge:

\[
c_t(e)=\int_e \frac{1}{v_a(x)}\,ds+t_{\mathrm{action}}(e).
\]

Distance \(ds\) is metres, speed \(v_a>0\) is metres/second, and action time is seconds. A constant-speed segment reduces to \(\ell/v+t_{\mathrm{action}}\). Use the actual traversal direction and relevant agent state.

A weighted game objective can be

\[
c(e)=c_t(e)+\sum_j \lambda_jp_j(e),\qquad c(e)\ge0.
\]

Give every \(p_j\) and \(\lambda_j\) a declared meaning and compatible units. If penalties are expressed as equivalent seconds, the result is a preference score; it need not equal predicted physical travel time. Return travel-time estimate separately when callers need it.

**Synthetic example:** a 12 m road at 2 m/s costs 6 s. A geometrically shorter 8 m mud route at 0.8 m/s costs 10 s. A least-time planner chooses the road; a least-distance planner chooses the mud route. Neither objective is universally correct.

Do not add an arbitrary constant to every edge to eliminate negative costs: paths with different edge counts change relative cost. Avoid negative rewards in a baseline Dijkstra/A* graph. If the design truly needs negative costs, select an appropriate model/algorithm and handle negative cycles explicitly.

Represent impassability by removing/disabling a transition. A very large finite cost still permits crossing when every alternative is worse. Do not divide by zero speed to manufacture an infinity.

### Cost placement matters

Document whether a terrain weight is charged on entry, exit, per edge length or by integration along the edge. Entry costs generally make reverse traversal use a different cost. Refining a grid changes results if a fixed per-cell fee is accidentally interpreted as a per-metre cost.

For a spatial cost density \(w(x)\ [\mathrm{cost/m}]\),

\[
c(e)=\int_e w(x)\,ds.
\]

An endpoint average is an approximation, not exact integration through a sharp terrain boundary. Smoothing a path may shorten its geometry while increasing this integral.

## Make direction and actions explicit

Store one-way drops, doors, currents, road directions and mode switches as directed transitions. Do not infer a reverse edge unless the movement model actually permits it.

For cost-to-go fields, reverse edge connectivity while retaining the original forward edge cost: the reverse arc \(v\to u\) carries \(c(u,v)\). It must not substitute \(c(v,u)\), which may differ or not exist.

An edge should carry enough action semantics for execution: walk corridor, open door, jump, climb, board lift, disembark, or teleport. Include its preconditions and a stable identifier for revalidation.

If opening a door changes future world state, choose the intended approximation. Charging its opening time on each traversal may be a conservative repeated-action model; a planner that reasons about opening it once and reusing it needs additional state or coordination. Do not silently mix those semantics.

Parallel edges can represent distinct actions between the same states. A small helper that accepts only one cost per pair has a narrower schema; reduce parallel actions to the minimum only when their outcomes and future state are truly equivalent.

## Choose valid lower bounds

If every movement edge obeys \(c_t(e)\ge\ell(e)/v_{\max}\), and no special connection defeats the geometric bound, then

\[
h(x)=\frac{\|x-x_g\|}{v_{\max}}
\]

is a useful travel-time lower bound. Include the fastest available legal movement in \(v_{\max}\), not the average walking speed.

For a distance objective with cost per distance bounded below by \(w_{\min}\ge0\),

\[
h(x)=w_{\min}\|x-x_g\|.
\]

If \(w_{\min}=0\), this bound becomes zero. A cheap teleport, an incorrect coordinate scale or a faster movement mode can invalidate a previously admissible geometric heuristic.

For a goal set \(T\), lower bounds can use \(\min_{t\in T}h_t(x)\) when each \(h_t\) is valid under the same query model. A large goal region needs a distance-to-region bound, not necessarily distance to its center.

See [search and heuristics](search-and-heuristics.md) for admissibility, consistency and reopening. Never tune heuristic scale independently from the objective's units without changing the stated guarantee.

## Represent goals and failure

Distinguish an interaction target from a valid destination. A building's center may lie inside blocked geometry. Supply reachable entrance states, an interaction region or a compatible closest-point policy.

Use explicit outcomes:

- Found an accepted goal.
- No path exists in the complete searched snapshot graph.
- Budget exhausted or query cancelled.
- Input invalid or start/goal projection failed.
- Snapshot stale.
- A useful partial route, with its endpoint and non-success status.

Do not equate budget exhaustion, missing streamed data or a temporary reservation horizon with global unreachability.

Connected-component labels are a fast rejection test only under their graph assumptions. Undirected connectivity does not establish directed reachability. Different strongly connected components may still have a one-way route between them.

## Validate the graph contract

Check finite costs, valid IDs, actual endpoints, stable units, directed transitions and profile-specific eligibility. Validate a start already at its goal, isolated start, inaccessible goal, one-way return trip, zero-cost transition and a cheaper longer route.

For continuous execution, validate clearance along the entire swept path. A graph's optimal route can still fail if its edges were not physically validated.

### Bundled profile data

Use `assets/agent-profiles-example.json` only as synthetic examples of profile shape and unit conventions. They are not human biomechanics, vehicle specifications or calibrated game balance. The numerical search helpers operate on already constructed graphs and do not implement all profile filters.
