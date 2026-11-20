# Planner selection and search guarantees

## Match capabilities before benchmarking

Inventory the requirements used by the model and the features actually accepted by
the planner. Then check the chosen heuristic and search configuration. A translator
may accept conditional effects or axioms that a particular heuristic cannot handle.
A command-line flag containing “optimal” does not compensate for unsupported input.

| Need | Candidate approach | Check first |
| --- | --- | --- |
| Small typed STRIPS teaching/prototype | pyperplan | No general ADL, numeric, temporal, or action-cost promise |
| Classical/ADL/derived facts and restricted costs | Fast Downward | Heuristic-specific axioms/effects support |
| Numeric resources | Numeric-capable planner | Supported operators, bounds, objective, precision |
| Durative actions and overlap | Temporal planner | Invariants, duration constraints, concurrency semantics |
| Preferences/trajectory constraints | Explicitly compatible planner | Supported constraint forms and metric semantics |
| Reusable domain methods | HTN-capable formalism/planner | Different problem formulation and guarantees |

The [pyperplan project](https://github.com/aibasel/pyperplan) describes itself as a
lightweight teaching/prototyping STRIPS planner without action costs. Fast Downward's
[current support page](https://www.fast-downward.org/latest/documentation/pddl-support/)
excludes general numeric and temporal planning, preferences, and object fluents. Do
not recommend it as a generic implementation of every PDDL 3.1 feature.

## State what the search establishes

A satisficing planner seeks a valid plan and may sacrifice optimality for speed. An
optimal configuration must search under conditions that establish the optimum for
the actual metric. Heuristic admissibility, search algorithm, cost transformation,
pruning, bounds, and termination all matter. Weighted search can improve speed but
requires its own guarantee analysis.

For a finite unit-cost state graph, exhaustive breadth-first search can find a
shortest action-count plan or exhaust the reachable state space. That statement
does not extend to arbitrary numeric PDDL or resource-limited interrupted runs.
For cost-sensitive search, keep the objective and edge costs explicit.

A typical documented Fast Downward pattern is:

```bash
./fast-downward.py --alias seq-sat-lama-2011 domain.pddl problem.pddl
./fast-downward.py domain.pddl problem.pddl --search 'astar(lmcut())'
```

Check feature support before using either pattern. The second is a common optimal
classical cost-search configuration only within its supported assumptions, not a
universal optimum guarantee. See [planner usage](https://www.fast-downward.org/latest/documentation/planner-usage/)
and [heuristic properties](https://www.fast-downward.org/latest/documentation/search/Evaluator/).

## Preserve termination meaning

Parse the actual version's exit codes and logs. Fast Downward distinguishes proved
unsolvability, incomplete search, bounds, timeout, memory exhaustion, and portfolios
that found a plan before another component failed. A nonzero status can coexist with
a useful candidate plan in portfolio modes. Validate the candidate while accurately
reporting the incomplete run. See [exit codes](https://www.fast-downward.org/latest/documentation/exit-codes/).

Use separate output directories per run and remove stale plan-file ambiguity. Record
plan hash, input hashes, command, version, limits, and observed status so a result can
be reproduced without guessing which artifact was returned.
