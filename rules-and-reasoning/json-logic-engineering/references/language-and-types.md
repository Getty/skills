# Language and types

## Read an expression as data

Use JSON Logic for serialized computations whose producer and consumer agree on an
evaluator. An operator object contains one key and its value supplies operands.
Compose calls by nesting them. Keep rules separate from the data being evaluated.

```json
{"and": [{">=": [{"var": "age"}, 18]}, {"===": [{"var": "active"}, true]}]}
```

Numbers, strings, booleans, and null are literals. Arrays can contain expressions
and are recursively evaluated. In json-logic-js, any object with exactly one key
is an operation node, whether that operation exists or not. Other objects pass
through as literals. This makes inline record literals fragile: adding one property
can change interpretation.

For example, `{"status":"ready"}` in expression position attempts an operation
named `status`. Put records in input data, or specify an extension. The bundled
inspector deliberately rejects all record literals in the rule tree. That is a
restricted authoring profile, not a claim that every such object is invalid upstream.

## Pin the result type

A rule may select a string, calculate a number, project a list, or return null.
Declare the output type at the boundary. Coercing a string such as `"false"` to a
Boolean would turn it into truth in JavaScript. If the contract requires Boolean,
validate the type rather than applying a generic cast.

JSON has no separate integer, decimal, date, duration, set, or binary type. Host
representations matter: JavaScript numbers cannot represent all large integers,
and division can produce Infinity or NaN, neither of which is a JSON number.
Reject non-finite values before serialization. For money, use documented integer
units within a verified range or a matching, versioned decimal extension.

## Normalize conservatively

Unary shorthand such as `{"var":"x"}` is convenient. Retain an extra operand-list
array when the operand itself is an array: `{"!!":[[]]}` supplies one empty list.
Do not flatten arrays or reorder operands during formatting.

Reject duplicate keys before parsing discards them. Require UTF-8, finite JSON
numbers, and size limits. An AST schema helps authors but does not establish
operation support, arity, input types, or domain correctness.

Authority: [project introduction](https://jsonlogic.com/),
[pinned implementation](https://github.com/jwadhams/json-logic-js/blob/2.0.5/logic.js),
and [operations](https://jsonlogic.com/operations.html).
