# Packaging, distribution, and updates

Ship a standalone plugin repository for third-party integrations. Prefer documented hooks, providers, middleware, and SDK contributions; avoid replacing Hermes core functions or private tables at runtime. The [native compatibility policy](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins) treats those patches as unsupported.

## Package inventory

Include only the runtime layers needed: native manifest/code, bundled skills, dependencies, Desktop source, Dashboard bundle, backend API, and plugin-owned assets. A plugin repository can have user documentation and release notes; do not confuse that artifact with this authoring skill's reference layout.

Keep the package tree immutable at runtime. Use profile-scoped plugin data for state, not files under the install directory. Preserve state during ordinary updates and document explicit reset/delete behavior separately.

## Development checks

Run the target version's validator and Plugin Doctor using its documented syntax. Current Doctor accepts:

```bash
hermes plugins doctor /absolute/path/to/plugin --ci
```

Doctor executes the real discovery/import/registration path with a temporary Hermes home. It is not a sandbox for untrusted code; subprocesses and in-process privileges still matter. A passed Doctor establishes registration behavior, not the semantics of external business actions.

## Reproducible installation

The [plugin installation reference](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins) supports immutable full commit pins:

```bash
hermes plugins install owner/repository --ref FULL_40_CHARACTER_COMMIT_SHA --no-enable
hermes plugins list
hermes plugins enable EFFECTIVE_PLUGIN_KEY
```

These are command templates: replace the source, full SHA, and discovered key. Do not run the placeholders. Keep enablement and dependency/capability consent explicit. A pinned install should not silently follow a moving branch; adopt a new reviewed SHA deliberately.

## Dependency ownership

On a PM-managed Hermes installation, declare Python dependencies and let the host's dependency admission prepare a compatible environment. Do not mutate the selected environment with ad-hoc pip installation during discovery or import. Account for Hermes' own pins and the union of enabled plugins.

Bound requirements to compatible versions and test the oldest supported API. Keep optional integrations optional. Use an isolated sidecar when dependencies genuinely conflict and the architecture can support a stable RPC boundary; document who starts and supervises it.

## Catalog

Read the current [catalog submission policy](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission). Catalog entries require an exact reviewed source pin, truthful metadata, supported SDK/core extension behavior, and admission checks. The catalog's compatibility floor uses Hermes SemVer, not the date-style release tag.

Do not add self-updating code or remote JS loaders that move execution beyond the reviewed package. Review new grants and dependency changes when updating the pin.

## Upgrade and rollback

Test old state with new code, then rollback code against retained state. If migration is irreversible, make the incompatibility explicit before rollout and retain a usable backup/export. Avoid source changes to the user's main Hermes installation when a standalone plugin suffices.

