# Installation and setup

Status: Getty contract proposal v0.2. This describes what the starters do and what a consumer's setup skill is for. The starters are built in agent-bun-runtime (phase 1, tested in its CI); the consumer side (template, setup skill) is not. Follow [contract.md](contract.md), [paths-platforms.md](paths-platforms.md), and [installation-locking.md](installation-locking.md).

## The starter installs on demand

Neither Codex nor Claude Code has an install hook (ADR 0002; not re-checked here). So every starter call that runs code (`run`) or asks for readiness (`ensure`) first ensures the pinned Bun:

- Present and matching: fast local check, then run.
- Missing: install under the OS lock, then run.
- After a plugin install or update, the first hook (normally `SessionStart`) therefore installs. Concurrent hooks block on the same lock, bounded by `GETTY_BUN_LOCK_WAIT` (default 300 s), re-check the slot, and then either run the entry, whose exit code passes through unchanged, or fail with one stderr line and exit 1. The starter never exits 2 for its own failures (ADR 0007). Executed, scenarios 2 and 3.
- The first hook after an update can take one download. Set each hook's `timeout` above the lock wait plus one download: a waiter that acquires the lock after a crashed holder downloads itself (ADR 0007, superseding 0002's "above the lock wait"). Codex and Claude Code document 600 s for most command hooks and seconds for `SessionEnd` ([codex.md](codex.md), [claude-code.md](claude-code.md)).
- `@getty/agent-bun-runtime` never installs, downloads, or edits lockfiles. A consumer writes no installer code of its own.

ADR 0002 makes installing or updating the plugin the point at which Bun is installed. In practice that waits for the host's hook trust, because a hook that is not yet trusted does not run (Codex: documented); this is our inference, not part of the ADR. The starter writes only under `<GETTY_HOME>`; it never edits shell startup files, PATH, or system packages, and never uses the official Bun install script.

## Bootstrap prerequisites

The starter runs before Bun, Node or Python exist. Prerequisites as built (agent-bun-runtime `bootstrap/README.md`, "POSIX starter: tools", "Windows starter"):

| Starter | Needs |
| --- | --- |
| `getty-bun.sh` (Linux; macOS in phase 4) | Fast path: POSIX `sh` builtins and `uname`. Install also: util-linux `flock` (`-w`, `-E`), Info-ZIP `unzip` (`-Z1`; not BusyBox's), `curl` or GNU Wget 1.16+ (not BusyBox's), `sha256sum` or `shasum -a 256`, `mktemp -d` and coreutils. Tested with `dash` and `busybox sh`. |
| `getty-bun.ps1` (Windows) | Windows PowerShell 5.1 or PowerShell 7; .NET for download, hash, zip, lock; `Add-Type` for AVX2 detection when no x64 slot exists, at install and in `status` (without it: baseline) |
| Git Bash, MSYS, Cygwin | `cygpath` and a Windows PowerShell; `getty-bun.sh` forwards to `getty-bun.ps1` and does nothing itself |

An unsupported target fails with one line naming it (executed, interface tests). A missing tool fails with one line naming it, before anything is written (`bootstrap/README.md`; not in the suite). Neither fetcher reads `~/.curlrc` or a wgetrc; a proxy comes from `https_proxy`/`no_proxy` (proxies not checked).

**One real coordinating process** owns the mutex across download, validation, and publication: the starter. Several independent shell calls with a PID in `.installing` are not one protected installation; a Markdown procedure cannot replace the starter.

## What one install does

The starter, not the agent, performs these steps (built; executed, scenarios 1–6):

1. Take version, archive, SHA256 and member from the rendered pin block; nothing else selects a version.
2. Resolve `<GETTY_HOME>` and detect the target; failed CPU-feature detection selects the baseline build; an unsupported target fails. `getty-bun.ps1` checks the CPU only when no x64 slot exists ([paths-platforms.md](paths-platforms.md)).
3. Fast path: the receipt's first three lines name the pinned version and target, and the executable is a non-empty regular file. A mismatching published slot fails closed and is never overwritten.
4. Acquire the permanent version/target mutex, bounded. Re-read the slot after acquisition; another installer may have completed.
5. Create a unique stage on the slots' filesystem and publish `.installing` under the mutex.
6. Download `<base>/bun-v<version>/<archive>` from the official release or `GETTY_BUN_MIRROR`; verify the archive SHA256 from the pin block before unpacking; reject an archive with an unexpected or extra member; extract the expected member by name.
7. Run `bun --version` and compare it with the pin (Windows: killed after 60 s, retried once after a failure, illegal-instruction fallback to the baseline; POSIX: no time bound), then write the receipt.
8. Publish the complete stage to an **absent** final slot with one atomic rename while holding the mutex. A cross-filesystem copy or move is not such a primitive.
9. Clear this attempt's status before releasing the mutex, and clean the stage. Keep the permanent lock file. `getty-bun.ps1` then runs `bun --version` on the published `bun.exe` once more and exits 1 if it does not run, leaving the slot published; `getty-bun.sh` does not (open difference, card `agent-bun-runtime k19`, [contract.md](contract.md)).

A crash after publication but before marker cleanup is handled by the next owner validating the slot and cleaning orphan status, not by reinstalling. A failed attempt leaves no partial slot.

## The setup skill: repair and diagnosis

Package a setup skill with the consumer ([setup-skill-template.md](../assets/setup-skill-template.md)). It is no longer the install path; it serves the cases where the automatic install failed or the user asks why the plugin is idle:

- Run the committed starter's `status` and report pin, target, slot and state (`ready`, `missing` or `mismatch`). `status` never installs.
- Run `ensure` to install explicitly, for example after a lock-wait timeout or a network failure, and report its stderr line.
- A slot that fails closed (`mismatch`): report its path. The MVP has no repair command; removing a published slot needs quiescence across every consumer using it and the user's decision. Do not delete it as an incidental fix.
- A `ready` slot whose `run` ends without a `getty-bun: ` line (exit 126, a crash) may hold a damaged executable, which the fast path does not detect; report the slot path ([contract.md](contract.md), fast path).
- Windows: an execution policy set by Group Policy takes precedence over `-ExecutionPolicy Bypass` (documented, [about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies)); if it turns scripts off or is `AllSigned`, the starter cannot run, and the setup skill must say so. Application control (AppLocker, WDAC) or antivirus can block it as well; under Git Bash a blocked `powershell.exe` shows as exit 126 with the shell's own line, not a `getty-bun: ` line (`bootstrap/README.md`; not checked).
- Check that `gettyBun.bunVersion` equals the pin in the committed starters; a mismatch is a release bug, not something to fix on the user machine.

Host onboarding surfaces (Codex `onboardingSkill`) may point to this skill; a context hint may mention it. Neither installs anything.

## Official installer limitations

Official Bun installers accept a release and `BUN_INSTALL`. The Unix installer may edit shell startup files; the inspected Windows script exposes `-NoPathUpdate`, `-NoRegisterInstallation`, and `-NoCompletions`. Sources: [Unix installer](https://bun.com/install), [Windows installer](https://bun.sh/install.ps1). The starters do not use them: they download the reviewed archive, verify it against the pin, and extract it themselves. Running an unpinned mutable installer script is not verification of the resulting runtime.

## Authorization

Honor existing authorization for repair; do not repeatedly request the same permission. Host hook review stays a real boundary: prepare the files, then let the user complete the review; never bypass it. Do not modify global shell configuration, replace system Bun, or add system packages as a side effect of this private-store design.
