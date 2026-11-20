# Incremental replanning and time-dependent routes

Distinguish a graph that changes between queries from a transition whose availability or cost depends on arrival time. They need different state and algorithms.

## Contents

- [Choose the smallest update strategy](#choose-the-smallest-update-strategy)
- [Understand LPA-star state](#understand-lpa-star-state)
- [Understand D-star Lite orientation](#understand-d-star-lite-orientation)
- [Handle graph updates completely](#handle-graph-updates-completely)
- [Represent scheduled traversal](#represent-scheduled-traversal)
- [Use time-expanded states when needed](#use-time-expanded-states-when-needed)
- [Keep reservations and avoidance distinct](#keep-reservations-and-avoidance-distinct)
- [Validate repairs and timing](#validate-repairs-and-timing)

## Choose the smallest update strategy

| Situation | Starting strategy |
|---|---|
| Occasional local terrain edit, few active routes | Invalidate affected routes and rerun A* |
| Many repeated queries to a common destination | Repair/rebuild a shared reverse field |
| Repeated related searches with edge changes | Consider LPA* or D* Lite after profiling |
| Doors, ferries or elevators with schedules | Arrival-time-aware transition model |
| Several agents must reserve narrow passages | Explicit temporal coordination |
| Nearby moving agents | Local avoidance plus a deadlock/replan policy |

A full A* rerun can be the best engineering choice for small graphs. Incremental search retains more state and needs complete change notifications; it is not automatically cheaper after a large edit or frequent goal changes.

## Understand LPA-star state

For a forward formulation with fixed start \(s\), maintain \(g(v)\) and a one-step lookahead:

\[
rhs(s)=0,\qquad
rhs(v)=\min_{u\in Pred(v)}\{g(u)+c(u,v)\}
\quad(v\ne s).
\]

A state is locally consistent when \(g(v)=rhs(v)\). A typical lexicographic key for target \(t\) is

\[
key(v)=
\left[
\min(g(v),rhs(v))+h(v,t),\quad
\min(g(v),rhs(v))
\right].
\]

Use compatible finite costs and a heuristic satisfying the chosen algorithm's assumptions. Infinity marks unreachable/uninitialized values; avoid numerical infinity subtraction or NaN comparisons.

The [LPA* primary paper](https://www.cs.cmu.edu/~maxim/files/aij04.pdf) supplies the complete queue/update/termination procedure. The equations here explain state ownership; they are not sufficient pseudocode for a correct implementation. For its standard proof conditions, retain strictly positive traversal costs and consistent heuristics; verify any zero-cost or altered variant separately.

**Original example:** if A has predecessor costs \(g(P)=4,c(P,A)=3\) and \(g(Q)=6,c(Q,A)=2\), then \(rhs(A)=7\). Increasing \(c(P,A)\) to 5 changes the lookahead to 8. Repair must propagate that change to successors whose values depended on A.

For a changed forward edge \(u\rightarrow v\), the immediate affected lookahead is \(rhs(v)\), because it depends on predecessors. Propagation handles subsequent effects. Removing a vertex requires updates for all incident transitions, not merely deleting its queue record.

## Understand D-star Lite orientation

D* Lite is designed for related navigation queries with a moving start and changing known edge costs. Its common formulation searches backward from a fixed goal \(t\):

\[
rhs(t)=0,\qquad
rhs(u)=\min_{v\in Succ(u)}\{c(u,v)+g(v)\}
\quad(u\ne t).
\]

Its key includes the current start \(s\) and a key offset:

\[
key(u)=
\left[
\min(g(u),rhs(u))+h(s,u)+k_m,\quad
\min(g(u),rhs(u))
\right].
\]

In the standard moving-start construction, update \(k_m\) using the heuristic distance between the prior and new start when required by the algorithm. Retain the selected formulation's positive-cost and consistent-heuristic assumptions, including directional triangle bounds. Use the [D* Lite paper and author corrections](https://idm-lab.org/bib/abstracts/Koen02e.html) for exact update and stopping rules.

For a changed directed edge \(u\rightarrow v\), update the tail's backward lookahead \(rhs(u)\) using the algorithm's update procedure, preserving the fixed goal boundary \(rhs(t)=0\); later propagation follows predecessors. An undirected connection represented by two directed edges needs both changes. This differs from the forward LPA* orientation above.

Choose the next action from a valid repaired solution using \(c(s,v)+g(v)\), subject to live execution checks. Do not assume the cost-to-go table is ready merely because a repair job has begun.

Maintain stable state identities, both successor and predecessor access, and a coherent graph revision. A goal change may require reinitialization or a specific supported extension. Do not retain arbitrary old values under a new goal and call that D* Lite.

## Handle graph updates completely

Changes include more than blocked tiles:

- Cost increases from mud, slope or damage.
- Cost decreases from a new road or drained ground.
- Added/removed bridges, doors and special links.
- Changed agent clearance, capabilities or movement mode.
- Graph rebuilding that changes topology or state IDs.

**Original repair scenario:** route S→A→G costs \(2+2=4\), while S→B→G costs \(3+3=6\). If A→G rises to 10, the correct new route costs 6. If a later shortcut B→G drops to 0.5, the new optimum is 3.5. Test both increases and decreases; only repairing broken route edges misses the latter improvement.

A current route can remain traversable while becoming suboptimal. State the policy: mandatory replan for invalidity, optional periodic/cost-threshold replan for quality. Prevent oscillation between nearly equivalent routes with a declared decision rule rather than corrupting the underlying path cost.

Publish a coherent graph snapshot or a revisioned update batch. Mixing old and new costs within an ordinary A* query voids its static-graph proof. A time budget can return “repair pending”; it must not masquerade as a fully repaired optimal result.

## Represent scheduled traversal

Let \(a_e(t)\) be the arrival time after taking edge \(e\) at departure time \(t\). Its travel duration is

\[
c_e(t)=a_e(t)-t\ge0.
\]

A FIFO edge satisfies

\[
t_1\le t_2\ \Rightarrow\ a_e(t_1)\le a_e(t_2).
\]

It forbids a later departure overtaking an earlier one *under that edge's modeled service rule*. FIFO is a property of arrival functions, not a statement that every moving obstacle queue behaves well.

For earliest-arrival search on a suitable FIFO network, a relaxation uses

\[
T(v)\leftarrow\min(T(v),a_{u,v}(T(u))).
\]

This is different from reading all edge durations at the initial query time and then running ordinary static Dijkstra.

**Original example:** a ferry departs at times 0, 10, 20, … seconds and crosses in 4 s. If waiting is allowed at the dock,

\[
a(t)=10\left\lceil t/10\right\rceil+4
\]

under the convention that arrival exactly at departure can board. Arrival at 3 s reaches the far dock at 14 s. Specify boarding cutoff, capacity, duration and the exact event-time boundary; changing them changes the edge function.

If waiting is unrestricted at a safe node, a raw non-FIFO edge can sometimes be replaced by its best attainable arrival envelope:

\[
\bar a(t)=\inf_{\tau\ge t}a(\tau).
\]

This reduction requires representable waiting, a computable/attained result under the selected model, and compatibility with the objective and constraints. It is not valid if waiting consumes a constrained resource or the waiting location becomes unsafe.

[Orda and Rom](https://sites.cs.ucsb.edu/~suri/cs231/Rlist/ordaRom.pdf) analyze time-dependent routes under different waiting restrictions. Treat waiting semantics as part of the problem definition, not a heuristic patch.

## Use time-expanded states when needed

For discrete planning ticks, model states \((v,k)\) and transitions

\[
(u,k)\rightarrow(v,k+\delta_e(k)).
\]

Include explicit wait actions where legal. Check occupancy throughout a transition, not only its endpoints. State the time unit, integer rounding policy, planning horizon and what happens at its boundary.

**Original example:** a bridge needs two ticks to cross and is blocked during interval \([3,5)\). Entry at tick 2 overlaps the blockage even if the agent's start node is free at tick 2 and the far node is free at tick 4. A legal crossing test must consider the occupied interval.

The expanded graph can grow as positions × time × additional state. Safe-interval methods compress free time spans while preserving required timing information; use a complete published formulation if adopting them. Do not collapse two arrivals at the same location when their future options differ.

A static spatial lower bound can remain admissible in a time-expanded search if it ignores nonnegative waiting/conflict delays and uses a valid minimum travel cost. It must still respect special links and agent capabilities.

## Keep reservations and avoidance distinct

A reservation records planned use of vertices, edges or spatial resources over intervals. Check both simultaneous occupancy and opposite-direction edge swaps under the chosen agent model. For finite-size agents and variable durations, geometric overlap can occur even when discrete node reservations do not conflict.

Incremental replanning repairs one agent's graph problem. It does not itself prevent two agents from accepting incompatible routes. Local collision avoidance does not guarantee global progress through a narrow corridor. Temporal coordination, priorities, resource scheduling or joint multi-agent search are separate optional mechanisms.

Define whether an agent continues occupying its goal after arrival. A warehouse doorway used as a permanent goal can block every subsequent arrival under a stay-at-goal model. Prefer explicit staging/parking/service locations when the game requires turnover.

## Validate repairs and timing

After each edit sequence, compare repaired path cost and validity with a fresh exact search on the same revision. Include disconnected/reconnected graphs, one-way edges, moving starts, changed goals, large edits and budget interruption.

For schedules, test exact boundary times, permitted/forbidden waits, blocked intervals, simultaneous requests and horizon exhaustion. Distinguish earliest arrival from minimum travel time or energy; waiting can affect these objectives differently.

Save durable world and schedule state. Search heaps and incremental caches are usually rebuildable; serialize them only with explicit graph/algorithm/version compatibility. Never reload a stale queue and silently apply it to a differently rebuilt topology.
