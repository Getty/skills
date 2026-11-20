# Validation, debugging and benchmarks

Verify the represented problem, algorithm and execution separately. A shortest graph path can still be physically unusable; a physically valid route can still optimize the wrong objective.

## Contents

- [Define correctness](#define-correctness)
- [Run the reference checks](#run-the-reference-checks)
- [Select focused scenarios](#select-focused-scenarios)
- [Audit heuristics and fields](#audit-heuristics-and-fields)
- [Use external benchmarks correctly](#use-external-benchmarks-correctly)
- [Measure meaningful performance](#measure-meaningful-performance)
- [Diagnose common failures](#diagnose-common-failures)

## Define correctness

Record:

- Graph/state representation and finite-agent geometry assumptions.
- Allowed moves and directed/parallel edge semantics.
- Cost objective and units.
- Start/goal validity and arrival definition.
- Static snapshot, graph revision or explicit temporal model.
- Algorithm guarantee and heuristic assumptions.
- Local avoidance/reservation conflict model when enabled.

For a returned graph route, check every edge exists and is executable under the query profile, endpoints connect, the goal is accepted and the reported cost equals the chosen edge sum. Check zero-length start=goal separately.

For a continuous route, additionally validate clearance and movement constraints along the swept trajectory. A point waypoint list alone does not certify finite-radius motion.

## Run the reference checks

From the skill directory:

~~~bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_navigation_reference.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/navigation_reference.py demo
PYTHONDONTWRITEBYTECODE=1 python3 scripts/navigation_reference.py audit
~~~

Read [numerical examples](numerical-examples.md) for exact APIs and supported fixture schemas. These utilities implement small finite-graph searches and checks. They are not navmesh builders, complete crowd planners or engine integrations.

The bundled suite uses analytical examples and an independent Bellman–Ford oracle on deterministic generated graphs. Comparing only A* against Dijkstra implemented by the same kernel can miss a shared defect; independent reasoning and a different algorithm help expose that risk.

## Select focused scenarios

| Scenario | Required property |
|---|---|
| Start equals goal | Found with zero cost and no movement |
| Disconnected goal | Unreachable only after complete search under the stated model |
| Expensive direct edge, cheap detour | Choose minimum cost, not first discovered goal |
| Directed door or drop | Outward and return reachability may differ |
| Parallel door/jump edges | Preserve the chosen action identity |
| Admissible inconsistent heuristic | Reopen improved expanded states |
| Zero-cost cycle | Search and extracted policy terminate |
| Cheap teleport | Recheck geometric heuristic admissibility |
| Eight-neighbor grid corner | Enforce the declared corner rule |
| Two actor radii at a narrow opening | Profile-specific traversability |
| Vehicle at a tight turn | Heading and motion feasibility, not just centerline clearance |
| Weighted terrain smoothing | Recompute objective and swept collision validity |
| Door closes during a query | Snapshot/revision handling and safe publication |
| Cheaper bridge opens off old route | Distinguish feasible cache from optimal cache |
| New intent while old query runs | Ignore obsolete completion |
| Unloaded region | Report missing coverage rather than global unreachability |
| Two agents swap a narrow edge | Detect or prevent the selected conflict |
| Goal remains occupied | Respect stay/disappear/terminal-occupancy policy |
| Delayed arrival to reserved passage | Repair coordination before unsafe execution |
| Save/load after navmesh rebuild | Revalidate intent and stable references |

Choose tests for the implemented capabilities. The table is a scenario catalog; it does not claim the bundled scripts execute every row.

## Audit heuristics and fields

On small finite graphs, compute exact goal distances with reverse Dijkstra and check:

\[
0\le h(u)\le d^*(u,T),\qquad h(t)=0\quad(t\in T),
\]

\[
h(u)\le c(u,v)+h(v)\quad\text{for every allowed directed edge}.
\]

Treat admissibility and consistency as separate results. A function name such as Manhattan or Euclidean does not establish either property for a graph containing special links or different costs.

For a reverse field, check every selected successor satisfies

\[
D(u)=c(u,v)+D(v)
\]

within the stated numerical policy. Also require policy termination; equality alone permits cycles on zero-cost edges. The bundled implementation uses settlement rank to break that ambiguity.

Keep unreachable values explicit. Do not evaluate infinity minus infinity in landmark differences or mistake a missing successor at a goal for an unreachable state.

Test properties under permutation of node/edge input order, graph relabeling and uniformly scaled costs/heuristics. Compare cost and validity, not a particular optimal tie route, unless stable tie behavior is a documented API requirement.

## Use external benchmarks correctly

[Moving AI](https://www.movingai.com/benchmarks/) provides reusable pathfinding datasets. Read the [format and movement assumptions](https://www.movingai.com/benchmarks/formats.html) before comparing against supplied scenario lengths.

For its documented grid scenarios, diagonal costs and corner rules matter; coordinate orientation and terrain symbols also require explicit interpretation. Do not load every non-wall character as an identical walkable tile and assume every benchmark's original semantics are preserved.

Record dataset version/source, parser version, movement model, query subset and any transformations. Keep downloaded datasets separate from synthetic fixtures and comply with their attribution/license terms.

For MAPF benchmarks, additionally record conflict definitions, goal occupancy, wait actions, objective (sum of costs or makespan), time horizon and timeout policy. Do not compare solvers solving different conflict models as if their costs were interchangeable.

Avoid bundling large externally sourced map collections in this skill. Use small original fixtures and pointers to obtain the desired datasets.

## Measure meaningful performance

Report at least:

- Valid solved fraction and reasons for noncompletion.
- Cost ratio or difference against an appropriate oracle/bound.
- Median and tail query latency, including/excluding queue time explicitly.
- Expanded states, queue operations and memory peaks.
- Graph preprocessing/update cost and amortization workload.
- Navmesh/collision rebuild cost where relevant.
- Replanning and movement failure frequency under dynamic scenarios.

Warm/cold cache, debug/release builds, hardware, compiler/runtime, threading and random seeds affect results. Record them. Exclude setup only if that exclusion is stated and appropriate to the actual game.

For approximate planners, compare speed at a stated quality level. An invalid shortcut or an unreported partial route is not a speed improvement.

A finite benchmark suite supplies evidence for its tested workload, not a universal best algorithm. Add a targeted scenario when a real failure exposes a missing assumption; do not accumulate tests solely to raise a count.

## Diagnose common failures

| Symptom | Check first |
|---|---|
| A* returns expensive route | Early goal discovery exit, overestimating heuristic, missing reopen, wrong cost units |
| Correct route in one direction only | Directed edge semantics and reversed field costs |
| Flow arrows loop | Equal-distance zero-cost tie policy |
| Agent clips a corner | Point graph versus body clearance, diagonal rule, smoothing |
| Agent reaches building but cannot work | Goal center versus valid interaction entrance/slot |
| Small door change causes frame spike | Rebuild scope, query bursts, duplicated work |
| Old route overwrites new task | Missing intent/query version check |
| Crowd blocks forever | Coordination/progress policy, not necessarily global path search |
| Empty path after engine startup | Navigation data readiness, start/goal projection, status details |
| World edit is visible but route fails | Collision/navigation revision mismatch |
| Fastest-route result looks longer | Distance versus time objective |
| Cached heuristic breaks after bridge opens | Cost-decrease/new-edge lower-bound invalidation |

Inspect graph edges, costs, heuristic values, profile filters, expanded states, portal geometry, current corridor, reservation intervals and query versions. Make units and status visible in debugging tools.
