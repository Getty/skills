# Testing and conformance

## Validate in layers

| Layer | Evidence | Does not establish |
| --- | --- | --- |
| Strict JSON | Parser rejects malformed text/duplicate keys/non-finite literals | Supported operations |
| Authoring profile | Allowed AST shapes, operations, arities, size/depth | Runtime correctness |
| Input contract | Facts meet schema and trusted binding rules | Intended business meaning |
| Runtime cases | Selected engine returns expected values/errors | Every engine agrees |
| Differential checks | Named versions agree on supplied corpus | Universal equivalence |
| Domain review | Reviewed cases match source intent | Completeness of real-world facts |

The project publishes a shared [test corpus](https://jsonlogic.com/tests.json).
Pin the retrieved bytes and keep its provenance. Treat it as compatibility evidence,
not certification by an external standards body. Include application-specific
cases: upstream tests do not know the intended rule or its trusted inputs.

## Design tests that catch semantic faults

Compare actual values and types. Preserve missing/null/false/zero/empty string/empty
list distinctions. Include operand-returning `and`/`or`, an unchosen branch that
would otherwise error, an unknown operation, strict versus coercing equality,
quantifiers over empty lists, nested scope, and reduction initialization.

Test input schema separately from raw evaluator behavior. A coercing runtime may
return true for an invalid numeric string; the system contract should reject that
input before evaluation. Do not hide this by rewriting the expected business value.

For numeric outputs, decide whether approximate comparison is permitted and document
the tolerance. Never use a tolerance to conceal changed units or gross rounding.
Reject non-finite results at the adapter. In JavaScript, serializing Infinity as
JSON can conceal it as null.

## Verify helpers and changes

Run `inspect_rule.py` on accepted examples and negative probes for duplicate keys,
unknown operators, invalid arity, excessive depth, and forbidden static path segments.
Run `run_cases.cjs` with a trusted pinned evaluator. Verify that a deliberately wrong
expected value causes a nonzero exit, then discard that temporary probe.

For a release, record runtime/version, corpus revision/hash, supported profile, result
count, and untested ports. Keep deployment smoke checks focused on the actual adapter.
Do not call a static inventory or a few passing examples full JSON Logic conformance.

The bundled semantic corpus is original. It is intentionally small enough to inspect
and emphasizes behavioral distinctions rather than restating implementation code.
