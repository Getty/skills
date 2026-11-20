# Derived facts, timed literals, and constraints

## Derive facts from the underlying state

Use a derived predicate for a relation whose truth follows from other facts, such as
reachability through a changing connection graph. Keep basic predicates mutable by
actions and derived predicates computed from the state. Do not add a derived predicate
to an action's add/delete effects or initialize it as an independent truth.

The PDDL2.2 definition restricts rules so the derivation is well defined: actions do
not directly affect derived predicates; head variables and free body variables must
match; derived predicates cannot occur negatively in the rule body after normalization.
Positive recursion can express closure. See the [PDDL2.2 primary specification](https://ipc08.icaps-conference.org/deterministic/data/edelkamp-hoffmann-ipcbooklet-2004.pdf).

After state changes, derived facts must be recomputed according to their semantics.
A stale derived cache can make an invalid action appear applicable. If compiling
away derived predicates, account for recomputation, termination, action ordering,
and changes to plan cost/length. Do not assume that a handful of extra actions is
a semantics-preserving compilation.

## Represent known external times explicitly

Timed initial literals express specified future changes that are not chosen as
ordinary planner actions. Use them for known opening/closing windows or scheduled
availability changes. Distinguish a known appointment from an uncertain event whose
time may vary. A classical planner with derived-predicate support need not also
support timed literals, because those require temporal reasoning.

Record the time origin and units of the problem snapshot. If execution starts late,
rebuild the timed facts or translate them consistently; replaying a plan against a
shifted clock can invalidate it. Do not treat the schedule as an observation of what
actually occurred.

## Distinguish hard trajectory constraints and preferences

PDDL3 adds constraints over trajectories and preferences that can be violated at a
cost. A final-state goal, a hard trajectory constraint, and a soft preference are
three distinct mechanisms. For example, “the robot must never enter a restricted
room” is a trajectory restriction; “prefer fewer visits to a busy room” may be soft.

Use named preferences and metric penalties only with a planner that implements their
semantics. Include tests where the shortest feasible plan violates a preference but
a more expensive plan satisfies it, and verify the selected tradeoff. Consult
[Gerevini and Long's primary account](https://strathprints.strath.ac.uk/3149/1/strathprints003149.pdf)
and the [IPC source catalogue](https://ipc08.icaps-conference.org/deterministic/PddlResources.html).

Do not replace a safety constraint with a sufficiently large guessed penalty.
Unless the model and objective establish the bound, the optimizer may still choose
to violate it. Likewise, encoding `always` as a final-state goal permits temporary
violations. If the target engine cannot express the required constraint, either use
a reviewed compilation with preserved guarantees or select an appropriate engine.
