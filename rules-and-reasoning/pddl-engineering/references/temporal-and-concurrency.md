# Temporal planning and concurrency

## Model time as semantics, not output decoration

Use durative actions only when duration, overlap, or intermediate invariants affect
validity. A timestamp added to a sequential plan does not establish temporal validity.
Declare `:durative-actions` and any additional numeric/duration requirements actually
used, then select a planner and validator that support the resulting fragment.

A durative action specifies duration, temporally qualified conditions, and effects.
Conditions can apply at start, throughout the open interval, or at end; discrete
effects occur at start or end. If a property must hold across the closed interval,
model both endpoint conditions and the `over all` condition. See the [durative-action
semantics](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/node5.html).

## Preserve resource exclusivity

For a resource that cannot serve two actions concurrently, require an availability
fact at start, remove it at start, and restore it at end, or use a supported numeric
capacity formulation. Preserve the distinction between a reservation and actual
resource consumption. A reusable machine and a consumable material need different
state updates.

Model locations during transit deliberately. If a robot leaves its origin at start
and reaches its destination at end, another action requiring either stationary
location should not run mid-transit unless that behavior is intended. Do not leave
the robot at both locations through an entire travel interval.

## Respect simultaneous endpoint restrictions

Under the no-moving-targets rules, an endpoint cannot rely on a value being changed
by a concurrent endpoint. Actions that appear compatible after a chosen sequential
ordering may be invalid at the same timestamp. Conflicting endpoints need separation;
compatible additive numeric updates have specific exceptions. Consult the [concurrency
chapter](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/node6.html)
rather than applying an ordinary multithreading intuition.

For example, an action that produces a fact and another that needs that fact should
not be assumed executable at exactly the same time. Moving the consumer slightly
later can repair a temporal plan only when its other constraints still hold. Do not
add arbitrary epsilons until the validator accepts a logically incorrect schedule.

## Validate with explicit tolerance

A temporal plan normally includes start times and durations in the selected planner's
output format. Preserve these values and their precision; sorting or rounding can
change validity. Set the validator's epsilon/tolerance explicitly, record it, and
align it with the planner and execution scheduler. VAL documents `Validate -v -t`
for diagnostic validation in its [application guide](https://github.com/KCL-Planning/VAL/blob/master/applications/README.md).

Model exogenous timed facts and continuous processes only with supported extensions.
A timed initial literal says an event occurs at a known modeled time; it does not
handle arbitrary surprises. Continuous effects, PDDL+ events, and real-time execution
require stronger assumptions than the bundled classical example. Revalidate after
changing timing, resource assumptions, or planner/compiler versions.
