# Null, diagnostics, and Boolean semantics

## Preserve the third value

FEEL can produce true, false, or null in Boolean operations. Use the following
small table to reason about missing or invalid information without borrowing
JavaScript truthiness:

| `a` | `b` | `a and b` | `a or b` |
| --- | --- | --- | --- |
| true | null | null | true |
| false | null | false | null |
| null | null | null | null |

Negating null produces null. Comparing a value to null tests for null; in
particular `null = null` is true. The formal rules also address values outside
Boolean/null; validate the contract rather than relying on non-Boolean values in
conditions. See [DMN 1.6 §10.3.2.4 and tables 50–53](https://www.omg.org/spec/DMN/1.6/PDF).

## Do not mistake branching for uncertainty propagation

`if c then x else y` chooses `x` only when `c` is true. If `c` is null, it chooses
`y`; it does not automatically return null. Thus:

```feel
if score >= 50 then "pass" else "fail"
```

can select `"fail"` when the score is absent or the comparison is invalid.
If the intended business result distinguishes unavailable information, use an
explicit branch and validate types at the host boundary:

```feel
if score = null then "needs-data"
else if score >= 50 then "pass"
else "fail"
```

That null check alone does not make a wrong-type string valid. Define a separate
input-validation outcome where malformed data must be rejected.

## Keep diagnostics with values

A legitimate missing value and an invalid operation can both return null. Engines
may additionally report syntax errors, unknown variables, wrong function types,
and other diagnostics through different channels. Preserve those channels. Do not
write an adapter that discards all warnings and then labels null as a business
rejection.

The [Camunda error guide](https://docs.camunda.io/docs/components/modeler/feel/language-guide/feel-error-handling/)
describes its runtime behavior and extensions. Functions such as `assert` or
`get or else` must be treated according to the selected engine/version, not assumed
to be universally portable FEEL.

## Choose defaults as business rules

A default changes meaning. For a missing list of required approvals, replacing it
with `[]` can make `every` true; replacing an invalid amount with zero can move it
into a cheaper category. Prefer validation and explicit outcomes when bad data
should block a decision. Use a fallback only when its business meaning is accepted,
and include a case that proves the intended behavior.
