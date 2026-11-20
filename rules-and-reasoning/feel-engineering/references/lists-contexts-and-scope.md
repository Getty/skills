# Lists, contexts, and scope

## Separate indexing, filtering, and projection

Lists are ordered and immutable. The first element is `[1]`; the last is `[-1]`.
A zero/out-of-range index yields null. A numeric bracket expression means indexing,
whereas a Boolean expression filters:

```feel
[4, 8, 12][2]
[4, 8, 12][item > 5]
```

The results are `8` and `[8,12]`. A filter retains only elements for which the
predicate is true. Null predicates do not keep an item. Do not infer that the source
list is empty merely because filtering excluded records with missing information.

Path projection preserves positions:

```feel
[{code: "a"}, {other: "b"}].code
```

returns `["a", null]` under the standard semantics. Adding a filter that checks
for a non-null code changes the cardinality intentionally. Record whether downstream
logic needs aligned positions or only present values.

## Build contexts with ordered dependencies

A context associates keys with values; entries can use earlier entries:

```feel
{base: 12, factor: 3, total: base * factor}.total
```

returns `36`. Do not assume a forward reference resolves to a later context entry.
Avoid duplicate keys and accidental shadowing of outer variables. Quoted keys are
keys, quoted string literals are values, and a bare name is a lookup.

Distinguish `customer.address.city` from a single external key containing dots.
Normalize awkward external keys into a deliberate context or use the implementation's
supported key-access function. Never rewrite customer data into expression source
in order to access it.

## Treat names as part of the profile

FEEL grammar supports expressive names, including multiword names in appropriate
contexts. Parser disambiguation and host variable rules can be narrower. A workflow
product may prohibit spaces in process-variable identifiers even when a standalone
FEEL parser supports them. Choose unambiguous names for portable application
bindings and record any escaping convention as engine-specific.

Use scope deliberately in nested contexts, filters, functions, and iterations.
Explicit iteration names can be clearer than relying on a field name imported
implicitly into a filter's scope. Test an input where an outer variable has the
same name as a field to expose accidental capture.

Read [DMN 1.6 §10.3.2.5–6](https://www.omg.org/spec/DMN/1.6/PDF), and the
[Camunda list](https://docs.camunda.io/docs/components/modeler/feel/language-guide/feel-list-expressions/)
and [context guides](https://docs.camunda.io/docs/components/modeler/feel/language-guide/feel-context-expressions/)
for the selected host's behavior.
