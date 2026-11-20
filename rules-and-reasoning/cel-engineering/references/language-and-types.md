# Language and types

## Start with an environment

Declare names and types before compiling. Decide whether inputs are typed messages,
maps, or dynamic values. Configure the namespace/container and protobuf descriptors
when relevant. A variable named `request`, `self`, or `resource` is supplied by an
embedding; it is not automatically available in every CEL evaluator.

Use expressions for values, predicates, and transformations. CEL does not supply a
general imperative program with arbitrary loops and side effects. Host extensions
must be reviewed separately. The [CEL overview](https://cel.dev/overview/cel-overview)
explains the compile-once/evaluate-many embedding model.

## Preserve types

Distinguish Boolean, signed integer, unsigned integer, floating point, string,
bytes, list, map, null, timestamp, duration, and registered message types. Use explicit
conversions where the policy intends one. Do not interpret strings as numbers or
empty collections as false by host-language habit.

For JSON, write down how the adapter handles integers, large values, nulls, and
maps. A parser that converts large integers through double precision can lose
information before CEL sees it. For money, version the representation and rounding
policy; a general expression language does not choose an accounting convention.

Keep `dyn` as a deliberate escape hatch for values not statically known. It postpones
some errors to runtime and may make overloaded calls ambiguous. A successful checker
cannot prove that dynamic input will have the right type on every request.

## Build a readable expression

Prefer meaningful declared variables and straightforward Boolean clauses. For
example, with `used:int` and `limit:int`, `used >= 0 && used <= limit` expresses a
bounded quota check. It does not authenticate who supplied those numbers or define
what happens when the quota changes concurrently.

Use parentheses to make precedence apparent. If a host expects Boolean, reject
an expression whose result is a list, string, or number even if the host language
would consider it truthy. Return rich values only where the consumer contract
explicitly supports them.

## Separate language from implementation extensions

Consult the [language definition](https://github.com/cel-expr/cel-spec/blob/master/doc/langdef.md)
for baseline semantics, and the [implementation support matrix](https://cel.dev/reference/api-reference)
for optional and extension features. A function available in one stack may be
absent in another. A compile error may be an environment mismatch, not invalid CEL.

During migrations, preserve the old type declarations with the expressions. Compare
numeric boundaries, key presence, timestamp adaptation, and output types. Reusing
only source text while changing the input adapter can change policy behavior even
when the source is byte-for-byte identical.
