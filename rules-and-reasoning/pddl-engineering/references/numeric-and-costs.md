# Numeric fluents and action costs

## Model quantities with units and bounds

Use numeric fluents for quantities such as fuel, inventory, battery, capacity, or
accumulated cost. Declare functions over typed objects, initialize values, and write
numeric comparisons in prefix form. Effects can assign or adjust a fluent using
supported operations such as `assign`, `increase`, and `decrease`.
The [numeric PDDL2.1 chapter](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/node3.html)
defines the language; each planner supports its own fragment.

Document units beside the model: seconds versus minutes, watt-hours versus percent,
and integer cents versus currency units. Check every effect preserves physical bounds.
If an action consumes fuel, model both its availability precondition and its decrease.
An objective alone does not prevent a plan from consuming a resource below zero.

Do not model arbitrary real numbers as ordinary action parameters. PDDL2.1 numeric
fluents associate values with object tuples. If an operation chooses among a finite
set of settings, model named settings or a supported numeric formulation explicitly.
Unbounded numeric behavior can make a search space fundamentally different from a
finite propositional one.

## Keep action costs distinct from general arithmetic

A common cost-only profile declares `(total-cost)`, initializes it to zero, increases
it on actions, and minimizes it in the problem metric. This does not imply support
for fuel arithmetic, arbitrary numeric guards, or temporal planning.

Fast Downward's researched profile accepts restricted nonnegative integer action
costs: at most one total-cost update per action, outside conditional effects. It
does not support general numeric planning. Verify the current [PDDL support contract](https://www.fast-downward.org/latest/documentation/pddl-support/)
and the selected heuristic's capabilities.

```lisp
; Cost-only fragment, not a complete domain/problem pair.
(:functions (total-cost))
; Add (increase (total-cost) 4) to the selected action's effects.
; In the problem:
(:init (= (total-cost) 0))
(:metric minimize (total-cost))
```

Retain other required initial facts; the fragment illustrates syntax and must not
replace a complete `:init` section. Use `:action-costs` only with a compatible engine.

## Make the objective well defined

A minimum-length plan and a minimum-cost plan can differ. A plan containing more
cheap actions can beat a short expensive route. A satisficing search may return a
valid plan without proving minimum cost. A valid plan's reported cost must be recomputed
from the model, not inferred from the number of lines in its output.

Inspect loops that can improve the metric indefinitely, zero-cost cycles, division
by zero, and missing initial values. If the model rewards refueling without a finite
fuel source or capacity, the optimum may be undefined. The [plan-metrics discussion](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/node4.html)
explains why the objective is part of the modeling problem. Keep those risks explicit
when translating business rewards into planner costs.
