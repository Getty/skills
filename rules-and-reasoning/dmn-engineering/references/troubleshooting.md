# Troubleshooting

| Symptom | Likely checks | Repair direction |
| --- | --- | --- |
| XML parses but deployment rejects it | Namespace, schema version, supported boxed expressions | Export a supported profile and validate actual target |
| Decision returns no value | Input name binding, no matching row, null expression, API wrapper | Inspect diagnostics and each input expression |
| Two matching rows fail | Unique overlap or Any unequal outputs | Repair partitions or explicitly revise policy |
| Wrong rule wins | First row order versus Priority output order | Restore intended ordering semantics |
| Aggregation is unexpectedly high | Multiple rows match; duplicate outputs legitimately count | Review predicates instead of silently deduplicating |
| String output becomes null | Unquoted FEEL name or unknown variable | Quote literal values and check diagnostics |
| A range rejects a boundary | Open/closed endpoint or numeric conversion | Add exact-boundary cases and consistent numeric binding |
| Diagram looks correct but result differs | Displayed DRD differs from underlying XML or extensions | Inspect the executable artifact and imported dependencies |
| Upgrade changes results | FEEL dialect, type conversion, time zone, bug fix, or defaults | Differential test the pinned old/new runtimes |
| Editor drops content | Unsupported imports/extensions/diagram profile | Preserve before/after files and use a compatible modeler |

## Reduce a failure

Capture the exact `.dmn` artifact, input context, requested decision/service, runtime
version, and unmodified error. Reproduce without downstream actions. Reduce to the
smallest decision and input that preserve the failure, then classify the layer:
serialization, binding, expression, table semantics, runtime support, or host mapping.
Do not rewrite the entire model before finding the failing layer.

For a null result, ask whether it was an intentional output, no match, a missing
input, or an expression error. Read the runtime diagnostics rather than assuming
all nulls mean ineligible. For a type error, inspect the original host value: a
JSON string containing digits remains a string unless explicitly converted.

## Resolve source disagreement

Compare the selected normative version with the engine documentation and a reduced
TCK case. Record known ambiguities such as compound Output Order in DMN 1.6 instead
of hiding them in an adapter. Check [OMG issues](https://issues.omg.org/issues/spec/DMN/1.6)
and [TCK cases](https://dmn-tck.github.io/tck/tests.html).

After the fix, run the regression that reproduced the defect plus neighboring
boundaries. Broaden testing only when the changed semantics or required deployment
gate warrants it. Report exactly what changed and which behavior remains untested.
