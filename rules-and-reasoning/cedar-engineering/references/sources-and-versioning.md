# Sources and versioning

Use the language reference as semantic authority, the SDK API and
release notes for implementation capabilities, and managed-service documentation for
service behavior. Original examples and helpers in this skill are not upstream
conformance tests and contain no copied production policy.

## Baselines

- [Language history](https://docs.cedarpolicy.com/other/doc-history.html): language 4.7,
  SDK 4.15.0, 2026-11-16; schema linking entered language 4.6.
- [SDK 4.15.0 API](https://docs.rs/cedar-policy/4.15.0/cedar_policy/): stable and
  experimental features, depth limits, and public types.
- [Official CLI release](https://github.com/cedar-policy/cedar/releases/tag/cedar-policy-cli-v4.15.0):
  executable used for example verification.
- [SDK changelog](https://github.com/cedar-policy/cedar/blob/main/cedar-policy/CHANGELOG.md):
  migration details; pin a tag when implementing rather than relying on moving `main`.

## Semantic and implementation sources

Use [authorization](https://docs.cedarpolicy.com/auth/authorization.html),
[policy syntax](https://docs.cedarpolicy.com/policies/syntax-policy.html),
[operators](https://docs.cedarpolicy.com/policies/syntax-operators.html),
[data types](https://docs.cedarpolicy.com/policies/syntax-datatypes.html),
[entities](https://docs.cedarpolicy.com/policies/syntax-entity.html),
[JSON input](https://docs.cedarpolicy.com/auth/entities-syntax.html),
[validation](https://docs.cedarpolicy.com/policies/validation.html),
[schemas](https://docs.cedarpolicy.com/schema/human-readable-schema.html),
[templates](https://docs.cedarpolicy.com/policies/templates.html), and
[schema linking](https://docs.cedarpolicy.com/schema/schema-linking.html).

For proof claims, read [How We Built Cedar: A Verification-Guided Approach](https://www.amazon.science/publications/how-we-built-cedar-a-verification-guided-approach)
and the [formal specification repository](https://github.com/cedar-policy/cedar-spec).
Distinguish machine-checked properties of a formal model from differential testing
of the implementation and from correctness of an application's authorization design.

For AWS integration, use the [Verified Permissions guide](https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/what-is-avp.html).
Do not infer service support from a newer open-source language release.

## Refresh procedure

Check language history, SDK changelog, selected binding, feature flags, and managed
service independently. Revalidate schemas and policies, replay decision/error cases,
and retest the input and enforcement adapters. Compare diagnostics as well as decisions.
Update the baseline only after recording observed compatibility. Cached search results
may lag current documentation; inspect the underlying primary source.
