# Getty Bun integration review

Contract proposal v0.2.

## Subject and status

- Consumer and revision:
- agent-bun-runtime revision the starters were rendered from, or missing component:
- Exact Bun requirement (`gettyBun.bunVersion`, `vars.bun_version`) and contract version:
- Reviewed targets and table checksums:
- Agent client version, surface, and distribution route:
- Status: proposed / implemented / source-checked / executed on listed targets:

## Decisions and evidence

| Requirement | Implementation location | Evidence/result |
| --- | --- | --- |
| Canonical `gettyBun` pin in real package.json; CI validates it against the schema | | |
| Rendered `getty-bun.sh` and `getty-bun.ps1` committed under `bootstrap/`; CI: pin block equals package.json, fresh render (`render-pin.ts --check`) equals committed copy | | |
| Bundled entry committed (`bun build --target=bun`); CI rebuild byte-identical; no external packages | | |
| Hooks call the starter's `run`; only `run`, `ensure`, `status` used | | |
| Codex `command` and `commandWindows`; `"${PLUGIN_ROOT}"` quoted; `hooks.json` not shared with Claude Code | | |
| Claude Code adapter (Windows: open decision) | | |
| Hook timeouts set explicitly, above the lock wait plus one download; no starter call on `SessionEnd` or Codex `Interrupt` | | |
| First hook installs without external Bun/Node; concurrent hooks wait | | |
| Shared slot under `<GETTY_HOME>` per version/target/environment | | |
| Starter stdout clean, stderr messages; never exits 2 for its own failures; the entry's exit code passes through unchanged | | |
| Entry exit codes within 0–255; no entry argument begins with `-` | | |
| Windows: PowerShell 5.1 and 7, Process byte copy, Git Bash forwarding | | |
| Setup skill for repair and diagnosis | | |
| Side-by-side update; rollback by previous plugin release | | |
| Shared runtime survives consumer removal | | |
| Host review/activation observed (Codex re-review after changed bundled script) | | |
| Dependency install, consumer lock, binding (later, phase 5 only) | | |

## Checks performed

Record the concrete command or scenario, environment, observed result, and limits. Label each: documented, source-checked, schema-checked, scenario-reviewed, executed, measured by windows-developer, or not checked. Cite the agent-bun-runtime phase 1 gate (CI run and commit) for the starter revision instead of re-testing locking; it covers CI runners, not the host. Do not mark unexecuted platform cases as passed.

## Remaining gaps

Identify missing provider behavior, unsupported targets, untested host behavior, or required native review. State the practical next step without implying an unimplemented command exists.

## Sources

List primary documentation and inspected revisions supporting external facts. Mark Getty-specific layout, fields, and lifecycle rules as design decisions (agent-bun-runtime plan and ADRs).
