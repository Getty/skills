# Data binding and missing values

## Define path semantics

Use `var` against the current data scope. The reference evaluator splits dotted
paths into property segments and can access arrays by numeric indexes. The empty
path returns the whole current scope. Do not assume JSON Pointer escaping, wildcard
selection, bracket notation, or a built-in way to escape a literal dot in a key.

```json
{"var": ["account.limit", 0]}
```

State whether a default is a business value or a technical fallback. A zero budget
may be intentional, or it may hide a failed lookup. Use explicit data-quality state
when missing evidence requires review.

## Separate existence and completeness

For json-logic-js 2.0.5:

| Data for `x` | `{"var":["x",9]}` | `{"missing":["x"]}` |
| --- | --- | --- |
| Absent | `9` | `["x"]` |
| Null | `null` | `["x"]` |
| Empty string | `""` | `["x"]` |
| Zero | `0` | `[]` |
| False | `false` | `[]` |
| Empty list | `[]` | `[]` |

Treat this as a tested implementation profile, not a guarantee about every port.
`missing_some` returns an empty list if enough nominated fields are present;
otherwise it returns the missing names. It does not return a count or Boolean.

For property presence while allowing null, use a schema or a precisely specified
presence extension. Do not turn the domain's unknown into false accidentally.
Do not let a null numeric field satisfy a coercing comparison and call it valid.

## Bind trusted plain data

Decode bounded JSON into plain data. Avoid passing objects with methods, getters,
proxies, or inherited sensitive properties. The inspected `var` code reads
properties directly, rather than enforcing own-property checks at each segment.
Apply hardening to the host object graph as well as to the rule.

For replay, capture relevant facts at one logical instant. Inject timestamps as
facts. Bind tenant, subject, resource, and authoritative attributes server-side.
Comparing two attacker-controlled tenant strings does not establish tenancy.

Authority: [data operations](https://jsonlogic.com/operations.html#accessing-data)
and [implementation of var and missing](https://github.com/jwadhams/json-logic-js/blob/2.0.5/logic.js).
