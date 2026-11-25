# Primary source map

Checked: 2026-11-25. Refresh changing host APIs, release artifacts, and platform support before implementing a new integration. Getty paths, metadata, lifecycle policy, and lock protocol are proposals; these sources support external behavior and precedents.

## Bun

| Source | What to verify |
| --- | --- |
| [Installation](https://bun.sh/docs/installation) and [release assets](https://github.com/oven-sh/bun/releases) | Exact release artifacts, OS/CPU/ABI requirements, version probes. |
| [Runtime](https://bun.com/docs/runtime) | Direct TS/JS execution, flag placement, `--no-install`, script execution behavior. |
| [Install dependencies](https://bun.com/docs/pm/cli/install) | Frozen installation, absent-lockfile behavior, lifecycle scripts, production dependency selection. |
| [Auto-install](https://bun.com/docs/runtime/auto-install) | Runtime package fetching and why recurring execution disables it. |
| [Unix installer source](https://bun.com/install), [Windows installer source](https://bun.sh/install.ps1) | Release argument, private install directory, PATH/profile side effects and switches. |

## Agent hosts

| Source | What to verify |
| --- | --- |
| [Claude mods creation](https://code.claude.com/docs/en/plugins/mods/create), [reference](https://code.claude.com/docs/en/plugins/mods/reference), [API](https://code.claude.com/docs/en/plugins/mods/api) | Native adapters, middleware, context caching, prompt submission. |
| [Claude published types](https://github.com/anthropics/claude-code/blob/fa0dece70669a54b3104c618de9eebaaa78af19f/mods/types/claude-code.d.ts) | Pinned source for the supplied `prompt.context` example; compare installed declarations. |
| [Claude hooks](https://code.claude.com/docs/en/hooks), [loading](https://code.claude.com/docs/en/plugins/loading), [manifest](https://code.claude.com/docs/en/plugins/manifest-reference) | Concurrency, hook outputs, lifecycle, data/cache paths, activation and manifest behavior. |
| [Codex plugin packaging](https://developers.openai.com/plugins/build/plugins.md) | Onboarding metadata, package formats, host/distribution scope. |
| [Codex local hooks](https://learn.chatgpt.com/docs/hooks.md) | Supported handlers, concurrency, context outputs, Windows command override, native trust review. |

## Locking

| Source | What to verify |
| --- | --- |
| [Linux flock(1)](https://man7.org/linux/man-pages/man1/flock.1.html), [flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html) | Retained descriptors, inherited ownership, lock-family differences, filesystem limitations. |
| [Apple lockf(1) source](https://raw.githubusercontent.com/apple-oss-distributions/shell_cmds/main/lockf/lockf.1) | Descriptor mode and permanent backing-file behavior; probe actual OS availability. |
| [Microsoft File.Open](https://learn.microsoft.com/en-us/dotnet/api/system.io.file.open?view=netframework-4.8.1), [FileShare](https://learn.microsoft.com/en-us/dotnet/api/system.io.fileshare?view=netframework-4.7.2) | Exclusive open and stream lifetime for the Windows candidate. |
| [Linux /proc](https://www.kernel.org/doc/html/latest/filesystems/proc.html), [Windows Process.StartTime](https://learn.microsoft.com/dotnet/api/system.diagnostics.process.starttime) | Process identity diagnostics and their availability. |

## Prior implementations and toolchain metadata

See [prior-art.md](prior-art.md) for OpenClaw, mise, pnpm, and npm with exact primary links and limitations. See [prior-art-plugins.md](prior-art-plugins.md) for commit-pinned AgentPulse, GStack, and Claude-mem sources. Do not replace those inspected revisions with current `main` without rechecking the claims.
