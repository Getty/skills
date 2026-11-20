# Validation and testing

## Keep the layers separate

Parse/format source, run compiler checks, check schemas/capabilities, execute policy
cases, exercise the integration, and measure operational limits where relevant.
Do not call source fully validated merely because `opa check` succeeded. Schema-aware
compiler checking does not validate every runtime input. Inspect installed command
help for supported flags. [CLI reference](https://www.openpolicyagent.org/docs/cli).

## Assert exact outcomes

Write descriptive `test_` rules and substitute facts using `with`. For defined
Boolean permissions, assert `allow == false` on a denial; `not allow` can also
succeed when a broken policy became undefined. Keep expected values independent of
the condition under test wherever possible.

| Case | Failure it can expose |
| --- | --- |
| Owner read | Broken intended access |
| Cross-tenant editor | Tenant boundary bypass |
| Revoked identity | Ignored activity status |
| Missing subject/resource | Undefined accepted as permission |
| Wrong type | Input assumptions |
| Empty collection | Vacuous universal truth |
| Overlapping output rules | Conflicts or incorrect precedence |
| Built-in failure | Error-policy mismatch |

Use coverage to find unexercised paths, then check whether the exercised paths
actually include difficult boundaries. Parameterized tests and coverage reporting
are available in OPA; choose forms supported by the target release.
[Policy testing](https://www.openpolicyagent.org/docs/policy-testing).

## Compare versions and targets

Replay identical cases on old/new profiles and native/Wasm engines. Compare values,
types, errors, and definedness. Normalize ordering only for collections whose
contract is unordered. Include nested missing references in negation migrations.
Classify every mismatch before accepting a new runtime.

Application tests must still verify authentication and authoritative lookup. A Rego
case with handwritten `input.subject` cannot prove that a gateway verifies sessions.
A controller case with only the rule cannot prove the constraint matches the
intended namespace and resource operation.

## Preserve useful evidence

Record exact engine, policy/data revisions, capabilities, commands, and observed
results. If an evaluator is unavailable, report structural checks and unexecuted
layers explicitly. Do not implement a lightweight imitation of Rego and present it
as runtime validation.

Keep minimal redacted regression cases for defects. Prefer a case that falsifies
the old behavior to a test that merely repeats the implementation. Stop optional
testing after concrete risks and required gates are covered; expanding a corpus
without a remaining question can dilute the useful signal.
