---
name: getty-bun-integration
description: Use when an agent plugin or tool must run TypeScript on Getty's shared per-user Bun runtime (getty-bun) — declaring the Bun version in package.json, wiring Claude Code or Codex hooks through the getty-bun starter, shipping a bundled entry, or reviewing such an integration.
---

# Getty Bun Integration

Build integrations against **Getty contract proposal v0.2**. The decisions come from the `getty-bun` repository (`docs/plan.md`, `docs/adr/`); where this skill disagrees, they win. **Built:** the starters `getty-bun.sh` and `getty-bun.ps1` in getty-bun `bootstrap/` (phase 1), tested in its CI on Linux and Windows runners; `bootstrap/README.md` there is their behavior contract. **Planned, not built:** the skilletor template `getty-bun-install` that delivers them, the SDK `@getty/bun-runtime`, and the host adapters. Never claim that a consumer ships the starters or that Codex or Claude Code ran them unless you observed it.

## Inspect the actual integration

1. Inspect the consumer repository, package manifests, release process, and target agent client. Follow repository instructions and preserve unrelated work.
2. Identify the execution environment: native Windows, Git Bash, Linux, macOS, WSL distribution, remote host, or container. Record the client version and distribution surface.
3. Read [the contract](references/contract.md). Missing provider behavior (the template, a target, a starter feature) is built in getty-bun first, not worked around in the consumer. The provider interface is `run`, `ensure`, `status`; invent no other commands.
4. Establish authorization from the session. Prepare concrete changes before required host trust/review; do not bypass it.

## Preserve the invariants

- Declare one exact runtime requirement in the consumer's real `package.json`: `gettyBun.contractVersion: 1` and `gettyBun.bunVersion`. Getty metadata, not Bun behavior; the consumer's CI validates it against the schema and keeps it equal to the starters' pin block.
- **The starter is the only installer.** Every `run`/`ensure` ensures the pinned Bun first: fast local check when present, install under the OS lock when missing. After a plugin install or update the first hook (normally `SessionStart`) installs; concurrent calls wait, bounded, on the same lock. `@getty/bun-runtime` never installs. The setup skill is repair and diagnosis.
- **Ship a bundled entry.** Commit `bun build --target=bun` output; no `bun install` on user machines. Frozen-lockfile installs under a consumer lock are a later option for consumers that cannot bundle.
- Share one verified installation per exact **version and target within one execution environment**, in immutable slots under `<GETTY_HOME>/runtimes`, outside plugin caches. Never overwrite a published slot; a mismatch fails closed.
- Run Bun by absolute path with `--no-install`. Never PATH, shell startup files, a `current` link, `bun upgrade`, `bunx`, or a shebang.
- stdout belongs to the entry; starter messages go to stderr. The starter never exits 2 for its own failures; the entry's exit code passes through unchanged. Keep entry exit codes within 0–255 and let no entry argument begin with `-`; both limits come from Windows and hold on every OS.
- Hold the OS-backed mutex throughout shared installation mutations; `.installing` is diagnostics, never ownership. Never remove a lock because a PID looks dead.

## Implement in order

### 1. Declare the pin

Merge [package.fragment.json](assets/package.fragment.json) deliberately; its version is getty-bun's pin when this was written, so check the current one there (plan, "Decided"; `bootstrap/versions.json`). Validate with [requirement.schema.json](assets/requirement.schema.json). Set the same version as `vars.bun_version` for `getty-bun-install` once the template exists. Targets and roots: [paths-platforms.md](references/paths-platforms.md).

### 2. Commit the rendered starters

Commit both starters as `bootstrap/getty-bun.sh` and `bootstrap/getty-bun.ps1`; the consumer root is the parent of `bootstrap/`. Until `getty-bun-install` exists and skilletor can render into a plugin, copy them from getty-bun `bootstrap/`, rendered for the consumer's version, and let CI run `render-pin.ts --check` ([contract.md](references/contract.md), "Delivery"). Do not write installer or locking code in the consumer; [installation-locking.md](references/installation-locking.md) is the contract the starters implement and the review checklist for them.

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

Use [verification.md](references/verification.md) and [integration-review-template.md](assets/integration-review-template.md). Label evidence: documented, source-checked, schema-checked, scenario-reviewed, executed (for getty-bun's CI: run ID and commit), measured by windows-developer, or not checked. Deliver concrete changes, the exact pin, supported/tested targets, update behavior, and remaining gaps. Cite the getty-bun phase 1 gate for the starters; it covers CI runners, not a host or a desktop.

## Research and rationale

[prior-art.md](references/prior-art.md) covers OpenClaw, mise, pnpm, and metadata compatibility; [prior-art-plugins.md](references/prior-art-plugins.md) covers AgentPulse, GStack, and Claude-mem; [sources.md](references/sources.md) maps primary sources, the getty-bun decisions, and the windows-developer measurements. Attribute external facts; mark Getty paths, fields, locking policy, and lifecycle rules as our proposal.
