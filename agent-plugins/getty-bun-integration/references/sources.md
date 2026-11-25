# Primary source map

Checked: 2026-11-25. Refresh changing host APIs, release artifacts, and platform support before implementing a new integration. Getty paths, metadata, lifecycle policy, and lock protocol are contract proposal v0.2; these sources support external behavior and precedents.

## Getty decisions and measurements

| Source | What it holds |
| --- | --- |
| Repository `getty-bun` (`Getty/getty-bun`): `docs/plan.md`, `docs/adr/0001`–`0006` | The decisions behind v0.2: starter interface, install on demand, bundled entry, one starter per OS, version table and pin, npm distribution, phases and open decisions. They win over this skill. |
| `getty-bun` `bootstrap/` at `262bc95`: `getty-bun.sh`, `getty-bun.ps1`, `versions.json`, `render-pin.ts`, `README.md` | The built starters. The README is their behavior contract (pin block, render CLI, receipt, `.installing`, tools, Windows limits) and labels each claim with the CI run that executed it. |
| `getty-bun` CI runs 45603412444 and 45604685681 on `262bc95`; `docs/hook-cost.md` (runs 45572032454, 45579886904, 45589361806) | The phase 1 gate: scenario suite on linux-x64, linux-arm64, Windows 5.1 and 7, all jobs green. Per-hook cost on the CI runners, Defender real-time protection off. |
| `getty-bun` project skills `getty-bun-bootstrap`, `getty-bun-windows` | Starter invariants, target detection, PowerShell 5.1 rules. Where they and `bootstrap/README.md` differ, the README describes what is built. |
| Hub `windows-developer`: `docs/hook-start-windows.md`, `docs/starter-konvention.md`, `docs/umgebung.md` | Measurements on Windows 11 with Claude Code 2.1.287: hook start forms, path forms, stdin/stdout, PowerShell start cost, probe y4. Codex was not installed there. |
| Hub `agent-developer`: `docs/windows-referenzen.md` (hub-researcher) | Read, not executed: Claude Code hook fields and exec form (CHANGELOG at `anthropics/claude-code` `4cc5e8b`), Codex shell selection and textual `${PLUGIN_ROOT}` substitution (`openai/codex` `3f65e9f`), Bun `install.ps1`, claude-mem's stdin handling. |
| `openai/codex` `3f65e9f`: `codex-rs/core/src/session/mod.rs`, `core/src/shell.rs`, `core/src/environment_selection.rs`, `hooks/src/engine/command_runner.rs` | Read, not executed (hub review of 2026-11-25): hooks run in the turn environment's session shell without login; `$SHELL -lc` or `%COMSPEC% /C` only as the fallback without a single local environment. |

## Bun

| Source | What to verify |
| --- | --- |
| [Installation](https://bun.sh/docs/installation) and [release assets](https://github.com/oven-sh/bun/releases) | Exact release artifacts, OS/CPU/ABI requirements, version probes, `SHASUMS256.txt` and its signature `SHASUMS256.txt.asc`. |
| [Bundler](https://bun.com/docs/bundler) | `--target=bun`, the `// @bun` pragma, `packages`/`external` and what stays a runtime import. |
| [Runtime](https://bun.com/docs/runtime) | Direct TS/JS execution, flag placement, `--no-install`, script execution behavior. |
| [Install dependencies](https://bun.com/docs/pm/cli/install) | Frozen installation, absent-lockfile behavior, lifecycle scripts (later dependency-install path only). |
| [Auto-install](https://bun.com/docs/runtime/auto-install) | Runtime package fetching and why recurring execution disables it. |
| [Unix installer source](https://bun.com/install), [Windows installer source](https://bun.sh/install.ps1) | PATH/profile side effects; why the starters do not use them. |

## Agent hosts

| Source | What to verify |
| --- | --- |
| [Claude mods creation](https://code.claude.com/docs/en/plugins/mods/create), [reference](https://code.claude.com/docs/en/plugins/mods/reference), [API](https://code.claude.com/docs/en/plugins/mods/api) | The optional repair-hint mod, middleware, context caching. |
| [Claude published types](https://github.com/anthropics/claude-code/blob/fa0dece70669a54b3104c618de9eebaaa78af19f/mods/types/claude-code.d.ts) | Pinned source for the supplied `prompt.context` example; compare installed declarations. |
| [Claude hooks](https://code.claude.com/docs/en/hooks), [loading](https://code.claude.com/docs/en/plugins/loading), [manifest](https://code.claude.com/docs/en/plugins/manifest-reference) | Concurrency, hook outputs, default timeouts and the `SessionEnd` budget, exec versus shell form, lifecycle, data/cache paths, activation and manifest behavior. |
| [Codex plugin packaging](https://developers.openai.com/plugins/build/plugins.md) | Onboarding metadata, package formats, host/distribution scope. |
| [Codex local hooks](https://learn.chatgpt.com/docs/hooks.md) | Supported handlers, concurrency, context outputs, `commandWindows`, `PLUGIN_ROOT`/`CLAUDE_PLUGIN_ROOT`, timeouts, working directory, trust review and re-review after a changed bundled script. |

## Locking and Windows

| Source | What to verify |
| --- | --- |
| [Linux flock(1)](https://man7.org/linux/man-pages/man1/flock.1.html), [flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html), [execve(2)](https://man7.org/linux/man-pages/man2/execve.2.html) | Retained descriptors, inherited ownership, lock-family differences, filesystem limitations; descriptors surviving `exec`, the reason the starter closes the lock before Bun starts. |
| [Apple lockf(1) source](https://raw.githubusercontent.com/apple-oss-distributions/shell_cmds/main/lockf/lockf.1) | Descriptor mode and permanent backing-file behavior; probe actual OS availability. |
| [Microsoft File.Open](https://learn.microsoft.com/en-us/dotnet/api/system.io.file.open?view=netframework-4.8.1), [FileShare](https://learn.microsoft.com/en-us/dotnet/api/system.io.fileshare?view=netframework-4.7.2) | Exclusive open and stream lifetime for the Windows starter. |
| [about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies) | Group Policy takes precedence over `-ExecutionPolicy Bypass` (5.1 and 7 views). |
| [Linux /proc](https://www.kernel.org/doc/html/latest/filesystems/proc.html), [Windows Process.StartTime](https://learn.microsoft.com/dotnet/api/system.diagnostics.process.starttime) | Process identity diagnostics and their availability. |

## Prior implementations and toolchain metadata

See [prior-art.md](prior-art.md) for OpenClaw, mise, pnpm, and npm with exact primary links and limitations. See [prior-art-plugins.md](prior-art-plugins.md) for commit-pinned AgentPulse, GStack, and Claude-mem sources. Do not replace those inspected revisions with current `main` without rechecking the claims.
