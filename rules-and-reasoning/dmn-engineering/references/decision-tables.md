# Decision tables and hit policies

## Define the table contract

Name the input expressions, their types and admissible values, each output and its
type, and the expected result cardinality. A row matches when all its input entries
are satisfied. Each input entry is a unary test evaluated against the corresponding
input expression; an output entry is a value expression. Rule annotations are
explanatory metadata rather than returned outputs.

Quote strings in FEEL: `"urgent"` is a string, while `urgent` is a name lookup.
Use `-` for an unrestricted input test. Do not use an empty cell to imply a business
meaning that only the editor happens to supply.

## Choose the hit policy explicitly

| Policy | Result selection | Meaning of order |
| --- | --- | --- |
| Unique (`UNIQUE`, U) | At most one matching rule | Row order is irrelevant |
| Any (`ANY`, A) | Overlapping matches must have equal outputs | Row order is irrelevant |
| Priority (`PRIORITY`, P) | Highest-priority matched output | Declared output-value order |
| First (`FIRST`, F) | First matched row | Row order is part of logic |
| Rule order (`RULE ORDER`, R) | All matches, in rule order | Row order is part of result |
| Output order (`OUTPUT ORDER`, O) | All matches, ordered by output priority | Output-value order |
| Collect (`COLLECT`, C) | All matches, or a supported aggregate | No list-order guarantee without further logic |

Unique is the default, not a completeness declaration. Test both overlap and gaps.
Any does not mean choose any arbitrary differing result; differing outputs violate
the policy. Priority is not another spelling of First.

## Handle Collect correctly

With one result output, `aggregation="SUM"`, `MIN`, `MAX`, or `COUNT` produces an
aggregate. Without aggregation, retain the matched output list, including duplicates.
If two matched rows each output `5`, Collect Sum gives `10` and Collect Count gives
`2`; do not deduplicate. For compound outputs use unaggregated Collect and an
explicit, tested subsequent calculation if an aggregate is needed.

Do not infer no-match behavior from the identity of a mathematical aggregate.
DMN 1.6 clause 10.3.2.10 specifies default output or `null` on no hit. An engine or
API may expose a list wrapper, null, absent property, or error for an invalid table.
Pin the runtime behavior and keep the distinction in the adapter.

## Check nonportable corners

The [DMN 1.6 PDF](https://www.omg.org/spec/DMN/1.6/PDF), clause 8.2.11, permits
compound Output Order with lexicographic output priority, while clause 10.3.2.10
restricts Output Order to a single output. For portable models, use a single output
or a separate explicit ordering step and record the choice. Do not invent a
cross-engine guarantee from this inconsistent text.

The inspected [Camunda profile](https://docs.camunda.io/docs/components/modeler/dmn/decision-table-hit-policy/)
lists Unique, Any, First, Rule Order, and Collect. Check support before importing
Priority or Output Order. An editor offering a policy does not prove that the
deployed runtime executes it.

## Useful review cases

Exercise exact thresholds, absent/invalid values, no-hit input, two overlapping
matches, equal and unequal duplicate outputs, and deliberate row permutations.
For order-independent policies, permuting rows should preserve the decision value
(up to an explicitly unordered result list). For First, keep a regression that
changes if rows are mistakenly reordered.
