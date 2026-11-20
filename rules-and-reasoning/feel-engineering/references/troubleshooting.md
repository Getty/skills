# Troubleshooting FEEL

| Symptom | Check first | Typical correction |
| --- | --- | --- |
| A literal-looking word returns null | It may be a variable lookup | Quote string literals |
| `< 20` does not parse | Expression mode versus unary-test mode | Use correct entry point or `x < 20` |
| An expression starting with `=` fails | Product marker passed into raw parser | Remove host marker only at the boundary |
| A list returns the wrong element | One-based/negative indexing | Correct the index and test zero/out-of-range |
| Empty input is accepted | `every []` or a default empty list | Add explicit nonempty/required input condition |
| Missing score becomes failure | Null comparison drives else branch | Model an explicit missing-data outcome |
| Total differs between engines | Decimal representation or input conversion | Inspect precision and run the decimal probe |
| Context entry is unavailable | Forward reference, duplicate key, or scope | Reorder dependencies or rename bindings |
| Date result shifts | Local versus offset/zone, clock, serialization | Pin temporal contract and reference time |
| Function works in one product only | Vendor extension/provider | Use a portable function or document dependency |

## Reduce the failing example

Capture source, bindings, mode, runtime/dialect, result, and diagnostics. Remove
surrounding DMN/workflow logic only after preserving the actual bound types. Test
subexpressions independently, then rebuild the original expression. Do not replace
a typed host value with a string during reduction; that can create a different bug.

For null, trace name resolution and function signatures before adding a fallback.
For a parse error, inspect operator syntax, parentheses, and host markers before
changing the business expression. For a cross-engine difference, read the normative
clause and test an isolated example.

## Check safety of an apparent fix

Switching FEEL to B-FEEL, coercing all strings to numbers, converting all nulls to
false, and replacing missing collections with empty lists are semantic changes.
Use them only when the business contract calls for them and document the changed
cases. A warning-free result can still be numerically wrong for the intended
contract, as the bundled decimal probe demonstrates.

Use [OMG DMN 1.6](https://www.omg.org/spec/DMN/1.6/PDF), the exact engine source
or docs, and [known issues](https://issues.omg.org/issues/spec/DMN/1.6) to resolve
behavior. Report an unresolved specification or implementation gap rather than
asserting a universal interpretation unsupported by the evidence.
