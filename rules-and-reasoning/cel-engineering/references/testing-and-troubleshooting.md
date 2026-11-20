# Testing and troubleshooting

## Test the complete expression contract

Keep source, declarations, profile, bindings, and expected typed outcome together.
Test parse errors, type-check errors, runtime errors, valid false, valid true, and
wrong output types separately. A checked expression is not automatically correct
for the user's decision question.

Use the same real evaluator that will run in production when feasible. A host
language reimplementation of the predicate does not validate CEL semantics. For
cross-stack work, preserve disagreements as evidence and identify whether they
come from the language subset, adapter, extension, or defect.

## Exercise meaningful boundaries

| Category | Cases |
| --- | --- |
| Presence | Missing key, null, empty value, absent parent |
| Types | Correct type, incompatible dynamic value, coercion attempt |
| Collections | Empty, one member, duplicates, invalid member, maximum size |
| Numeric | Zero, negative, exact threshold, one beyond, large value |
| Temporal | Before start, at start, before expiry, at expiry |
| Errors | Failing function, absorbed error, unresolved error |
| Environment | Missing declaration, missing overload, changed descriptor |
| Host | Inactive binding, wrong match scope, unavailable parameters |

For partial-evaluation applications add unknown attribute combinations and residual
agreement tests. The bundled corpus does not claim to cover every unknown API.

## Diagnose by stage

A parser failure suggests syntax or disabled macros. A checker failure suggests
undeclared names, incompatible types, or missing overloads. A runtime failure after
successful checking often involves dynamic data, missing bindings, conversion, or
custom functions. A correct local result with wrong production behavior suggests
host matching, binding, data adaptation, or result consumption.

Do not silence a checker issue by declaring everything dynamic unless runtime
flexibility is a real requirement. Do not convert every error into false without
preserving diagnostic classification. A denied request and an evaluator outage
may share an external response while requiring different operational action.

## Inspect Python results carefully

The official wrapper exposes CEL type and value. Host Python equality can consider
Boolean true equal to integer one. Check the CEL type first, then the value; use
CEL-aware comparisons where the library provides them. The bundled runner makes
those checks explicitly. See the [wrapper documentation](https://github.com/cel-expr/cel-python/blob/main/README.md).

## Finish with reproducible evidence

Record the exact runtime version and command, number of executed cases, failed
case IDs, and untested integration layers. Add a minimal regression case for each
repair. Validate YAML structure separately from server-side Kubernetes acceptance;
then verify actual create/update behavior where authorized and available.
