# Acceleration, abstraction and any-angle paths

Add acceleration after measuring representative queries. Choose techniques by graph structure, shared destinations, edit rate and acceptable path quality.

## Contents

- [Identify the actual cost](#identify-the-actual-cost)
- [Use landmark lower bounds](#use-landmark-lower-bounds)
- [Build hierarchy with explicit approximation](#build-hierarchy-with-explicit-approximation)
- [Use jump-point pruning only in its domain](#use-jump-point-pruning-only-in-its-domain)
- [Distinguish any-angle planning and smoothing](#distinguish-any-angle-planning-and-smoothing)
- [Handle bidirectional termination carefully](#handle-bidirectional-termination-carefully)
- [Version and validate accelerators](#version-and-validate-accelerators)

## Identify the actual cost

Measure graph construction, nearest-node projection, search, corridor processing, collision checks and path following separately. A faster priority queue will not fix a full navmesh rebuild on every agent request.

| Repeated workload | Candidate approach | Main cost or limitation |
|---|---|---|
| Many agents, same destination and movement costs | Reverse distance/policy field | Shared field invalidation and memory |
| Large mostly stable graph, varied destinations | Landmark bounds or hierarchy | Preprocessing and update maintenance |
| Long routes across regions | Portal/cluster abstraction | Approximation and connector quality |
| Uniform regular grid with many symmetric alternatives | Jump Point Search family | Restrictive movement/cost assumptions |
| Similar queries after local cost changes | Incremental search | Retained state and repair bookkeeping |
| Short time budget with acceptable extra cost | Bounded-suboptimal/anytime methods | Must preserve the chosen bound's conditions |

Start with a good representation and compact data. Avoid introducing every method simultaneously: it becomes difficult to identify which cache or approximation caused a route error.

## Use landmark lower bounds

For a fixed directed graph, precompute shortest distances **from** and **to** selected landmarks \(L\). Distances to a landmark are computed from it on the reversed graph with original edge costs.

For target \(t\), triangle inequalities give:

\[
d(v,t)\ge d(L,t)-d(L,v),
\]

\[
d(v,t)\ge d(v,L)-d(t,L).
\]

Use

\[
h(v)=\max\left(0,\max_L
\{d(L,t)-d(L,v),\,d(v,L)-d(t,L)\}\right)
\]

over well-defined finite terms. All terms use the same cost unit and movement profile. Do not substitute an absolute difference of forward distances on a directed graph. That familiar simplification requires symmetric distances.

**Original example:** \(d(L,t)=20\) s and \(d(L,v)=7\) s provide a 13 s bound. If \(d(v,L)=16\) s and \(d(t,L)=5\) s, the reverse-distance term provides 11 s. The combined landmark bound is 13 s.

Never evaluate infinity minus infinity. Skip undefined bounds, or use proven reachability information to reject a state/query. A zero fallback remains admissible. Per-node omission of unavailable terms needs a consistency check on the usable search graph if the implementation forbids reopening; a reopening A* avoids relying on an unproved consistency claim.

The [Goldberg–Harrelson ALT paper](https://www.microsoft.com/en-us/research/publication/computing-the-shortest-path-a-search-meets-graph-theory/) establishes the landmark/triangle-inequality approach. Choose landmark placement and count empirically for the game's graph rather than copying road-network performance claims.

With \(k\) landmarks and \(N\) nodes, storing two full directed distance tables uses roughly \(2kN\) distance values before compression and metadata. Example: 16 landmarks, one million nodes and 8-byte distances require 256 MB for those values alone (decimal MB). This is arithmetic, not a benchmark.

When all edge costs only increase or edges disappear, an old admissible heuristic remains a lower bound for the new distances. Decreases or newly added shortcuts can invalidate it. Tag tables with graph/profile/cost revisions and rebuild or fall back to a safe bound when necessary.

## Build hierarchy with explicit approximation

Partition space into regions and identify legal transitions between them. Preserve costs for crossing each region between its selected connectors. Search the abstract graph, then refine its route into local paths.

Store:

- Region and connector IDs independent of render tiles.
- Agent-profile/capability constraints.
- Local connector paths/costs and dependency revisions.
- Entry and exit geometry, not merely a region's average elevation.
- A rule for connecting arbitrary query endpoints to the abstraction.

**Original example:** two rooms share a 20 m opening. Representing only its midpoint forces every query through that midpoint. A route entering and leaving near one end may take a needless detour. The low-level searches can each be exact while the chosen abstract route remains suboptimal.

Do not assign a region-crossing edge one constant cost when its cost depends on both entry and exit; model connector pairs or another justified summary. Distinguish a lower-bound abstraction used as a heuristic from a realizable route abstraction used to produce movement.

[HPA* by Botea, Müller and Schaeffer](https://webdocs.cs.ualberta.ca/~mmueller/ps/2004/hpastar.pdf) is a primary reference for clustered grid pathfinding. Its reported experimental quality/speed is not a universal bound for every game graph. Connector selection, cluster size, refinement and smoothing affect quality.

For dynamic worlds, rebuild changed local connectors and propagate invalidation to dependent abstract edges. A bridge removed in one tile can invalidate long regional routes. A new bridge can create a better route even though the old route is still traversable.

Preserve connectivity where possible. Coarse summaries that accidentally discard the only narrow passage create false no-path results. If a coarse search fails, distinguish a proven disconnection from abstraction incompleteness.

## Use jump-point pruning only in its domain

Original Jump Point Search removes symmetric intermediate expansions on a uniform-cost regular grid using direction-dependent pruning and jump rules. Its optimality argument depends on the permitted cardinal/diagonal transitions and obstacle/corner rules.

Use the [Harabor–Grastien primary paper](https://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf) for the complete pruning definitions. Do not port only the visual “jump until obstacle” idea.

Do not assume original JPS supports arbitrary polygon neighbors, weighted mud/road costs, directed doors, special actions or variable agent footprints. Specialized later variants may support different domains, but verify that variant's proof and implementation.

**Original counterexample idea:** two apparently symmetric grid routes may traverse grass costing 1 and mud costing 10. Pruning one as interchangeable with the other is no longer justified solely by geometric symmetry.

Record the exact grid policy:

- Four or eight neighbors.
- Cardinal and diagonal costs.
- Whether diagonal movement past blocked corners is allowed.
- Agent clearance already baked into the grid.
- Static or runtime-checked obstacles.

For each supported policy, compare costs against ordinary Dijkstra/A* on exhaustive small maps and adversarial corner patterns. Map edits require the current obstacle view; precomputed jump data needs explicit invalidation.

## Distinguish any-angle planning and smoothing

Grid-constrained A* optimizes routes through grid edges. Removing that heading restriction changes the route space.

Theta* tests visibility to an expanded node's parent and can connect farther ancestors directly. The [Theta* authors](https://idm-lab.org/bib/abstracts/Koen10r.html) explicitly distinguish its short any-angle paths from guaranteed globally shortest continuous paths. Do not describe Basic Theta* as an exact Euclidean shortest-path method.

Line-of-sight must include the actual footprint and movement rules. A point ray between nodes can pass through a gap narrower than the agent. On weighted terrain, a geometric shortcut may be more expensive; integrate the same cost field along the shortcut rather than comparing only length.

**Original example:** replacing a 12 m road path with a 10 m mud segment reduces distance but can increase time from 3 s at 4 m/s to 10 s at 1 m/s. “Smoother” is not the optimized objective unless cost checks agree.

For navmesh corridors, funnel/string-pulling is a corridor processing technique. Its guarantees apply to the selected valid portal corridor under the appropriate geometric assumptions. A polygon-centroid A* corridor followed by a funnel does not automatically select the globally shortest route among every possible corridor. Refer to the navigation-representation guidance for footprint and nonplanar-surface details.

Keep a valid original path until a proposed shortcut passes collision, clearance, action and cost checks. Do not smooth across doors, jumps, ladders or scheduled transitions as though they were ordinary ground segments.

## Handle bidirectional termination carefully

Two searches meeting once do not prove optimality. Track the best complete route cost \(\mu\) and a lower bound on any route not yet excluded.

For ordinary bidirectional Dijkstra on a fixed nonnegative directed graph, search forward from start and backward over reversed edges from goal. A standard stopping condition compares the minimum valid unsettled distances:

\[
\min Q_f+\min Q_b\ge\mu,
\]

provided candidate cross-connections and queue invariants are maintained consistently. This statement is a design checkpoint, not a complete implementation.

Heuristic bidirectional search needs compatible potentials and its own termination derivation. Do not apply the Dijkstra condition to two arbitrary A* queues. If the implementation is not complete, prefer the simpler proven single-direction baseline.

## Version and validate accelerators

Key cached results by graph revision, agent profile, goal/set, cost model and relevant settings. Separate route validity from optimality: a cost decrease outside an existing route may leave it valid but no longer best.

Benchmark cold build, warm queries, local edits, frequent goal changes and unreachable cases. Include memory, invalidation/rebuild time and path-cost ratio against a baseline. Do not quote historical paper speedups as expected performance on the user's game.

For approximate approaches, report the actual guarantee: exact under defined graph assumptions, bounded by a factor, empirically near-optimal on a test set, or a designer heuristic. These are different claims.
