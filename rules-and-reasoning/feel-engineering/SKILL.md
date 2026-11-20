---
name: feel-engineering
description: "Use when writing or debugging FEEL expressions, standalone or in DMN — unary tests, Decimal128, null and three-valued logic, contexts, iteration, dates and durations, S-FEEL and B-FEEL, host bindings, or engines that disagree on a result."
---

# FEEL Engineering

Treat FEEL as a typed expression language with its own value model, scope rules,
operators, and diagnostics. Keep it separate from the surrounding DMN model, a
workflow product's expression field, and the implementation language of the host.

Use the FEEL specification in **OMG DMN 1.6** as the
normative baseline. Include **S-FEEL** as the simpler subset and **B-FEEL** as the
standardized dialect defined in DMN 1.6. Pin the actual engine/profile when writing
executable expressions; do not assume that every FEEL implementation supports the
latest grammar, decimal semantics, built-ins, or B-FEEL.

## Select the needed reference

| Task | Read |
| --- | --- |
| Establish versions, normative authority, or implementation evidence | [Sources and versioning](references/sources-and-versioning.md) |
| Choose FEEL, S-FEEL, B-FEEL, or a product expression profile | [Dialects and embedding](references/dialects-and-embedding.md) |
| Work with types, decimals, comparisons, names, or conversion | [Types and operators](references/types-and-operators.md) |
| Diagnose null, errors, Boolean results, or branch selection | [Null and Boolean semantics](references/null-and-boolean-semantics.md) |
| Author DMN input entries, alternatives, or interval tests | [Unary tests and ranges](references/unary-tests-and-ranges.md) |
| Filter lists, project fields, build contexts, or resolve names | [Lists, contexts, and scope](references/lists-contexts-and-scope.md) |
| Define functions, iterations, quantifiers, and built-in calls | [Functions and iteration](references/functions-and-iteration.md) |
| Handle dates, time zones, durations, and reproducible time | [Temporal semantics](references/temporal-semantics.md) |
| Integrate an interpreter with application data and diagnostics | [Runtime integration](references/runtime-integration.md) |
| Compare engines or design meaningful regression cases | [Testing and portability](references/testing-and-portability.md) |
| Diagnose unexpected results efficiently | [Troubleshooting](references/troubleshooting.md) |
| Run original cases with a real interpreter | [Worked examples](references/worked-examples.md) |

Use the optional `dmn-engineering` skill for decision graphs, hit policies, and
model interchange. This skill remains independently usable without a DMN engine.

## Establish the expression contract

Record the expression's purpose, source text, parser mode, expected result type,
input names and types, dialect, runtime version, enabled extensions, and diagnostic
policy. Inspect surrounding configuration: a leading `=` may belong to a workflow
product's expression marker rather than to FEEL syntax.

Choose **expression** mode for formulas such as `amount >= 100` and **unary-test**
mode for conditions such as `>= 100` applied to an implicit value. Never guess the
mode from a successful parse in a permissive editor. Record the actual API used.

Distinguish missing input, explicit null, invalid input, a valid false result, and
an evaluation failure in the host contract. A single null result cannot explain
which of these occurred without context and diagnostics.

## Author and verify an expression

1. **Define inputs and units.** Preserve numeric precision and temporal types at
   the boundary. Convert an external string deliberately; do not assume automatic
   coercion. Bind data as context values rather than interpolating it into source.
2. **Choose the minimal readable form.** Prefer a named context for intermediate
   calculations and a function for reusable logic. Keep business thresholds and
   reference dates explicit. Avoid giant nested conditionals when a small DMN table
   or named subexpressions would be easier to review.
3. **Check scope and parser mode.** Distinguish names from quoted strings, paths
   from literal keys, and complete expressions from unary tests. Check host naming
   restrictions separately from language grammar.
4. **Specify absence and errors.** Decide whether missing data should propagate,
   cause host rejection, or select an explicit fallback. Do not hide malformed input
   under a convenient default. Inspect warnings alongside returned values.
5. **Exercise semantic boundaries.** Test a normal case, false case, exact boundary,
   missing/wrong-type input, empty collection, and relevant error path. Add temporal,
   decimal, and scope cases when those features are used.
6. **Run the selected implementation.** Parse and evaluate using the real engine.
   Do not write a miniature evaluator to validate the engine being discussed.
   Preserve errors and returned types; do not compare only serialized text.
7. **Report scope of evidence.** Return the expression, binding assumptions,
   parser/dialect/version, observed result and diagnostics, and untested features.
   Distinguish standard expectations from an implementation's measured behavior.

## Preserve the easily missed semantics

- FEEL equality is `=`, inequality is `!=`, and exponentiation is `**`. Do not
  substitute JavaScript operators or use host-language truthiness.
- Standard FEEL numbers use Decimal128-style decimal semantics. A JavaScript
  implementation may expose binary floating-point differences; test rather than
  assuming all `number` implementations are numerically equivalent.
- Null is a value, not the string `"null"`. `null = null` is true; mixed-kind
  equality such as `1 = "1"` is null in FEEL rather than a coercing comparison.
- `false and null` is false; `true or null` is true. Other combinations can retain
  null. Negating an unknown does not turn it into true.
- `if condition then a else b` chooses `a` only when the condition is true.
  A null/non-true condition selects the else branch. Add an explicit unknown branch
  if the business meaning requires one.
- Lists are one-based; `[-1]` selects the last item. A zero or out-of-range index
  yields null. A numeric bracket expression selects an index; a Boolean one filters.
- A filter retains elements whose predicate is true. A field projection preserves
  list positions, including null for a missing field. Filtering and projection are
  different operations and may produce different lengths.
- Context entries can refer to earlier entries. Names, quoted string values, and
  quoted context keys have different roles. Do not depend on shadowed bindings
  without testing the intended scope.
- Multiple iteration bindings form a Cartesian product, not a zip. `every` over
  an empty collection is true; `some` over an empty collection is false.
- `sum([])` is null in standard FEEL. Do not import SQL or application defaults.
  State an explicit empty-list result when the business contract needs zero.
- Years/months durations and days/time durations are different kinds. One month
  is not generally thirty days. A calendar date is not a timestamp string.
- B-FEEL changes invalid-operation results and can change aggregates and comparisons.
  Treat moving to B-FEEL as a semantic change with dedicated tests.
- Functions or extensions supplied by the host can introduce effects, clock reads,
  and portability limits. A pure-looking expression is only as repeatable as its
  bound functions and inputs.

## Use the bundled cases

The original fixtures contain expression and unary-test cases. The Node helper
runs them through an explicitly supplied **feelin-compatible module** exporting
`evaluate` and `unaryTest`, with the documented `{value, warnings}` result contract.
It does not implement FEEL and performs no network requests.

```bash
node scripts/run_cases.mjs --engine /path/to/feelin/dist/index.js --cases assets/examples/core-cases.json
node scripts/run_cases.mjs --engine /path/to/feelin/dist/index.js --cases assets/examples/portability-probes.json
```

Read [worked examples](references/worked-examples.md) before running. The core cases
were exercised with feelin 8.2.0. Separate normative probes deliberately expose
measured decimal and type-handling mismatches on that runtime; do not change their
expected results to hide the differences. These are focused examples, not a
conformance certification.

## Deliver a precise answer

For a rewrite, explain the changed result on a distinguishing input. For a null or
error, show the expression, exact input binding, and diagnostics that support the
diagnosis. For a runtime recommendation, compare the features the user needs and
state observed limitations. Do not call a successful smoke test complete DMN or
FEEL conformance, or claim the absence of warnings proves correctness.
