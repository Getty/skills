# Consumer setup skill authoring template

Contract proposal v0.2. This is a template for the integration engineer, not a ready-to-run procedure. In v0.2 the consumer's committed starter installs Bun on demand in its hooks; this skill is for **repair and diagnosis**, not installation. Replace every `{{TOKEN}}` with verified consumer details and package the result in the host's documented format. Do not ship unresolved tokens, starter commands other than `run`, `ensure`, `status`, or links to this engineering skill as if it were installed on every user's machine. The starters are built in agent-bun-runtime (`bootstrap/`, phase 1); ship a skill made from this template only with a consumer release that commits them.

Suggested frontmatter for the rendered consumer skill:

```yaml
---
name: {{CONSUMER_SETUP_SKILL_NAME}}
description: Diagnose or repair {{CONSUMER_NAME}} when its hooks report a getty-bun failure or stay silent — Bun runtime state, lock waits, Windows execution policy.
---
```

## Procedure to adapt

1. Resolve this installed consumer's root (`<consumer-root>` below) using `{{HOST_ROOT_MECHANISM}}`. The starters are `bootstrap/getty-bun.sh` and `bootstrap/getty-bun.ps1` under that root.
2. Identify the execution environment (Linux, native Windows, Git Bash, WSL, container). Use `sh "<consumer-root>/bootstrap/getty-bun.sh" status` on Linux and WSL, and on Windows `powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "<consumer-root>\bootstrap\getty-bun.ps1" status`. Under Git Bash, `getty-bun.sh` forwards to the PowerShell starter itself.
3. Run `status`. Report its JSON (`pin`, `target`, `slot`, `state`) as printed. `state` is `ready` (the slot matches the pin), `missing` (no slot) or `mismatch` (a slot that does not match); exit 1 instead of JSON means the state cannot be determined, for example an unsupported target. Claim nothing beyond these values.
4. If the state is `missing`, run `ensure`. It may wait up to `GETTY_BUN_LOCK_WAIT` seconds (default 300) for another install; that is normal after a plugin install or update. On failure, report its one `getty-bun: ` stderr line verbatim and the step it names.
5. A slot that fails closed (`mismatch`: receipt version or target not matching the pin, or the executable missing or empty): report the path from the message. A `ready` slot whose hooks end without a `getty-bun: ` line (exit 126, a crash) may hold a damaged executable, which the fast path does not detect: report that path too. Do not delete, overwrite, or "repair" a slot; there is no repair command. Removing a published slot needs every consumer using it to be idle and the user's explicit decision; the next call then installs it again.
6. Windows: if PowerShell refuses to run the script, an execution policy set by Group Policy may be overriding `-ExecutionPolicy Bypass` (Group Policy takes precedence over it: documented, about_Execution_Policies). Application control (AppLocker, WDAC) or antivirus may block it instead; under Git Bash that can show as exit 126 with the shell's own error line. Report the error text as printed; do not change policy or security settings.
7. Check that `gettyBun.bunVersion` in `package.json` equals the starters' pin and that the bundled entry `{{ENTRY}}` exists. A mismatch is a release defect: report it, do not patch the installed plugin.
8. If hooks still do not run, check the host's hook trust using `{{HOST_ACTIVATION_OR_REVIEW_PROCEDURE}}`; do not bypass trust controls.
9. Report what ran and what it printed. Do not claim readiness from a marker, a previous message, or this skill's completion.

Honor existing authorization; do not ask again for already approved reversible steps such as `ensure`. Do not add installation to hooks beyond the starter call, and do not set `GETTY_HOME` or `GETTY_BUN_MIRROR` unless the user asks for it.

A consumer on the later dependency-install path (plan phase 5) needs additional steps for its frozen-lockfile install and binding; v0.2 does not specify them.
