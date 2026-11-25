# Paths and platform selection

Status: Getty contract proposal v0.2. Use [contract.md](contract.md) for ownership and canonical fields. Windows facts marked "measured by windows-developer" come from that hub (`docs/hook-start-windows.md`, `docs/starter-konvention.md`, `docs/umgebung.md`; Claude Code 2.1.287, Windows 11 25H2, PowerShell 5.1.26100). Everything else on Windows is source-checked or planned until a Windows run shows it.

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

Planned detection (skills `getty-bun-bootstrap`, `getty-bun-windows`):

- Linux: `uname -m` (`x86_64` -> `x64`, `aarch64`/`arm64` -> `aarch64`); `x64` without `avx2` in `/proc/cpuinfo` -> `x64-baseline`; unreadable -> baseline.
- Windows: `PROCESSOR_ARCHITECTURE` (`AMD64` -> `x64`; check `PROCESSOR_ARCHITEW6432` for a 32-bit host process); AVX2 via `IsProcessorFeaturePresent(40)` only during install; detection that fails (for example Constrained Language Mode) -> `x64-baseline`.

When adding a version, inspect the **chosen exact release**: OS, architecture of the process that executes Bun, libc/ABI, minimum OS, CPU instruction requirements and baseline variants, archive layout, expected member. Use official [Bun installation documentation](https://bun.sh/docs/installation) and [release assets](https://github.com/oven-sh/bun/releases). Treat emulation as an explicit tested target; do not reuse Windows executables in WSL or assume host runtimes exist in containers.

## Keep three paths separate

1. **Runtime executable:** `<GETTY_HOME>` plus the pin block.
2. **Consumer root:** derived by the starter from its own path, never from the working directory. `<entry>` is relative to it. This skill writes it `<consumer-root>`; in a hook command the host's placeholder stands for it: `${CLAUDE_PLUGIN_ROOT}` (Claude Code), `${PLUGIN_ROOT}` (Codex). Hosts start hooks in the session's working directory (Codex: documented), so the working directory says nothing about the plugin.
3. **User project:** explicit application input or the chosen working directory.

The bundled entry needs no module resolution at runtime. Pass project paths as arguments where supported.

## Quoting and process start

Prefer executable-plus-argument arrays. Quote for the actual shell when shell syntax is unavoidable; POSIX escaping is not PowerShell escaping. Test spaces, non-ASCII characters and separators in `GETTY_HOME` and in the consumer root (an old briefing bug was a non-ASCII home).

Windows rules for `getty-bun.ps1` (planned; from skill `getty-bun-windows`):

- Invocation: `powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "<consumer-root>\<starter-dir>\getty-bun.ps1" run <entry> [args]`. Measured by windows-developer: a PowerShell start costs about 720 ms. An execution policy set by Group Policy takes precedence over `-ExecutionPolicy Bypass` (documented for 5.1 and 7, [about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies)); if that policy turns scripts off or is `AllSigned`, the unsigned starter cannot run (derived, not measured).
- Run Bun through `System.Diagnostics.Process` (`UseShellExecute = $false`, stdin and stdout redirected, stderr inherited) and copy stdin and stdout as raw bytes asynchronously; close the child's stdin at end of input; exit with the child's `ExitCode`. **Never run Bun with `&`**: measured by windows-developer (probe y4), Windows PowerShell 5.1 did not pass the end of stdin to a native program; the hook hung until its timeout and the process stayed behind. PowerShell's pipeline also re-encodes text.
- 5.1 has only `ProcessStartInfo.Arguments`: quote every argument by the `CommandLineToArgvW` rules (spaces, embedded quotes, trailing backslashes).
- Language level 5.1: no `??`, `?.`, ternary, `&&`/`||` between commands, `$IsWindows`, `ProcessStartInfo.ArgumentList`. Keep the file pure ASCII; 5.1 reads a file without BOM in the ANSI code page.
- Measured by windows-developer: Claude Code sends UTF-8 JSON on stdin with backslash paths inside and passes stdout through unchanged.

Repository hygiene for consumers that ship starters: `.gitattributes` with `* text=auto eol=lf`, plus `*.exe binary` if the consumer ships a Windows executable (the shim option in [claude-code.md](claude-code.md); windows-developer `docs/starter-konvention.md`); no checked-in symlinks (measured by windows-developer: they become text files without developer mode).

## Host lifecycle

Claude Code uses versioned plugin cache locations; its plugin data has a separate lifecycle and may be removed on uninstall. Keep the store outside both. Source: [Claude Code loading](https://code.claude.com/docs/en/plugins/loading). Codex exposes the installed plugin root as `PLUGIN_ROOT` and, for compatibility, `CLAUDE_PLUGIN_ROOT` to plugin hook commands (documented, not executed) and substitutes `${PLUGIN_ROOT}` textually into the command string before the shell runs it (source-checked, openai/codex `3f65e9f`, not executed); quote it ([codex.md](codex.md)).

A moved or updated plugin needs nothing beyond its committed starters and bundle: the starter derives the consumer root afresh on every call, and the shared runtime remains valid.
