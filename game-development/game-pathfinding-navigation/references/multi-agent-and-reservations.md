# Multiple agents, bottlenecks and reservations

Use coordination only when agents compete for space or timed traversal in ways that independent routes cannot adequately handle. Many games need ordinary routing plus collision-aware movement; a full multi-agent planner is optional.

## Contents

- [Choose the coordination level](#choose-the-coordination-level)
- [Define the problem before choosing a solver](#define-the-problem-before-choosing-a-solver)
- [Represent conflicts explicitly](#represent-conflicts-explicitly)
- [Reserve intervals and capacity](#reserve-intervals-and-capacity)
- [Understand prioritized planning](#understand-prioritized-planning)
- [Use CBS with the right contract](#use-cbs-with-the-right-contract)
- [Connect plans to actual execution](#connect-plans-to-actual-execution)
- [Validate coordination](#validate-coordination)

## Choose the coordination level

| Approach | Suitable behavior | Important limit |
|---|---|---|
| Independent routes | Sparse agents, crossings handled by movement | Routes may conflict in time |
| Routes plus local avoidance | Continuous pedestrian-like traffic | No general guarantee of global progress |
| Queue/token at bottlenecks | Doors, lifts, narrow bridges | Needs safe waiting locations and fairness |
| Prioritized space-time planning | Moderate coordinated traffic | Fixed priority can fail despite a joint solution |
| Conflict-based/joint planning | Precise conflict-free schedules | Larger computation and explicit model assumptions |
| Windowed coordination | Bounded online workload | Horizon limits and future deadlock require policy |

Keep assignment separate: deciding who carries which crate or which worker takes a job belongs to logistics/task allocation. Navigation receives goals and capabilities. It may expose travel estimates or infeasibility back to that system.

## Define the problem before choosing a solver

Record the graph, movement duration, collision model, objective, start times, goal behavior and allowed waits. The [MAPF definitions paper](https://ojs.aaai.org/index.php/SOCS/article/view/18510) documents why changing those assumptions changes the problem being solved.

For a simple discrete model, agent \(i\) occupies node \(v_i(t)\) at integer timestep \(t\) and moves along an allowed edge or waits during \(t\rightarrow t+1\). A state is \((v,t)\), not just \(v\), because arriving at the same place at a different time may be feasible.

Choose the objective:

\[
\mathrm{makespan}=\max_i T_i,\qquad
\mathrm{sum\ of\ arrival\ times}=\sum_i T_i,
\]

where \(T_i\) is the agent's arrival time measured from the declared time origin. For unit-duration moves these are timestep counts; multiply by step duration for seconds. Weighted traversal costs are a different objective unless they equal time.

Specify whether agents remain at goals or disappear after arrival. Remaining at a goal can block a corridor indefinitely. When calculating arrival-based cost, do not accidentally charge every padded post-arrival wait as additional travel while simultaneously claiming the arrival-time objective.

## Represent conflicts explicitly

For the simple node/edge model:

- **Vertex conflict:** \(v_i(t)=v_j(t)\) when node capacity is one.
- **Opposite-edge swap:** \(v_i(t)=v_j(t+1)\) and \(v_i(t+1)=v_j(t)\), with different endpoints.
- **Following conflict:** one agent enters a node just vacated by another; allowing or forbidding this is a model choice.
- **Swept-geometry conflict:** bodies or trajectories overlap between discrete states, including diagonal crossings.

Vertex checks alone miss opposite-edge swaps. Checking swaps alone still misses diagonal trajectories crossing in an open square. A discrete solution for point agents does not automatically certify finite-radius continuous motion.

If a movement takes several ticks, reserve its swept occupancy over the actual interval. Waiting is also occupancy. Ladders, doors, elevators and docking maneuvers can require resource reservations in addition to geometric clearance.

For continuous linear motion over one interval, relative-position collision checks can help verify execution; use the constant-velocity assumptions and finite-body treatment in the movement reference. More complex trajectories require an appropriate swept-volume test.

## Reserve intervals and capacity

A practical reservation can contain:

- Resource/node/connection ID and navigation revision.
- Agent/operation ID.
- Start and end time with an explicit boundary convention.
- Capacity demand, direction and relevant footprint/profile.
- Tentative, committed, entered, released or expired state.

For resource capacity \(K\),

\[
\sum_{r\ \mathrm{active\ at}\ t}k_r\le K.
\]

Use half-open intervals \([t_{\mathrm{in}},t_{\mathrm{out}})\) only when that convention matches the modeled handoff. Add temporal/spatial separation where finite bodies need it; algebraically touching intervals do not ensure two bodies clear a narrow doorway.

**Original example:** a one-agent doorway occupied during \([2.0,3.4)\) s cannot accept another entry at 3.2 s. With a chosen 0.2 s clearance buffer, its next entry is at or after 3.6 s. The buffer is a game/controller assumption, not a universal constant.

Reserve opposing travel on the same narrow connection together. Two separate directed-edge tables can otherwise authorize a head-on encounter. Capacity above one may require lanes, direction compatibility and physical dimensions rather than a single counter.

Commit a collection of reservations atomically or use a recoverable acquisition policy. Acquiring one scarce passage while holding another can create a resource deadlock. Provide safe waiting zones, release unused claims and prevent indefinite starvation through a declared fairness rule.

## Understand prioritized planning

Prioritized planning selects an agent order, plans the first agent, then plans later agents around existing reservations. It is often useful and simple. It is not generally complete or globally optimal.

**Original discrete example:** graph edges connect \(L-M-R\), with siding \(S\) attached to \(M\). Agent A starts at \(L\) and wants \(R\); B starts at \(R\) and wants \(L\). Nodes have capacity one; waits are allowed; vertex and opposite-edge conflicts are forbidden; agents remain at goals.

If A first reserves its shortest route \(L,M,R\) at times \(0,1,2\), B cannot vacate \(R\): arriving at \(M\) at time 1 collides with A, and moving \(R\rightarrow M\) during time 1–2 swaps edges with A. Nevertheless, a joint solution exists:

| Time | A | B |
|---:|---|---|
| 0 | L | R |
| 1 | M | R |
| 2 | S | M |
| 3 | S | L |
| 4 | M | L |
| 5 | R | L |

Its arrival-time sum is \(5+3=8\), and makespan is 5. This table demonstrates feasibility, not a proof of the minimum objective. It also uses the stated discrete following convention; finite bodies may require longer transition occupancy.

Repair options include changing priorities, replanning a small conflict group, adding a bounded backtracking policy, or choosing a different solver. Report a failed priority schedule as such; do not equate it with proof that the physical goal set is impossible.

## Use CBS with the right contract

Conflict-Based Search separates individual constrained searches from a higher-level conflict tree. A node contains constraints and the corresponding individual paths. When paths conflict, branch by constraining one participant in one child and the other participant in another, then recompute affected paths.

For sum-of-costs optimal CBS, low-level searches must optimize the same cost definition under their constraints, and the high-level ordering and conflict splitting must preserve the algorithm's assumptions. A conflict-free node selected by the specified search can then establish the model's optimal solution. Merely resolving the first observed conflict greedily is not CBS.

Use the authors' [CBS paper summary](https://www.movingai.com/papers/sharon2015cbsjournal.html) and [journal paper](https://doi.org/10.1016/j.artint.2014.11.006) for the complete algorithm and guarantees. Completeness, termination on infeasible problems, bounded-suboptimal variants and performance depend on the actual formulation and implementation. A finite search horizon restricts any feasibility claim to that horizon.

Encode edge conflicts as transition constraints, not only destination-node bans. Goal occupancy and constraints after apparent arrival must be respected. Continuous-time, finite-body or capacity-rich variants need matching conflict detection and constraints; do not copy discrete point-agent guarantees into them.

## Connect plans to actual execution

A schedule assumes agents follow its timing. Acceleration, collisions, animation, stalled machinery or a blocked door can break that assumption. Monitor actual entry/exit events; extend or revoke reservations under a consistent recovery policy before allowing conflicting entries.

Separate intended reservation time from actual occupancy. Expiry must not claim a physically occupied passage is empty merely because an agent is late. Conversely, retaining every stale claim forever creates artificial blockage.

Version reservations against topology and capability. A bridge collapse invalidates both routes and crossing reservations. A cost-only change may preserve physical feasibility while changing optimality. Revalidate the appropriate property instead of rebuilding everything indiscriminately.

Keep coordination state in the navigation/integration layer. Terrain reports changes in support and water; buildings report door/lift state; logistics reports a loaded vehicle's profile; task systems supply goals. None of those domains needs to own the multi-agent search algorithm.

## Validate coordination

Test swaps, crossings, following, waiting at goals, late execution, reservation cancellation, doorway capacity and the siding example. Check every reported schedule against an independent conflict validator using the same time/body model.

Measure success rate, completion time, objective cost, waits, deadlocks and solver budget. State timeout and horizon separately from “no solution.” Use [Moving AI MAPF benchmarks](https://www.movingai.com/benchmarks/mapf.html) for comparable research experiments only after matching their problem assumptions; retain attribution when redistributing data.

For a game with occasional traffic, a queue at the narrow bridge can be the right complete feature. Add general multi-agent search when the game's observable behavior requires coordinated planning beyond those local resources.
