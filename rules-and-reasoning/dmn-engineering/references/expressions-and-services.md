# Expressions and services

## Select a boxed expression

A boxed expression gives a structured presentation of logic. Choose its shape
according to the operation, not because the modeler defaults to a table.

| Shape | Useful purpose | Important check |
| --- | --- | --- |
| Literal expression | Compact FEEL formula or condition | Dialect and result type |
| Context | Named intermediate computations | Entry order and final result binding |
| Decision table | Explicit condition/result combinations | Hit policy and domain coverage |
| Invocation | Call a function or BKM with bindings | Parameter names, arity, and types |
| Function definition | Reusable parameterized logic | Supported function kind |
| List or relation | Collection or tabular data value | Item shape and ordering |
| Conditional/iteration/filter forms | Structured control/data transformations | Actual version and engine support |

Read [DMN 1.6](https://www.omg.org/spec/DMN/1.6/PDF), clauses 7 and 10, for
precise metamodel elements. A vendor's visual editor may expose fewer forms than
its runtime or serialize equivalent logic differently.

## Keep FEEL and the host distinct

FEEL provides typed values and expressions. A DMN input cell accepts unary tests
such as `< 10` or `[10..20]`; a literal expression requires a complete expression
such as `weight < 10`. Output entries return values, so the text `"freight"` is
appropriate while `= "freight"` is not a portable output expression.

DMN 1.6 defines FEEL and the B-FEEL dialect. B-FEEL deliberately changes how invalid
operations and missing information influence values. Do not change a language URI
as an editor convenience. Confirm a runtime supports it and run cases that reveal
the semantic differences. The standalone `feel-engineering` skill covers the
language independently if present.

## Reuse knowledge with explicit bindings

Use a BKM to expose named parameters and a result. Supply invocation bindings rather
than depending on mutable application globals. Keep function names separate from
external service locations. FEEL function support does not imply that Java, PMML,
ONNX, or a custom function provider is available; these require capability checks.

For external functions, declare purity, timeout, failure behavior, and versioning.
Avoid external network calls during replay unless their original result is part of
the replay input. A model can be deterministic only relative to all relevant inputs
and invoked implementations.

## Publish decision services carefully

Identify input data, input decisions, output decisions, and encapsulated decisions.
Expose the business contract needed by callers while keeping internal calculations
replaceable. A decision service groups a decision interface; deployment transport,
authentication, transactions, retries, and authorization remain host concerns.
Test service invocation separately from evaluating one decision directly. A direct
engine API can expose intermediate results that a service contract intentionally
omits. Record exactly which interface each test exercises.
