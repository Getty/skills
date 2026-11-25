# Consumer setup skill authoring template

This is a template for the integration engineer, not a ready-to-run installer. Replace every `{{TOKEN}}` with verified consumer/provider details and package the resulting setup skill in the host's documented format. Do not ship unresolved tokens, assumed provider commands, or links to this engineering skill as if it were installed on every user's machine.

Suggested frontmatter for the rendered consumer skill:

```yaml
---
name: {{CONSUMER_SETUP_SKILL_NAME}}
description: Set up or repair {{CONSUMER_NAME}} by verifying its Getty-managed Bun runtime and installing its locked dependencies in the current execution environment.
---
```

## Setup procedure to adapt

1. Resolve this installed consumer's root using `{{HOST_ROOT_MECHANISM}}`. Read its actual `package.json` and `bun.lock`. Require a valid `gettyBun` object and an existing lockfile; do not infer the pin from PATH.
2. Identify the current execution environment. Resolve the provider root using `{{PROVIDER_ROOT_RESOLUTION}}`. Read the bundled provider integration instructions at `{{PROVIDER_REFERENCE_PATH}}` and verify that their implementation/API version matches this consumer.
3. Reuse an already verified exact version/target when available. Otherwise perform the real bootstrap operation `{{VERIFIED_BOOTSTRAP_ENTRY_POINT_AND_ARGUMENTS}}` using the available OS tools and session authorization. This entry point must work before external Bun/Node exists and own a validated mutex through shared installation mutations.
4. Inspect the operation's output and actual state. A `.installing` PID/name/start token is diagnostic; do not delete a held lock or kill a process from it. Follow the provider's supported wait/recovery flow. Report unsupported capabilities or inaccessible state explicitly.
5. Verify the selected executable's absolute path, exact version, target, receipt, and smoke result. Resolve the package at `{{CONSUMER_PACKAGE_RESOLUTION}}` and install its frozen dependencies using that executable under consumer-level coordination. Keep dependencies outside unrelated user project repositories.
6. Apply the documented lifecycle-script/native-dependency policy `{{DEPENDENCY_POLICY_REFERENCE}}`. Run the consumer check `{{VERIFIED_SMOKE_ENTRY_POINT_AND_ARGUMENTS}}`. Publish a binding only after success.
7. Configure ordinary execution with the selected absolute executable, `--no-install`, the absolute entry point, and correctly separated project input. Use `{{HOST_ACTIVATION_OR_REVIEW_PROCEDURE}}` for changed hooks; do not bypass trust controls.
8. Report the resolved path/version/target and checks actually performed. On failure, identify the failed step and retain any previous working binding. Do not claim successful setup from a marker or an agent message alone.

Honor existing authorization; do not ask again for already approved reversible setup. Do not add repeated installation to ordinary hooks. Keep the agent's setup tools available while this consumer is unready.
