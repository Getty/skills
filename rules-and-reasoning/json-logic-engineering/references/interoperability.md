# Interoperability

## Choose the right layer

| Technology | Suitable responsibility | Translation hazard |
| --- | --- | --- |
| JSON Logic | Compact JSON-serialized expressions | Dynamic types, coercion, scope |
| FEEL | Typed decision expressions and unary tests | Null logic, decimal/temporal semantics, indexing |
| DMN | Decisions, dependencies, tables, hit policies | A tree has no DRD or table-hit contract |
| CEL | Embedded checked expressions with host declarations | Error/unknown semantics and host libraries |
| Rego/OPA | Structured policy queries and deployment | Undefined, sets, rule composition |
| Cedar | Application authorization over entities | Permit/forbid, entity typing, schema |
| XACML | Attribute-based access decisions and obligations | Four outcomes, combining, obligations |
| PDDL | State/action planning | Expression evaluation does not search for plans |
| RUML | Rulemaps with source/context/result conventions | Ordered/undefined semantics and capabilities |

Use the respective autonomous skills for detailed work. This is a responsibility
mapping, not a ranking or an assertion that every pair has a standard converter.

## Translate by observable behavior

Define source and target versions and the supported subset. Map types, missing/null,
truthiness, errors, number representation, order, collections, and external functions.
Create counterexamples before implementing a translator. A Boolean-only happy path
can conceal important differences.

For FEEL, do not mechanically change `and` tokens: JSON Logic returns operand values,
and its missing/default behavior differs. For a DMN table, decide how to reproduce
overlap, hit policy, output aggregation, and no-match behavior. A priority `if` chain
only represents a deliberately chosen first-match contract.

For authorization, keep richer results in an outer wrapper rather than flattening
everything to false. XACML Indeterminate and NotApplicable are distinct; Cedar forbids
and Rego undefined values require explicit mappings. Preserve reason/status and
obligation handling when translating an access-decision API.

## Treat round trips as a separate problem

An executable translation can lose source labels, stable IDs, comments, decision
dependencies, explanation paths, or editor layout. Specify whether the goal is
execution compatibility, human editing, or reversible interchange. Test all promised
properties separately.

Avoid claiming a standard mapping where only an application-specific compiler exists.
Record lossy features and reject unsupported constructs rather than silently treating
them as true, false, or no-op.

Source anchors: [JSON Logic format](https://jsonlogic.com/),
[OMG DMN](https://www.omg.org/spec/DMN/1.6),
[CEL specification](https://github.com/google/cel-spec),
[OPA documentation](https://www.openpolicyagent.org/docs/policy-language),
[Cedar](https://docs.cedarpolicy.com/), and
[XACML core](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-en.html).
