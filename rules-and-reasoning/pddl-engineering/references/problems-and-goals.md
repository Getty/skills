# Problems and goals

## Build an explicit instance

A problem names its domain, declares its objects, provides the initial state, and
states a goal. Domain constants are shared across instances; problem objects are
instance-specific. Use immutable mapping IDs for external objects so a regenerated
problem can be traced back to the same real entities. See the [problem grammar](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/node28.html).

Validate domain-name matching, object types, predicate argument order, and symbol
spelling before search. Treat PDDL symbols according to the parser's case-insensitive
language conventions; avoid case-only external identifiers. Keep human-readable labels
in an external mapping instead of using punctuation or whitespace that changes parsing.

For classical propositional input, omitted facts are false under the model's closed
world. That is a statement about the model, not a claim that an unobserved real-world
fact is false. A missing `(connected dock lab)` therefore removes the route in the
bundled example. If a route is merely unobserved, decide whether to inspect it,
assume it conservatively unavailable, or use a richer uncertainty model.

Initialize numeric fluents used by the model explicitly. Do not assume every omitted
numeric value defaults to zero; numeric undefinedness differs from absent propositions.
Avoid contradictory initial facts such as simultaneous exclusive locations. A planner
may search the provided inconsistent abstraction without recognizing the intended
physical impossibility.

## Separate goal, invariant, and objective

A goal constrains the final state. It does not necessarily say how the goal was
reached. A parcel can end at its destination after an unacceptable intermediate
state unless the actions or trajectory constraints prohibit that state. State
trajectory requirements explicitly in a supported formulation.

A metric ranks plans; it does not make a soft preference mandatory. “Deliver parcel”
should remain a hard goal if failure to deliver is unacceptable. A cost term such as
“prefer fewer moves” should not replace that hard goal. When several objectives
conflict, state whether the desired ordering is weighted, lexicographic, or a hard
bound plus a secondary objective; confirm planner support before choosing syntax.

## Test three baseline instances

Start with a small reachable goal whose expected plan can be inspected by hand.
Then remove one enabling fact to create an impossible instance in a finite classical
profile. Finally create an already-satisfied goal. The correct result of the third
case can be an empty plan; do not use a language-level truthiness test to classify
an empty list as search failure.

For generated problems, retain the source snapshot, generation time, object-ID map,
and relevant assumptions. Deterministic generation makes model diffs meaningful.
A new observation normally produces a new problem instance; changing the domain is
appropriate only when the transition model or capabilities themselves changed.
