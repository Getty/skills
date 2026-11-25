---
name: getty-bun-integration
description: Use when an agent plugin or tool must run TypeScript on Getty's shared per-user Bun runtime (getty-bun) — declaring the Bun version in package.json, wiring Claude Code or Codex hooks through the getty-bun starter, shipping a bundled entry, or reviewing such an integration.
---

# Getty Bun Integration

Build integrations against **Getty contract proposal v0.2**. The decisions come from the `getty-bun` repository (`docs/plan.md`, `docs/adr/`); where this skill disagrees, they win. **Nothing is implemented yet:** the starters `getty-bun.sh` and `getty-bun.ps1` and the skilletor template `getty-bun-install` that delivers them are planned (getty-bun phase 1), not built or tested. Never describe them as existing.

## Inspect the actual integration

1. Inspect the consumer repository, package manifests, release process, and target agent client. Follow repository instructions and preserve unrelated work.
2. Identify the execution environment: native Windows, Git Bash, Linux, macOS, WSL distribution, remote host, or container. Record the client version and distribution surface.
3. Read [the contract](references/contract.md). Check whether the starters exist in getty-bun; if not, building them there is the first task, not a consumer workaround. The provider interface is `run`, `ensure`, `status`; invent no other commands.
4. Establish authorization from the session. Prepare concrete changes before required host trust/review; do not bypass it.

## Preserve the invariants

- Declare one exact runtime requirement in the consumer's real `package.json`: `gettyBun.contractVersion: 1` and `gettyBun.bunVersion`. Getty metadata, not Bun behavior; the consumer's CI validates it against the schema and keeps it equal to the starters' pin block.
- **The starter is the only installer.** Every `run`/`ensure` ensures the pinned Bun first: fast local check when present, install under the OS lock when missing. After a plugin install or update the first hook (normally `SessionStart`) installs; concurrent calls wait, bounded, on the same lock. `@getty/bun-runtime` never installs. The setup skill is repair and diagnosis.
- **Ship a bundled entry.** Commit `bun build --target=bun` output; no `bun install` on user machines. Frozen-lockfile installs under a consumer lock are a later option for consumers that cannot bundle.
- Share one verified installation per exact **version and target within one execution environment**, in immutable slots under `<GETTY_HOME>/runtimes`, outside plugin caches. Never overwrite a published slot; a mismatch fails closed.
- Run Bun by absolute path with `--no-install`. Never PATH, shell startup files, a `current` link, `bun upgrade`, `bunx`, or a shebang.
- stdout belongs to the entry; starter messages go to stderr. The starter never exits 2 for its own failures; the entry's exit code passes through unchanged.
- Hold the OS-backed mutex throughout shared installation mutations; `.installing` is diagnostics, never ownership. Never remove a lock because a PID looks dead.

## Implement in order

### 1. Declare the pin

Merge [package.fragment.json](assets/package.fragment.json) deliberately; its version is illustrative. Validate with [requirement.schema.json](assets/requirement.schema.json). Set the same version as `vars.bun_version` for `getty-bun-install`. Targets and roots: [paths-platforms.md](references/paths-platforms.md).

### 2. Commit the rendered starters

Once `getty-bun-install` exists, render it for the consumer and commit both starters; until skilletor can render into a plugin, copy them by hand and let CI compare with a fresh render ([contract.md](references/contract.md), "Delivery"). Do not write installer or locking code in the consumer; [installation-locking.md](references/installation-locking.md) is the contract the starters implement and the review checklist for them.

### 3. Bundle the entry

Read [dependencies-and-execution.md](references/dependencies-and-execution.md). Commit the bundle; CI rebuilds with the pinned Bun and compares byte for byte.

### 4. Wire the host

- Codex: [codex.md](references/codex.md): `command` runs `getty-bun.sh`, `commandWindows` the PowerShell starter; hook trust and re-review.
- Claude Code: [claude-code.md](references/claude-code.md): shell-form hook on Linux; the Windows adapter is an open decision.
- Hermes or another host: apply the contract and inspect current official interfaces; this skill ships no Hermes adapter.

Set every starter hook's `timeout` explicitly, above the lock wait plus one download; put no starter call on `SessionEnd` (or Codex `Interrupt`), whose budget is seconds. Treat host examples as source-checked until exercised in the actual client.

### 5. Package the setup skill

Read [setup-and-installation.md](references/setup-and-installation.md) and adapt [setup-skill-template.md](assets/setup-skill-template.md) for repair and diagnosis through `status` and `ensure`.

### 6. Handle updates and retention

Read [updates-and-retention.md](references/updates-and-retention.md). A Bun bump re-renders the starters and rebuilds the bundle in one release; the new slot installs beside the old one. No automatic pruning.

### 7. Verify and deliver

Use [verification.md](references/verification.md) and [integration-review-template.md](assets/integration-review-template.md). Label evidence: documented, source-checked, schema-checked, scenario-reviewed, executed, measured by windows-developer, or not checked. Deliver concrete changes, the exact pin, supported/tested targets, update behavior, and remaining gaps. Never describe the starters as installed or cross-platform tested because this skill exists.

## Research and rationale

[prior-art.md](references/prior-art.md) covers OpenClaw, mise, pnpm, and metadata compatibility; [prior-art-plugins.md](references/prior-art-plugins.md) covers AgentPulse, GStack, and Claude-mem; [sources.md](references/sources.md) maps primary sources, the getty-bun decisions, and the windows-developer measurements. Attribute external facts; mark Getty paths, fields, locking policy, and lifecycle rules as our proposal.
