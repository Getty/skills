# Domain modeling

## Model facts with stable meanings

Define typed predicates with a short sentence explaining each argument. For example,
`(robot-at ?r ?l)` means one robot is located at one location, while `(connected ?a ?b)`
means a permitted directed route. Do not let the same predicate alternately mean
“known true,” “possibly true,” and “requested.” Those are different state variables.

Separate static facts, which no action changes, from fluents, which can change.
Static connectivity can reduce grounding cost; a route that can close must be modeled
as dynamic or supplied in a new problem snapshot. Keep facts relevant to planning;
large descriptive metadata can remain in the host system with stable object mappings.

Types restrict parameters, but do not impose state invariants. The type `robot` does
not ensure the robot is at exactly one location. Preserve such invariants in the
initial state and in every action that touches the related predicates.

## Write actions as transitions

Specify parameters, precondition, and effects. Ensure every variable is bound and
well typed, and each predicate use has the declared arity. Test preconditions in the
current state; apply the transition's effects rather than treating the effect list
as sequential code. Facts not changed persist. See the [action grammar](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/node26.html)
and [simple-plan semantics](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/node12.html).

For a transfer action, explicitly remove the old location and establish the new one.
For a pickup, remove the parcel's floor location, remove `handempty`, and add `carrying`.
For a drop, reverse the carrying relationship and restore capacity. Omitting the
capacity precondition allows multiple simultaneous logical loads even if the action
name sounds physically constrained.

Require every permission-relevant or resource-relevant fact that makes the modeled
action possible, but distinguish those abstract facts from current runtime authorization.
A planned action's precondition may become false before execution. The model explains
why the planner expects the action to work; the adapter must still check reality.

## Audit invariants using counterexamples

Create a compact invariant ledger:

| Invariant | Initial-state check | Action check |
| --- | --- | --- |
| A robot has one location | Exactly one location fact | Move deletes origin and adds destination |
| A parcel is either placed or carried | One placement/holder | Pick/drop preserve exclusivity |
| Robot carries at most one parcel | Empty or exactly one load | Pick requires and consumes `handempty` |
| Connectivity is directed | Declare intended directions | Move tests origin-to-destination edge |

Test a second pickup without a drop, a move without a route, and a parcel transfer
from a different location. If a counterexample succeeds, repair the action contract;
do not merely add a goal that hides the intermediate violation.

Use negative preconditions, conditional effects, and quantification only with the
required profile and actual support. Conditional effects test conditions in the
applicable pre-state, not after earlier textual effects. Avoid contradictory effects
and duplicate encodings of the same fact unless their consistency is maintained.
Keep a minimal STRIPS version when it expresses the real requirement cleanly.
