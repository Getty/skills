---
name: json-logic-engineering
description: "Use when writing, embedding, validating, testing, migrating or debugging JSON Logic (JsonLogic) rules — JSON expression trees, json-logic-js and other ports, var and missing values, truthiness and coercion, collection scope, custom operations, rules shared between browser and server, rule builders, or rules that must behave the same across evaluators."
---

# JSON Logic Engineering

Treat JSON Logic as an expression format with project documentation, reference
implementations, and implementation-specific behavior. Do not present it as an
OMG, OASIS, or IETF standard. Identify the evaluator and supported operator profile
before promising portability or predictable error handling.

Use the project documentation and **json-logic-js 2.0.5** as the inspected reference
profile. This package version is not a separately versioned
language specification. Recheck releases before adopting dependencies.

## Select the reference for the task

| Task | Read |
| --- | --- |
| Understand expression shape, types, and object ambiguity | [Language and types](references/language-and-types.md) |
| Bind inputs and distinguish absent, empty, null, and false | [Data binding and missing values](references/data-binding-and-missing.md) |
| Predict logical, comparison, arithmetic, or conditional results | [Operators and control flow](references/operators-and-control-flow.md) |
| Write map/filter/reduce and quantified conditions | [Collections and scope](references/collections-and-scope.md) |
| Turn a requirement into a maintainable rule | [Modeling workflow](references/modeling-workflow.md) |
| Embed in a service, UI, or another language | [Embedding and portability](references/embedding-and-portability.md) |
| Add operations or accept rules from another party | [Extensions and security](references/extensions-and-security.md) |
| Create a behavior corpus and compare implementations | [Testing and conformance](references/testing-and-conformance.md) |
| Store, version, deploy, explain, and replay rules | [Storage and lifecycle](references/storage-and-lifecycle.md) |
| Compare or translate other rule systems | [Interoperability](references/interoperability.md) |
| Diagnose surprising output | [Troubleshooting](references/troubleshooting.md) |
| Run original fixtures and helpers | [Worked examples](references/worked-examples.md) |
| Check authority, versions, and refresh steps | [Sources and versioning](references/sources-and-versioning.md) |

Load only the needed references. Work independently of sibling skills. Use
`dmn-engineering`, `feel-engineering`, `opa-rego-engineering`, `cel-engineering`,
`cedar-engineering`, or `xacml-engineering` when the task also needs those technologies.

## Establish the execution contract

Inspect supplied rules and their caller. Record the evaluator/package version,
host language, extension registry, input schema, and expected result type. Establish
missing-data and coercion policies, numeric ranges, time representation, allowed
operators, size/depth limits, and execution budget. Identify the authoritative
decision point and the way evaluation errors reach its caller.

For an illustrative request, select a small profile and label assumptions. Do not
ask for production details when a synthetic example suffices. For a repair, preserve
the intended output contract instead of changing values until a test passes.

## Build or repair a rule

1. **Name the decision and inputs.** Write expected outputs for ordinary, boundary,
   missing, null, wrong-type, and empty-collection cases before nesting rules.
2. **Validate facts at the boundary.** Use a schema or typed adapter. Distinguish
   invalid input from a negative business decision; normalize units and dates.
3. **Choose the smallest expression.** Use one operator key per expression node.
   Keep metadata outside the AST. Use explicit operand arrays where shorthand is unclear.
4. **Preserve semantics.** Prefer strict scalar equality for a typed contract, guard
   missing data explicitly, and track the scope of each `var` in collection bodies.
5. **Execute meaningful cases.** Run the original fixtures and relevant upstream tests
   on every supported port. Separate unsupported operations, exceptions, non-finite
   results, and ordinary falsy values.
6. **Integrate a bounded wrapper.** Apply the operator allowlist before evaluation.
   Keep extensions pure when replay matters. Enforce the documented result type.
7. **Version complete behavior.** Bind rule, input schema, evaluator, and extension
   profile revisions together. Preserve review and rollback evidence.
8. **Report observed behavior.** Name the runtime executed and the remaining untested
   layers. Parsing JSON does not establish rule validity or business correctness.

## Preserve the non-obvious semantics

- A rule may return a non-Boolean. `and` and `or` return operand values. For an explicit
  Boolean authorization contract, require `result === true` at the host boundary.
- JSON Logic makes an empty array falsy and string `"0"` truthy. Do not substitute
  host-language truthiness.
- `var` supplies a default for an unresolved path; an explicit null is not replaced
  by that default in the inspected JavaScript evaluator.
- `missing` treats null and empty string as missing in that evaluator. Zero and
  false are present values. It is not a pure property-existence test.
- `==` permits coercion. `===` avoids scalar coercion but is not portable deep
  structural equality for records or lists.
- `map`, `filter`, `all`, `some`, and `none` change data scope to the current item.
  `reduce` supplies `current` and `accumulator`; do not invent outer-scope escapes.
- For an empty list, `all` is false, `some` is false, and `none` is true in the
  reference profile. Do not import another language's quantifier conventions.
- Custom functions receive evaluated arguments and cannot introduce a new lazy
  control structure merely by wrapping a host function.
- A one-key object is interpreted as an operation by json-logic-js. Place ordinary
  records in input data instead of relying on ambiguous inline object literals.
- The format has no built-in enforcement point, provenance model, combining
  algorithm, durable workflow, or sandbox for arbitrary host extensions.

## Use the bundled helpers

Run from this skill directory or substitute absolute paths:

```bash
python3 scripts/inspect_rule.py assets/examples/training-eligibility.logic.json
node scripts/run_cases.cjs --engine /trusted/path/to/logic.js assets/examples/semantic-cases.json
```

`inspect_rule.py` parses strict JSON, applies bounded static checks for a deliberately
restricted authoring profile, and inventories operators and static paths. It rejects
literal record objects and unknown operations. It is not a general validator,
evaluator, or runtime-cost proof.

`run_cases.cjs` loads a caller-supplied trusted local CommonJS evaluator and compares
values/types or expected errors. It downloads nothing and registers no extensions.
Loading that module executes its code; use a trusted runtime. Neither helper is an
execution sandbox.

## Deliver evidence

Return the requested rule or integration, runtime/profile, input contract, case
results, and any material portability limitation. For an action, identify the
server-side enforcement point and distinguish invalid input and runtime failure
from an ordinary negative decision. Preserve the user's requested scope.
