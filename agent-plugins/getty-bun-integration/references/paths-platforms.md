# Paths and platform selection

Status: Getty contract proposal v0.2. Use [contract.md](contract.md) for ownership and canonical fields. Windows facts marked "measured by windows-developer" come from that hub (`docs/hook-start-windows.md`, `docs/starter-konvention.md`, `docs/umgebung.md`; Claude Code 2.1.287, Windows 11 25H2, PowerShell 5.1.26100). Facts marked executed come from getty-bun's CI on `windows-latest` (a server image, Defender real-time protection off); getty-bun `bootstrap/README.md` names the run per claim. Everything else on Windows is source-checked or not checked.

## Resolve the root once, then use absolute paths

`GETTY_HOME`, if set, is the root and must be absolute. Otherwise:

| Environment | Default root | Executable |
| --- | --- | --- |
| Linux (macOS later) | `~/.getty` | `<GETTY_HOME>/runtimes/bun/<version>/<target>/bin/bun` |
| Native Windows | user profile (`[Environment]::GetFolderPath('UserProfile')`) plus `\.getty` | `<GETTY_HOME>\runtimes\bun\<version>\<target>\bin\bun.exe` |
| Git Bash, MSYS, Cygwin | as native Windows: `getty-bun.sh` forwards to `getty-bun.ps1` | the same slot as native Windows |
| WSL | the distribution's Linux home | Linux layout and target; never a Windows `bun.exe` |
| Remote/container | the home of the user/environment actually executing the tool | that environment's OS layout |

On Windows, do not derive the root from `$HOME` or `$env:HOME`: Git Bash sets `HOME` to a `/c/Users/...` path. Tildes and angle-bracket names are notation. Never hardcode another machine's home path.

`GETTY_HOME` is one override for a whole environment (and for tests, which always set it), not a per-consumer setting. Two consumers seeing different `GETTY_HOME` values get separate stores and locks: safe, but not shared. `GETTY_BUN_MIRROR` changes only the download base URL; the pinned SHA256 still decides.

For a home shared between incompatible execution contexts (network homes, synchronized profiles), set `GETTY_HOME` to a local root per context first.

## Select a real release artifact

The target comes from the reviewed version table, never from a plausible asset name. MVP targets: `linux-x64`, `linux-x64-baseline` (no AVX2), `linux-aarch64`, `windows-x64`, `windows-x64-baseline`. musl, `windows-aarch64` and macOS come later as explicit table entries; until then the starter detects them and fails with a message naming the target.

Detection as built (getty-bun `bootstrap/README.md`):

- Linux: `uname -m` (`x86_64` -> `x64`, `aarch64`/`arm64` -> `aarch64`); `x64` without `avx2` in the first `flags` line of `/proc/cpuinfo` -> `x64-baseline`; unreadable -> baseline. A musl loader without the glibc one fails as `linux-<arch>-musl`. No fallback when an x64 Bun dies with SIGILL (card `k12`).
- Windows: `PROCESSOR_ARCHITEW6432`, else `PROCESSOR_ARCHITECTURE` (`AMD64` -> `x64`; `ARM64` fails as `windows-aarch64`). AVX2 via `IsProcessorFeaturePresent(40)` through `Add-Type`, only when neither x64 slot exists: before an install, and in `status`, which then reports `missing` with the detected target; where `Add-Type` cannot load (Constrained Language Mode, no compiler) -> `x64-baseline`. The `Add-Type` check and the ARM64 failure (simulated through `PROCESSOR_ARCHITECTURE`): executed, getty-bun CI 45572032454. An x64 probe dying with `STATUS_ILLEGAL_INSTRUCTION` publishes nothing, and the starter installs `windows-x64-baseline` under that target's lock (source-checked, `getty-bun.ps1:583-600`; a local run with a fixture probe, not in CI; a real CPU without AVX2: not checked).
- Windows fast path: the first existing slot of `windows-x64`, then `windows-x64-baseline`, without CPU detection; a mismatching `windows-x64` slot fails closed and is never skipped (source-checked, `getty-bun.ps1:207-214`; a local run with pwsh 7 on Linux, not in CI). A profile that moves to a CPU without AVX2 keeps its x64 slot, and Bun dies there (not checked); removing that slot lets the next call install the baseline.

When adding a version, inspect the **chosen exact release**: OS, architecture of the process that executes Bun, libc/ABI, minimum OS, CPU instruction requirements and baseline variants, archive layout, expected member. Use official [Bun installation documentation](https://bun.sh/docs/installation) and [release assets](https://github.com/oven-sh/bun/releases). Treat emulation as an explicit tested target; do not reuse Windows executables in WSL or assume host runtimes exist in containers.

## Keep three paths separate

1. **Runtime executable:** `<GETTY_HOME>` plus the pin block.
2. **Consumer root:** derived by the starter from its own path, never from the working directory. `<entry>` is relative to it. This skill writes it `<consumer-root>`; in a hook command the host's placeholder stands for it: `${CLAUDE_PLUGIN_ROOT}` (Claude Code), `${PLUGIN_ROOT}` (Codex). Hosts start hooks in the session's working directory (Codex: documented), so the working directory says nothing about the plugin.
3. **User project:** explicit application input or the chosen working directory.

The bundled entry needs no module resolution at runtime. Pass project paths as arguments where supported.

## Quoting and process start

Prefer executable-plus-argument arrays. Quote for the actual shell when shell syntax is unavoidable; POSIX escaping is not PowerShell escaping. Test spaces, non-ASCII characters and separators in `GETTY_HOME` and in the consumer root (an old briefing bug was a non-ASCII home).

Windows rules for `getty-bun.ps1`, as built (getty-bun `bootstrap/README.md`, "Windows starter"):

- Invocation: `powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "<consumer-root>\bootstrap\getty-bun.ps1" run <entry> [args]`. Entry arguments never begin with `-`: `-File` hands them to PowerShell's parameter binding ([contract.md](contract.md)). Cost: measured by windows-developer, a PowerShell start takes about 720 ms on a desktop; executed in getty-bun CI, the starter adds 348–522 ms over Bun alone, 171–294 ms of it the PowerShell start (medians, 5.1 and 7), a lower bound for desktops ([claude-code.md](claude-code.md), table). An execution policy set by Group Policy takes precedence over `-ExecutionPolicy Bypass` (documented for 5.1 and 7, [about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies)); if that policy turns scripts off or is `AllSigned`, the unsigned starter cannot run (derived, not measured).
- Run Bun through `System.Diagnostics.Process` (`UseShellExecute = $false`, `CreateNoWindow`, stdin and stdout redirected, stderr inherited) and copy stdin and stdout as raw bytes asynchronously; close the child's stdin at end of input; end once Bun has ended, even while the host keeps stdin open; exit with the child's `ExitCode` (executed, scenarios 8 and 8b on 5.1 and 7). **Never run Bun with `&`**: measured by windows-developer (probe y4), Windows PowerShell 5.1 did not pass the end of stdin to a native program; the hook hung until its timeout and the process stayed behind. PowerShell's pipeline also re-encodes text. The cost of `CreateNoWindow`: Ctrl+C in the host's console does not reach Bun, and Bun survives a kill of `powershell.exe` (not checked; card `k13`).
- 5.1 has only `ProcessStartInfo.Arguments`: quote every argument by the `CommandLineToArgvW` rules (spaces, embedded quotes, trailing backslashes, non-ASCII: executed, scenario 8).
- Language level 5.1: no `??`, `?.`, ternary, `&&`/`||` between commands, `$IsWindows`, `ProcessStartInfo.ArgumentList`. Keep the file pure ASCII with LF; 5.1 reads a file without BOM in the ANSI code page (checked by getty-bun's static CI job).
- Measured by windows-developer: Claude Code sends UTF-8 JSON on stdin with backslash paths inside and passes stdout through unchanged.

Git Bash, MSYS2 and Cygwin forwarding, as built: `getty-bun.sh` hands every call to the `getty-bun.ps1` next to it, preferring Windows PowerShell 5.1 by its fixed path under `$SYSTEMROOT`, converts a POSIX `GETTY_HOME` with `cygpath -w`, and sets `MSYS_NO_PATHCONV=1` and `MSYS2_ARG_CONV_EXCL='*'`, which stay in the entry's environment. Shared slot and lock: executed, scenario 11; the converted `GETTY_HOME` and unchanged arguments: executed, getty-bun CI 45589361806; the 5.1 preference: source-checked. Exit codes 0, 1, 2, 7 and 42 come back unchanged (executed, getty-bun CI 45579886904); a crash's NTSTATUS maps differently per path (source-checked; `bootstrap/README.md`, "Limit: exit codes through Git Bash").

Hint for hosts and tests, not a requirement: give the starter its input on a pipe. Under Git Bash, a native PowerShell blocks reading an inherited NUL handle (executed, getty-bun CI 45589361806), so for a stdin that is a character device but no terminal (`/dev/null`) the forwarding starts PowerShell on an empty pipe instead of `exec` (executed, CI 45597390051). On that path a signal to the shell ends only the shell (card `k13`). Hook input on a pipe keeps the `exec` path; that hosts use a pipe is inferred for Claude Code (windows-developer recorded the JSON and end of input, not the handle type) and not measured for Codex.

Repository hygiene for consumers that ship starters: `.gitattributes` with `* text=auto eol=lf`, plus `*.exe binary` if the consumer ships a Windows executable (the shim option in [claude-code.md](claude-code.md); windows-developer `docs/starter-konvention.md`); no checked-in symlinks (measured by windows-developer: they become text files without developer mode).

## Host lifecycle

Claude Code uses versioned plugin cache locations; its plugin data has a separate lifecycle and may be removed on uninstall. Keep the store outside both. Source: [Claude Code loading](https://code.claude.com/docs/en/plugins/loading). Codex exposes the installed plugin root as `PLUGIN_ROOT` and, for compatibility, `CLAUDE_PLUGIN_ROOT` to plugin hook commands (documented, not executed) and substitutes `${PLUGIN_ROOT}` textually into the command string before the shell runs it (source-checked, openai/codex `3f65e9f`, not executed); quote it ([codex.md](codex.md)).

A moved or updated plugin needs nothing beyond its committed starters and bundle: the starter derives the consumer root afresh on every call, and the shared runtime remains valid.
