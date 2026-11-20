# Modeling workflow

## Build an explicit decision contract

Write the business question, output domain, valid input domain, and handling of
invalid input before building the table. For example: select `express`, `economy`,
or `freight` for a shipment using a nonnegative weight and an urgency value of
`normal` or `urgent`. This is a synthetic policy, not a logistics recommendation.
Separate input validation from routing so that an unknown urgency cannot accidentally
be interpreted as an ordinary shipment.

Record units, reference time, rounding rule, allowed enum values, and ownership.
A bare `number` does not encode kilograms, currency, or acceptable precision.
Use ItemDefinitions and allowed-value restrictions where appropriate, while also
specifying the host's input-validation contract.

## Translate source prose carefully

Extract statements into conditions, consequences, exceptions, and dependencies.
Preserve ambiguous terms as review questions: `recent`, `high risk`, and `normally`
need an agreed meaning. Do not hide discretion inside a numeric threshold invented
by the modeler. Keep source quotations outside executable expressions and attach
stable references to the relevant decision or rule.

Choose the expression shape that exposes the important logic. A score formula may
be clearer as a literal expression; a small classification matrix as a table; a
sequence of named intermediate calculations as a context. Reusing a function does
not require duplicating its business meaning across many tables.

## Partition and test the domain

For a threshold `10`, distinguish below, equal, and above. For two inputs, test the
cross-product of relevant partitions rather than merely one case per row. Include
invalid values separately so that validation failures do not masquerade as business
outcomes. Check whether the table is complete over the declared domain; an unbounded
claim of completeness is usually meaningless without that domain.

Under Unique, prove or check non-overlap for admissible inputs. Under Any, compare
all output components for overlapping rules. Under First, show which later rules
are shadowed and why order is intentional. Do not repair an overlap by switching to
First without explaining the changed behavior to the business owner.

## Iterate with an observable artifact

Keep a decision contract, the model, and a table of cases close together. Derive
expected outcomes from the agreed policy before running an engine. A test runner
must compare actual results to an independent expectation, not calculate expected
results with the same implementation.

Review changes by business effect: which inputs move to a different outcome, which
new inputs are accepted, and which failures are handled differently. Use structural
XML diffs for tooling and a human-readable table or decision diff for review.
The [DMN specification](https://www.omg.org/spec/DMN/1.6) defines the modeling
constructs; these workflow choices are engineering recommendations.
