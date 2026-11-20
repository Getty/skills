# Rego semantics

## Values and documents

Identify JSON scalars, arrays, and objects, plus Rego sets. Treat `input` as the
request document and `data` as the root of loaded base and derived documents.
An absent path is not JSON null. Avoid object keys whose JSON serialization would
collide; Rego supports a wider key model than JSON.

Use assignment for introducing values, comparison for checks, and unification for
intentional structural relations. Do not replace `=` with `==` mechanically when
repairing a binding problem. [Language guide](https://www.openpolicyagent.org/docs/policy-language).

## Rules, alternatives, and conflicts

Give Boolean permission a complete-rule contract:

```rego
default allow := false
allow if { input.action == "read"; input.subject == input.resource.owner }
allow if { input.action == "read"; input.subject in data.reviewers }
```

Both alternatives contribute true. Two complete rules returning different prices
for the same input instead conflict. Use a collection of candidates only if that
is the intended domain result; otherwise make conditions disjoint or model priority.
An `else` chain supplies ordered fallback within a rule, not universal precedence
across every independent rule in a package.

Use `violations contains message if { ... }` to accumulate a set. Distinguish this
head keyword from the string `contains` built-in. The collection does not promise
ranking or duplication. [Contains reference](https://www.openpolicyagent.org/docs/policy-reference/keywords/contains).

## Quantification and absence

Use `some item in input.items` for existential search and `every item in input.items`
for a universal condition. Universal truth over an empty array succeeds; a nonempty
requirement needs a separate count check. Missing and wrong-type collections are
not empty arrays. See [some](https://www.openpolicyagent.org/docs/policy-reference/keywords/some)
and [every](https://www.openpolicyagent.org/docs/policy-reference/keywords/every).

| Observation | Meaning to preserve |
| --- | --- |
| `false` | Defined Boolean negative |
| No value | Undefined query or unsuccessful derivation |
| `null` | Defined null |
| Empty collection | Defined data; interpretation belongs to the caller |
| Error | Parse, compile, conflict, or runtime failure |

`default allow := false` supplies a value when the rule is otherwise undefined.
It does not convert every evaluator failure into false. See [default](https://www.openpolicyagent.org/docs/policy-reference/keywords/default).

## Negation and errors

Bind variables before negated use. Negation is not universal quantification over
unbound input. In legacy profiles, a composite negation can fail when an argument
or nested call is undefined before negation is applied. Current opt-in semantics
keep those computations within negation. Do not insert `rego.v2` or
`future.keywords.not` into old runtimes blindly. [Not reference](https://www.openpolicyagent.org/docs/policy-reference/keywords/not).

Inspect built-in support and strict-error settings. A failing built-in can yield
undefined in default native evaluation. A successful `opa eval` process is not a
true permission assertion. Test the precise query's type, value, and definedness.

For comprehensions, decide whether the output should be an array, set, or object.
Duplicate object keys with incompatible values indicate an invalid derivation;
deduplicating into a set can hide a cardinality defect if the business question
was about the number of occurrences. Preserve that distinction in tests.
