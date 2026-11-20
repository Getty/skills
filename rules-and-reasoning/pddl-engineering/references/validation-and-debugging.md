# Validation and debugging

## Validate in layers

| Check | Useful evidence | Limit |
| --- | --- | --- |
| Lexical/structural inspection | Balanced forms, expected sections, identifiers | Does not establish PDDL grammar or semantics |
| Parser/type checks | Bound variables, declared symbols, accepted syntax | Parser may accept only a fragment or ignore unsupported sections |
| Planner translation | Grounded/compiled task and feature diagnostics | Compilation must preserve intended semantics |
| Search | Candidate plan or meaningful termination | Search success alone does not validate the plan |
| Plan validation | Applicable sequence, goals, temporal/resource conditions | Establishes validity only relative to the model |
| Model review and simulation | Counterexamples and invariant checks | Does not prove every real-world assumption |
| Execution monitoring | Observed effects and current state | Previous results can become stale |

Prefer an independent validator when practical. Use VAL for a supported PDDL profile
and retain its version and output. Its [application guide](https://github.com/KCL-Planning/VAL/blob/master/applications/README.md)
documents syntax inspection and detailed plan validation:

```bash
Validate domain.pddl problem.pddl
Validate -v -t 0.001 domain.pddl problem.pddl candidate.plan
```

A permissive or unsupported parser must not be mistaken for acceptance by the standard.
Check warnings and the selected validator's support. For numeric and temporal models,
record tolerances and inspect near-boundary failures. The [PDDL2.1 validation discussion](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/node16.html)
explains why finite plan validation differs from solving the search problem.

## Debug from the earliest contradiction

For an invalid plan, inspect the first failing action or temporal event. Show the
required fact, actual state, and previous effect that should have established it.
Check argument order before changing logic. A plan that moves the robot before
picking a parcel at the origin should fail at the pickup, not be repaired by granting
the pickup impossible reach.

For no plan, first eliminate unsupported input and parser/grounder errors. Then
inspect whether goal facts can be established at all, whether necessary objects and
static links exist, and whether resource constraints are too strong. Reduce the
instance while preserving the failure. A complete finite search can establish
unsolvability for that model; a timeout cannot.

For a suspiciously easy plan, look for missing preconditions, missing delete effects,
forgotten resource consumption, interchangeable objects, goals already true, and
concurrency that bypasses a missing lock. Examine the state after each step rather
than praising a short output.

## Retain useful regression cases

Keep one reachable case, one blocked case, one initially satisfied goal, a capacity
counterexample, and each repaired bug's smallest reproducer. Temporal models also
need overlapping, conflicting-endpoint, invariant-breaking, and duration-boundary
cases. Numeric models need zero, upper/lower bounds, and missing initialization.
Use only tests relevant to the model's supported feature profile.

Report exactly which tools ran. Replaying a plan through the same planner library
is helpful but is not independent validation. The bundled helper states that limit
explicitly instead of presenting its assertions as a general conformance suite.
