# Collections and macros

## Select the intended quantifier

Use `items.all(x, predicate)` for every element, `items.exists(x, predicate)` for
at least one, and `items.exists_one(x, predicate)` for exactly one. Add `size(items)>0`
if an empty collection must fail a universal rule. Use map keys intentionally:
map macro iteration does not automatically bind each map value as the variable.

Original examples:

```cel
size(roles) > 0 && roles.all(r, r in ['reader', 'editor'])
items.exists(i, i.owner == subject)
items.exists_one(i, i.primary)
```

The exact field types must be declared or dynamically checked. Each example answers
a different cardinality question; do not substitute one because its name sounds similar.

## Distinguish macros from ordinary calls

Macros expand during parsing/checking into comprehension structures. A host chooses
which macros are enabled. `has` has special presence-test syntax; a custom function
with the same apparent call shape cannot recreate arbitrary field-presence semantics.
The standard macro set is documented in the
[API reference](https://cel.dev/reference/api-reference).

Use `map` for transformation and `filter` for selecting members. Decide whether
the consumer needs original order and duplicate entries. CEL lists are not Rego
sets; converting between them can lose meaning. For deduplication or sorting,
verify the host's extension library instead of inventing a core function.

## Preserve errors and complexity

`all` and `exists` combine predicate results using their Boolean semantics.
`exists_one` has a stricter need to determine exactly one satisfying member and
can expose errors that a successful `exists` could absorb. Test malformed members
alongside matching members. Do not assume a short-circuit at the first true match.
[Language definition](https://github.com/cel-expr/cel-spec/blob/master/doc/langdef.md).

Nested comprehensions multiply work. A validation comparing each item against every
other item grows with both list sizes. Prefer keyed lookup or a host-computed summary
when that preserves the intended decision and reduces repeated scanning.

## Check schema-dependent collection behavior

Kubernetes can give lists map/set semantics based on structural schema annotations.
Equality or concatenation in that environment can therefore differ from a plain
CEL list adapter. Keep those tests in the Kubernetes profile rather than changing
the general CEL fixture expectations.

For each collection rule, include empty, single, duplicate, boundary-length, and
malformed-member cases. If the input adapter drops invalid entries before evaluation,
record that normalization so reviewers know what the expression actually receives.
