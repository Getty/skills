# Performance and compilation

## Diagnose grounding before changing search

Count objects per type, action parameters, grounded operators, facts, and translation
time. A schema with several unconstrained parameters can create a large Cartesian
product before search begins. Use meaningful types and static relations to rule out
impossible combinations. Remove irrelevant objects only when they cannot affect the
goal, constraints, resources, or authorization-related abstraction.

Keep static connectivity and dynamic availability distinct. A static graph can
support grounding reductions; a route that changes during a plan cannot safely be
compiled away as permanently true. Use concise action schemas, but do not pack
unrelated operations into one action merely to reduce the visible action count.

The [Fast Downward translator format](https://www.fast-downward.org/latest/documentation/translator-output-format/)
helps inspect the compiled finite-domain task. Its output format and compiler behavior
are versioned interfaces; do not treat internal translator output as a stable exchange
format for every planner.

## Compare search configurations fairly

Use the same domain/problem, resource limits, cost interpretation, and validation
procedure. Record translation and search separately. Report solved instances, plan
quality, time, and memory rather than only the fastest successful case. A heuristic
that performs well on one domain can behave poorly on another structure.

Check whether the heuristic supports conditional effects, derived facts, and action
costs in the selected configuration. For example, a universal condition can be compiled
into axioms, making apparent syntax support depend on axiom-aware heuristics. Read the
[current feature restrictions](https://www.fast-downward.org/latest/documentation/pddl-support/)
and [evaluator properties](https://www.fast-downward.org/latest/documentation/search/Evaluator/).

## Preserve meaning through compilation

If replacing negative conditions, numeric resources, derived facts, or preferences
with a simpler encoding, specify what is preserved: solvability, final state, plan
length, cost, temporal behavior, or optimality. These are different properties. A
compilation can preserve reachability while changing minimum action count.

Keep a map back from compiled actions/objects to original ones. Validate decoded
plans against the original model when tooling allows. Do not execute bookkeeping
actions introduced solely for compilation as real external operations.

Discretizing a quantity creates an approximation. State rounding direction, bounds,
and the consequences of a lost feasible plan or an introduced infeasible one. A
conservative resource abstraction may be useful, but it must be reviewed and tested.
Do not hide numerical approximation behind the word “equivalent.”

## Stop optimization at the actual bottleneck

If translation dominates, adding a clever search heuristic may not help. If external
state loading dominates, planner tuning may be irrelevant. Reduce a slow instance
while retaining its structural difficulty, and preserve correctness regression cases
alongside benchmark data. Re-run independent plan validation after optimizing a
model or compiler path.
