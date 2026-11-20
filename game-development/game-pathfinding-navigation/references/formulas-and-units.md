# Formula conventions and navigation index

Use this reference to locate the full model before implementing an equation. The linked chapters state assumptions, worked examples and limits; this index is not a standalone navigation solver.

## Contents

- [Declare the objective and units](#declare-the-objective-and-units)
- [Distinguish common symbols](#distinguish-common-symbols)
- [Find the relevant formula](#find-the-relevant-formula)
- [Use a complete formula card](#use-a-complete-formula-card)
- [Check dimensions and guarantees](#check-dimensions-and-guarantees)

## Declare the objective and units

Choose one additive objective for each ordinary shortest-path query: seconds, metres, joules, or defined game-cost units. Store the objective identity with the graph/profile revision. A distance-optimal result is not automatically time-optimal.

For continuous travel with cost density \(\kappa\) and discrete action charges \(p_\ell\),

\[
C(\gamma)=\int_\gamma \kappa(x)\,ds+\sum_{\ell\in\gamma}p_\ell.
\]

When \(\kappa\) is seconds/metre, both the integral and every charge must be seconds. Dimensionless terrain multipliers can modify an existing cost; a raw risk probability cannot be added to seconds without a declared conversion or a different objective model.

Separate clock time, traversal duration and planning cost. A time-dependent edge may arrive at \(a_e(t)\), with duration \(a_e(t)-t\). A discrete reservation uses ticks or intervals; document the conversion and rounding policy.

## Distinguish common symbols

| Symbol | Meaning | Unit or type |
|---|---|---|
| \(G=(N,E)\) | Directed state-transition graph | Discrete structure |
| \(c(u,v)\) | Edge traversal cost | Selected cost unit |
| \(g(v)\) | Best known accumulated cost | Same cost unit |
| \(h(v)\) | Estimated remaining cost | Same cost unit |
| \(f(v)\) | Search priority \(g+h\) | Same cost unit |
| \(D(v)\) | Exact/selected cost-to-go field | Same cost unit |
| \(rhs(v)\) | One-step lookahead cost | Same cost unit |
| \(w\) | Heuristic inflation factor | Dimensionless |
| \(\ell,r,m\) | Length, agent radius, geometric margin | m |
| \(\kappa\) | Spatial cost density | Cost/metre |
| \(\mathbf x,\mathbf v\) | Position and velocity | m; m/s |
| \(a_b\) | Available braking deceleration | m/s² |
| \(t,\tau\) | Time and prediction horizon | s, unless ticks declared |
| \(\operatorname{orient}(a,b,c)\) | Planar signed area predicate | m² |
| \(K,k_r\) | Resource capacity and request demand | Matching capacity units |

Symbols are local to a formula. The \(D\) cardinal-step cost in a grid heuristic is different from an entire distance field. The \(g\) search label is unrelated to terrain gravity. Prefer descriptive field names in code.

## Find the relevant formula

| Question | Full reference |
|---|---|
| Which representation and level of detail is enough? | [Scope and representation](scope-and-representation.md) |
| What belongs in the search state, profile and cost? | [Graphs, costs and agent profiles](graphs-costs-and-agent-profiles.md) |
| When does A* return an optimal path? | [Search and heuristics](search-and-heuristics.md) |
| How do Manhattan/octile/time bounds, reopening and weighted A* work? | [Search and heuristics](search-and-heuristics.md) |
| How do directed landmark bounds or abstractions apply? | [Accelerated and hierarchical search](accelerated-and-hierarchical-search.md) |
| How do changed edges, schedules and waits differ? | [Incremental and time-dependent search](incremental-and-time-dependent-search.md) |
| Does a finite agent fit, and what does a funnel optimize? | [Navmeshes and clearance](navmeshes-and-clearance.md) |
| How do projection, braking and local collision prediction work? | [Movement and local avoidance](movement-and-local-avoidance.md) |
| What are reservation capacity and multi-agent objectives? | [Multi-agent planning and reservations](multi-agent-and-reservations.md) |
| How should shared fields, caches and large worlds work? | [Large worlds and performance](large-worlds-and-performance.md) |
| How are changed world revisions published and consumed? | [Dynamic world and runtime](dynamic-world-and-runtime.md) |
| Which domain supplies terrain facts, destinations or movement? | [Domain contracts](domain-contracts.md) |
| How do concrete engine APIs map onto these concepts? | [Engine adapters](engine-adapters.md) |
| Which calculations and limits are executable? | [Numerical examples](numerical-examples.md) |
| What constitutes meaningful evidence of correctness or speed? | [Validation and benchmarks](validation-and-benchmarks.md) |
| Where are the original models and implementations documented? | [Sources and models](sources-and-models.md) |

## Use a complete formula card

When adding a model, record:

1. **Purpose:** observable game behavior and selected objective.
2. **Equation/state:** variables, authoritative data, units and orientation.
3. **Assumptions:** graph structure, costs, geometry, movement and time model.
4. **Algorithm conditions:** termination, reopening, queue invariants or constraint solver.
5. **Numerical policy:** finite inputs, precision, tolerances and degenerate cases.
6. **Original example:** small inputs with independently calculated expected output.
7. **Guarantee and limits:** exact, bounded, empirical, or explicitly heuristic.
8. **Evidence:** primary source, implementation version and verification cases.

Do not present a priority formula as a complete search algorithm, an ORCA half-plane as a complete avoidance solver, or a clearance equation as proof that an arbitrary vehicle can turn.

## Check dimensions and guarantees

- Add \(g+h\) only when both use the same objective and units.
- Divide geometric distance by a valid maximum speed to obtain a time lower bound; cheap special links can invalidate it.
- Reverse a directed edge for cost-to-go computation without changing its original cost semantics.
- Keep Euclidean smoothing separate from weighted-cost optimization.
- Convert world distances to voxel counts explicitly; do not apply baked clearance twice.
- Treat infinity as unreachable/uninitialized state according to the algorithm, not an invitation to compute infinity minus infinity.
- State the graph revision and agent profile for every optimality claim.
- Separate search completion from execution feasibility and eventual arrival.

The formulas are optional tools selected by the task. Their stated assumptions become requirements only when that model or guarantee is used.
