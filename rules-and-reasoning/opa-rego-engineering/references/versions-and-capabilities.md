# Versions and capabilities

## Record the layers

Keep OPA binary/SDK version, Rego language profile, bundle profile, integration
release, and allowed features separate. An OPA 1.x release does not imply that all
bundles use the same dialect. The inspected baseline is **v1.22.4**, released
2026-11-12 — a pin, not a latest-version claim or a minimum requirement. [Releases](https://github.com/open-policy-agent/opa/releases).

## Upgrade v0 to v1

Use explicit v1 rule heads: `if` for bodies and `contains` for multi-value sets.
The `in`, `every`, `if`, and `contains` keywords are part of v1. `import rego.v1`
opts suitable older OPA releases into that behavior; it cannot upgrade arbitrary
old binaries. Check import shadowing and ambiguous head changes during migration.
[Upgrade guide](https://www.openpolicyagent.org/docs/v0-upgrade).

Inventory bundle producers and consumers together. A locally accepted source may
fail inside a controller carrying another OPA version. Prefer explicit bundle
language metadata for mixed deployments and use documented compatibility switches.
[v0 compatibility](https://www.openpolicyagent.org/docs/v0-compatibility).

## Account for v2 and semantic opt-ins

Current docs expose `rego.v2`, `future.keywords.and`, `future.keywords.or`, and
`future.keywords.not`. The latter changes composite negation, not merely formatting.
`and`/`or` express rule-body success/failure; do not assume arbitrary value-expression
use. [Import reference](https://www.openpolicyagent.org/docs/policy-reference/keywords/import).

Before enabling those features, replay missing nested fields, undefined function
results, mixed alternatives, negated calls, and keyword-name collisions. Record
changed decisions as intentional changes or defects. Do not upgrade a dialect just
to silence a linter without checking consumers.

## Compile against deployment capabilities

Use `opa capabilities` and the target capability file. Inspect built-ins, future
keywords, and feature flags, including v2 when relevant. Capabilities describe what
the compiler may assume; they do not constitute a complete network or native-code
sandbox. Retain process limits and host access controls. [Operations](https://www.openpolicyagent.org/docs/operations).

For each release:

1. Record binary/SDK versions and deployment image digests.
2. Check source using target capabilities.
3. Compare old/new evaluators on identical inputs and data revisions.
4. Build with explicit entrypoints and profile.
5. Verify actual consumer activation and rollback.

Keep compatibility exceptions narrow. A legacy bundle need not force every new
module into old syntax. Conversely, upgrading the CLI alone does not upgrade an
embedded Gatekeeper or Wasm runtime. Keep the example corpus as a stable baseline
and add profile-specific probes rather than changing all examples simultaneously.

## Reproduced negation boundary

Using official OPA 1.22.4, this original rule with empty input demonstrates the
profile distinction:

```rego
package probe
import rego.v1
deny if { not startswith(input.name, "ok") }
```

Querying `data.probe.deny` with `{}` was undefined under legacy v1 semantics.
Adding `import future.keywords.not`, or selecting `import rego.v2`, produced true
for the same expression and input. This is a real behavior change: include such
cases when migrating permission or violation logic. The probe establishes this
specific boundary, not general equivalence of the profiles.
