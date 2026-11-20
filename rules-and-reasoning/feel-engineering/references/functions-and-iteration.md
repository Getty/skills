# Functions, iteration, and quantifiers

## Call functions with a defined signature

Use positional arguments in declared order or supported named arguments with exact
parameter names. Verify arity and types. An unknown function or wrong signature can
produce null plus diagnostics rather than a useful value. Do not silently substitute
a similarly named JavaScript/Python function.

Define a reusable local function in a context when it improves clarity:

```feel
{scale: function(value, factor) value * factor,
 result: scale(7, 3)}.result
```

Keep injected external functions explicit in the runtime contract. A function
provider can introduce I/O, time dependence, exceptions, or unrestricted host code;
these are properties of the provider, not guaranteed by FEEL syntax.

## Reason about iteration shape

`for x in items return expression` produces a list. Multiple bindings generate a
Cartesian product, not corresponding pairs:

```feel
for x in [1,2], y in [10,20] return x + y
```

produces four values. If two lists should be zipped, define the intended length
and index mapping explicitly, including unequal-length handling. Bound input sizes
before permitting nested iterations in a user-facing service.

The special `partial` binding and sequence-iteration details require attention to
the selected specification/runtime. Prefer ordinary transformations for portable
rules; test accumulated-state examples before depending on them.

## Distinguish quantifiers and collection functions

`some x in items satisfies predicate` asks whether at least one element satisfies
the predicate. `every` asks whether all do. Over an empty list, some is false and
every is true. This is useful logic, but can be the wrong business rule when the
input must contain at least one approval. Add an explicit nonempty requirement.

Use built-in `all`/`any` for Boolean collections according to their documented null
rules. Do not replace null items with false as a generic preprocessing step.

## Audit collection and string functions

Check empty-list behavior separately for `sum`, `min`, `max`, `mean`, and count.
In FEEL, `sum([])` is null while `count([])` is zero. Preserve duplicates unless
`distinct values` is deliberately requested. Check sorting comparator expectations
and do not assume a host locale's collation applies.

For string processing, distinguish literal containment from regular expression
matching and pin the regex semantics used by the implementation. Avoid interpolating
untrusted patterns or using unbounded expensive matches in a service without limits.
Consult [DMN 1.6 §10.3.4](https://www.omg.org/spec/DMN/1.6/PDF) and the
[Camunda function API](https://docs.camunda.io/docs/components/modeler/feel/language-guide/feel-functions/).
