# Collections and scope

## Track every variable's scope

`map`, `filter`, `all`, `some`, and `none` evaluate their body with the current item
as data. For an object item use its field names; for a scalar item use `{"var":""}`.
A path such as `order.customer` inside a body looks inside the item, not in the outer
document.

```json
{"map":[{"var":"items"},{"*":[{"var":"quantity"},{"var":"unitPriceMinor"}]}]}
```

If a predicate needs both row data and a global threshold, construct explicit row
contexts in the host, or select a language with suitable lexical bindings. Do not
invent `../`, `$root`, or `parent` as standard scope escapes. Nested collection
operators repeat the scope change.

## Initialize reductions

A reduction body receives `current` and `accumulator`. It does not inherit the
original document. Supply a typed initial value:

```json
{"reduce":[{"var":"amountsMinor"},{"+":[{"var":"current"},{"var":"accumulator"}]},0]}
```

The empty array returns the initial value. Missing and wrong-type collections
should usually be rejected by input validation. A forgiving fallback to an empty
result does not demonstrate valid business input.

## Test quantifiers and membership

For the reference profile, `all([])` is false, `some([])` false, and `none([])` true.
This differs from mathematical universal quantification. Decide explicitly whether
an empty approver list is acceptable.

`filter` preserves items whose predicate is truthy. `map` preserves array length
for valid array input. `merge` concatenates one level, not recursively. `in` can
mean list membership or substring search; prevent a role list being replaced with
a string that happens to contain the desired text.

## Bound work

Limit input cardinality as well as AST size. A shallow tree with nested collection
operations can perform substantial work. Static depth is not a cost proof. When
rules are untrusted, use an interruptible worker/process and test maximum permitted
sizes. A promise timeout on the same blocked event loop cannot interrupt synchronous
JavaScript evaluation.

Authority: [array operations](https://jsonlogic.com/operations.html#array-operations)
and [scoped evaluation source](https://github.com/jwadhams/json-logic-js/blob/2.0.5/logic.js).
