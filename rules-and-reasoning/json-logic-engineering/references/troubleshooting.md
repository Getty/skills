# Troubleshooting

| Symptom | Inspect | Likely repair |
| --- | --- | --- |
| Empty array passes a host if-statement | Host vs JSON Logic truthiness | Use a typed result contract or deliberate JSON Logic truthiness |
| Rule returns a string instead of Boolean | `and`/`or` operand return | Make the desired output explicit |
| Null uses no default | `var` distinguishes explicit null | Validate or normalize according to the input contract |
| False or zero reported missing by application | Host presence test | Use actual own-property/schema checks |
| Empty string is reported missing by rule | `missing` semantics | Separate completeness from presence |
| Outer variable disappears in a map | Current item scope | Build explicit contexts or choose another expression model |
| Empty collection fails `all` | Quantifier empty-case convention | Decide and encode the empty-case requirement |
| Literal record produces unknown operation | One-key object ambiguity | Move record into data or declare a supported constructor |
| Frontend and backend disagree | Package/profile/schema revisions | Run identical typed fixtures on both |
| Custom conditional executes both branches | Eager custom arguments | Use the built-in control structure |
| Numerical result becomes null in JSON | Infinity/NaN serialization | Reject non-finite results before serialization |
| Adding metadata disables evaluation | Multiple keys at expression node | Move metadata into an outer envelope |
| Large request blocks the event loop | Collection size and nested iteration | Bound inputs and use an interruptible boundary |

## Diagnose in a controlled order

Capture the exact rule, a minimized non-sensitive input, expected result/type,
actual result/type, evaluator version, and custom operation registry. Reproduce with
the original caller first; then remove unrelated fields and nesting without changing
scope. Keep missing and explicit null distinct during minimization.

If the rule itself is correct, inspect preprocessing, data lookup, host coercion,
serialization, caching, and UI revision skew. Do not patch the AST to compensate for
an adapter bug without documenting the contract change.

For port disagreements, isolate one operation and one type pair. Compare upstream
tests and actual source for the pinned versions. A behavior in a popular implementation
is evidence for that implementation, not proof that all libraries must behave identically.

Use the semantic corpus and static inspector to narrow faults. The inspector's
restricted-profile rejection may be intentional even when the raw reference engine
would accept an expression; name that distinction in the report.

Authority: [operations](https://jsonlogic.com/operations.html),
[truthiness](https://jsonlogic.com/truthy.html),
[extension caveats](https://jsonlogic.com/add_operation.html).
