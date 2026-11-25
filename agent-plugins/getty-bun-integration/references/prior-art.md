# Prior art and metadata compatibility

Primary sources checked: **2026-11-25**. These are evolving documentation pages; recheck them before relying on new versions or platforms.

`getty-bun` is this skill's **proposed integration contract**, not a released runtime manager. The precedents below support individual design choices; they do not implement our complete contract or establish compatibility with every agent client.

## Relevant precedents

| Project | Verified precedent | Limits of the comparison |
| --- | --- | --- |
| OpenClaw | Its Bun installer reads the chosen application release's runtime pin, checks archive and executable hashes plus fork revision, stages `~/.openclaw/tools/bun-<tag>/bun`, and binds its Gateway service to the exact executable. Upgrading stages the new release's pin and updates the service binding. | Uses an OpenClaw Bun fork. This installer path supports macOS and glibc Linux x64/ARM64; it refuses Windows and musl/Alpine. It also manages global packages and PATH. This is an application installer, not a Claude Code or Codex plugin. |
| mise | A shared user installation store, exact per-project Bun versions, and explicit executable discovery support sharing one installed runtime version across projects. Its Bun documentation warns that `bun upgrade` changes a managed binary without updating the recorded version. | A separate version manager with shims and contextual selection. Its versioned directories are not technically immutable; Getty's no-in-place-update rule is a stricter ownership policy. |
| pnpm | `devEngines.runtime` supports Bun, Node.js, and Deno. With download behavior, pnpm resolves a runtime, records its exact version and checksum in the lockfile, and uses that runtime for scripts. | These are pnpm features, not behavior guaranteed by the JSON field or by Bun. pnpm requires its own bootstrap and may become a second runtime owner. This source does not establish Getty's store layout or absolute-path contract. |

Sources:

- [OpenClaw installer: Bun runtime](https://docs.openclaw.ai/install/installer#bun-runtime).
- [mise Bun integration](https://mise.jdx.dev/lang/bun.html), [installation directories](https://mise.jdx.dev/directories.html), and [mise which](https://mise.jdx.dev/cli/which.html). `mise which` resolves the actual executable, bypassing shims; `--tool` selects the tool/version. Integrations should use these interfaces instead of guessing mise's internal layout.
- [pnpm package.json: devEngines.runtime](https://pnpm.io/package_json#devenginesruntime).

OpenClaw also applies `--no-install` to its owned Bun subprocesses so missing imports fail instead of triggering runtime package downloads, including when the working directory enables automatic fallback installation. This supports Getty's explicit setup phase and predictable hook execution. It does not constrain subprocesses independently launched by third-party plugins. Source: [OpenClaw Bun](https://docs.openclaw.ai/install/bun).

## Why Getty uses its own small requirement field

The canonical v0.1 declaration is `package.json`'s `gettyBun` object, containing `contractVersion` and an exact `bunVersion`. These are **our own metadata fields**. The Getty provider must read and enforce them; Bun does not acquire that behavior merely because the fields exist. Ordinary package requirements remain in `dependencies` and `bun.lock`.

Existing `devEngines.runtime` metadata can be an optional tooling mirror when the chosen toolchain supports it. Its Bun version must equal the canonical Getty pin. Avoid two tools independently installing or switching the runtime. This choice avoids the following documented compatibility differences:

- **pnpm version matters.** Version 10.14 introduced runtime downloading with only `onFail: "download"` supported. Version 11.4 fixed enforcement for `onFail: "error"` and `"warn"`, which had previously done nothing. Current pnpm therefore supports a Bun object with `name`, an exact `version`, and `onFail: "error"`; older pnpm behavior must not be assumed equivalent. Sources: [pnpm 10.14](https://pnpm.io/blog/releases/10.14) and [pnpm 11.4, Other fixes](https://pnpm.io/blog/releases/11.4#other-fixes).
- **npm interprets runtime identity differently.** npm v12 documents `name` as required, `version` as optional, and `onFail` as `warn`, `error`, or `ignore`, defaulting to `error`. It assumes Node and rejects another runtime name under error behavior. Thus `runtime.name: "bun"` is not a universally compatible npm declaration. Its ordinary `engines` documentation concerns Node/npm compatibility; do not claim it installs or selects Bun. Source: [npm v12 package.json: devEngines and engines](https://docs.npmjs.com/cli/v12/configuring-npm/package-json/#devengines).
- **Overrides can change ownership.** Current pnpm exposes `runtimeOnFail` with `download`, `error`, `warn`, and `ignore`, overriding the manifest. Its `runtime: false` setting or `--no-runtime` skips runtime provisioning by installing commands. If pnpm is deliberately used alongside Getty, check the selected pnpm version and configure one owner; the Getty provider still verifies its binding itself. Source: [pnpm CLI settings: runtime and runtimeOnFail](https://pnpm.io/settings/cli#runtime).

## Design conclusions

Use shared, versioned runtime slots; bind consumers explicitly; stage and verify a new version before switching a consumer. Retaining older slots while consumers still reference them makes rollback possible. Treat these lifecycle rules as Getty policy, not as guarantees supplied by all the cited projects. Keep platform support, prerequisite installation, package dependency installation, and agent hook capabilities as separately verified concerns.
