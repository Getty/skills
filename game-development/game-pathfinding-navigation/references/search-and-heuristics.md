# Search algorithms and heuristic correctness

Choose a graph and cost objective before choosing a search algorithm. These methods optimize the supplied state-transition model; they do not establish physical traversability or select a citizen's goal.

## Contents

- [Select the baseline](#select-the-baseline)
- [Define state and costs](#define-state-and-costs)
- [Implement A-star without hidden assumptions](#implement-a-star-without-hidden-assumptions)
- [Construct a valid heuristic](#construct-a-valid-heuristic)
- [Handle inconsistency and zero-cost edges](#handle-inconsistency-and-zero-cost-edges)
- [Choose bounded suboptimal search deliberately](#choose-bounded-suboptimal-search-deliberately)
- [Validate against an independent baseline](#validate-against-an-independent-baseline)

## Select the baseline

| Method | Appropriate input and objective | Important condition |
|---|---|---|
| Breadth-first search | Minimum number of edges, or equal positive edge costs | Different traversal costs invalidate the cost-optimality claim |
| Dijkstra | Minimum sum of finite nonnegative edge costs | Use actual directed edges and stop on settled goal |
| A* | Same objective, with a useful lower bound to the goal | Heuristic, reopening and termination must agree |
| Reverse/multi-source Dijkstra | Many starts share compatible destinations | Reverse directed edges, retaining original traversal costs |
| Weighted A* | A chosen bounded departure from cost optimality | State the inflation factor and required algorithm conditions |

For a first implementation, use Dijkstra as the oracle and A* as the optimized query. A zero heuristic makes the same correct A* implementation behave as Dijkstra. Do not add hierarchy or incremental repair solely because the map has polygons.

The [Red Blob introduction](https://www.redblobgames.com/pathfinding/a-star/introduction.html) is a useful conceptual starting point. Its [implementation guide](https://www.redblobgames.com/pathfinding/a-star/implementation.html) provides readable examples; adapt the algorithm to the full contract rather than treating example code as a universal engine.

## Define state and costs

Let \(G=(N,E)\) be a finite directed graph, with traversal cost \(c(u,v)\ge0\). A path \(P\) minimizes

\[
C(P)=\sum_{(u,v)\in P}c(u,v).
\]

Use one cost unit: seconds, distance, energy, or explicitly defined game-cost units. An edge with a one-time door-opening cost can use travel time plus interaction time. If turning, remaining fuel, movement mode, inventory permissions or time changes future legal transitions, include the necessary information in the search state. A location ID alone is then insufficient.

Example: a vehicle arriving at the same junction facing north or south may have different next-turn costs. Model states such as (junction, heading), or acknowledge an approximation. Do not attach a turn penalty depending on the search parent while still merging all arrivals into one location state.

Represent prohibited transitions as absent edges or a separately handled blocked value. Reject negative and nonfinite executable costs. A reward subtracted from path cost can create negative edges/cycles; use a different objective/model instead of assuming Dijkstra remains correct.

**Original example:** a 30 m route at 1.5 m/s costs 20 s. A 40 m route at 4 m/s costs 10 s. A shortest-distance route and a fastest route choose different paths. A heuristic measured in metres cannot be added directly to the accumulated seconds.

## Implement A-star without hidden assumptions

Store best known cost \(g(n)\), predecessor/action, and priority

\[
f(n)=g(n)+h(n).
\]

Use a priority queue with a stable tie field so equal priorities do not require arbitrary node objects to be comparable. A simple duplicate-entry heap can avoid a decrease-key operation:

~~~text
best[start] = 0
push(priority=h(start), queued_g=0, serial=next(), state=start)
while queue is not empty:
    pop the minimum-priority entry
    discard it if queued_g differs from current best[state]
    if state satisfies the goal:
        reconstruct and return the path
    for each legal outgoing transition:
        candidate = best[state] + transition_cost
        if candidate strictly improves best[successor]:
            update best and predecessor
            push(candidate + h(successor), candidate, next(), successor)
return no_path
~~~

This version permits a previously expanded state to be expanded again when improved. Validate costs, heuristic values and accumulated sums against NaN/overflow. Keep the graph revision and agent profile fixed during the query, or restart/repair with a defined algorithm.

**Stop when the goal is removed as the valid minimum-priority entry**, not when first discovered. With start-to-goal cost 10 and start-to-A-to-goal costs 1 and 1, first discovery can return 10 instead of 2.

Return distinct statuses for no path, budget exhausted, cancelled, invalid request and stale world. A time-limited search that has not exhausted its frontier has not proved that no route exists.

## Construct a valid heuristic

For a single goal \(t\), let \(d^*(n,t)\) be the optimal remaining cost.

- **Admissibility:** \(0\le h(n)\le d^*(n,t)\), with \(h(t)=0\).
- **Consistency:** \(h(u)\le c(u,v)+h(v)\) on every usable directed edge.

With a suitable consistent heuristic, ordinary A* can settle each state once. With an admissible but inconsistent heuristic, use a reopening implementation such as the one above. Admissibility alone does not justify a permanent closed set.

### Common lower bounds

For cardinal grid moves costing at least \(D\) per cell step:

\[
h=D(|\Delta x|+|\Delta y|).
\]

Coordinates here are grid-step counts. For 8-neighbor movement, cardinal cost \(D\), diagonal cost \(D_2\), and \(D\le D_2\le2D\):

\[
h=D(\max(|\Delta x|,|\Delta y|)-\min(|\Delta x|,|\Delta y|))
+D_2\min(|\Delta x|,|\Delta y|).
\]

These are relaxed obstacle-free metrics under the specified transition costs. Cheap diagonal zigzags, jump links or teleports can invalidate them. If costs vary, use globally valid lower bounds, not typical or average terrain costs.

**Original example:** \(|\Delta x|=7\), \(|\Delta y|=3\), \(D=2\) s and \(D_2=2\sqrt2\) s give \(h=8+6\sqrt2\approx16.4853\) s.

For travel time in continuous geometry, a possible bound is

\[
h(n)=\frac{\|\mathbf x_n-\mathbf x_t\|}{v_{\max}},
\]

provided every legal action respects that global speed/distance bound. A teleport can violate it. Use a graph-aware relaxation that includes cheap special links, or use zero.

For multiple acceptable goals, the minimum of compatible goal-specific lower bounds is a lower bound. The maximum of valid lower bounds for the *same objective and goal set* remains a lower bound. Do not sum them without a proven non-overlapping cost decomposition.

See [Amit Patel's heuristic discussion](https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html) for design ideas; preserve the precise lower-bound contract when transferring an idea.

## Handle inconsistency and zero-cost edges

**Original reopening fixture:** directed costs are S→A=3, S→B=1, B→A=1, A→G=2. Set \(h(S)=4,h(B)=3,h(A)=0,h(G)=0\). These are admissible, but B→A violates consistency because \(3>1+0\).

A* first expands A with cost 3, then B improves A to cost 2. Reopening A finds the optimal goal cost 4. A permanent closed set can retain the inferior goal cost 5. Include this case when a heuristic API promises only admissibility.

Zero-cost edges are valid for Dijkstra/A* on a finite graph with strict improvement and appropriate duplicate handling. They complicate route extraction from a distance field: equal-distance neighbors can form a cycle. Preserve an acyclic predecessor/successor relation established by search, or add a justified monotone secondary rank. “Always move to any neighbor with nonincreasing distance” is insufficient.

Do not add an epsilon to every edge merely to hide zero cycles; that changes the optimized objective. Floating-point comparison tolerances likewise change which improvements are accepted. Document their error implications or prefer exact/integer costs where appropriate.

## Choose bounded suboptimal search deliberately

Weighted A* uses

\[
f_w(n)=g(n)+w\,h(n),\qquad w\ge1.
\]

For a fixed finite graph with nonnegative costs, an admissible nonnegative heuristic with zero at the goal, proper reopening on improvements, and termination when the valid minimum-priority goal is popped, the returned cost satisfies \(C\le wC^*\) when a solution exists. This bound is about the graph's chosen cost, not geometric distance or collision-free execution.

The bound follows because an optimal-path frontier state has \(g+h\le C^*\) and therefore \(g+wh\le wC^*\). At termination the goal's cost cannot exceed that frontier priority under the stated search invariant.

Inflating a heuristic does not guarantee a speedup for every map. Do not change \(w\) midway while leaving queue priorities and closure assumptions stale. For controlled anytime improvement, study [ARA*](https://papers.neurips.cc/paper_files/paper/2003/file/ee8fe9093fbbb687bef15a38facc44d2-Paper.pdf) and implement its complete repair/termination rules.

**Original bound example:** if \(C^*=80\) s and \(w=1.25\), the guarantee is at most 100 s under those assumptions. A run stopped before a solution or using an inadmissible terrain estimate has no such automatic guarantee.

## Validate against an independent baseline

Test start=goal, unreachable goals, directed links, unequal costs, zero-cost cycles, duplicate heap entries, the reopening fixture, and cheap portals. Compare A* cost with Dijkstra on many small synthetic graphs; compare cost and validity rather than requiring the same tie-broken route.

Check heuristic inequalities against exact reverse distances on small fixtures. Record expansions, generated entries, peak frontier, time and graph-build cost separately. Consistent A* with a heap has familiar graph-search bounds; arbitrary reopening heuristics can cause many repeated expansions. Avoid advertising one complexity or speed number for every variant.
