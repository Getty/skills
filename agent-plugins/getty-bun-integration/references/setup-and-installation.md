# Installation and setup

Status: Getty contract proposal v0.2. This describes what the planned starters do and what a consumer's setup skill is for; neither the starters nor an installer exist yet. Follow [contract.md](contract.md), [paths-platforms.md](paths-platforms.md), and [installation-locking.md](installation-locking.md).

## The starter installs on demand

Neither Codex nor Claude Code has an install hook (ADR 0002; not re-checked here). So every starter call that runs code (`run`) or asks for readiness (`ensure`) first ensures the pinned Bun:

- Present and matching: fast local check, then run.
- Missing: install under the OS lock, then run.
- After a plugin install or update, the first hook (normally `SessionStart`) therefore installs. Concurrent hooks block on the same lock, bounded by `GETTY_BUN_LOCK_WAIT` (default 300 s), re-check the slot, and then either run the entry, whose exit code passes through unchanged, or fail with one stderr line and exit 1. The starter never exits 2 for its own failures.
- The first hook after an update can take one download. Set each hook's `timeout` above the lock wait plus one download: a waiter that acquires the lock after a crashed holder downloads itself. Codex and Claude Code document 600 s for most command hooks and seconds for `SessionEnd` ([codex.md](codex.md), [claude-code.md](claude-code.md)).
- `@getty/bun-runtime` never installs, downloads, or edits lockfiles. A consumer writes no installer code of its own.

ADR 0002 makes installing or updating the plugin the point at which Bun is installed. In practice that waits for the host's hook trust, because a hook that is not yet trusted does not run (Codex: documented); this is our inference, not part of the ADR. The starter writes only under `<GETTY_HOME>`; it never edits shell startup files, PATH, or system packages, and never uses the official Bun install script.

## Bootstrap prerequisites

The starter runs before Bun, Node or Python exist. Planned prerequisites (skill `getty-bun-bootstrap` in getty-bun):

| Starter | Needs |
| --- | --- |
| `getty-bun.sh` (Linux; macOS in phase 4) | POSIX `sh`, `curl` or `wget`, `unzip`, `sha256sum` or `shasum -a 256`, `flock` |
| `getty-bun.ps1` (Windows) | Windows PowerShell 5.1 or PowerShell 7; .NET for download, hash, zip, lock |

A missing prerequisite or an unsupported target fails with a message that names it. Under Git Bash, MSYS or Cygwin, `getty-bun.sh` forwards to `getty-bun.ps1` and does nothing itself.

**One real coordinating process** owns the mutex across download, validation, and publication: the starter. Several independent shell calls with a PID in `.installing` are not one protected installation; a Markdown procedure cannot replace the starter.

## What one install does

The starter, not the agent, performs these steps:

1. Take version and per-target SHA256 from the rendered pin block; nothing else selects a version.
2. Resolve `<GETTY_HOME>` and detect the target; failed CPU-feature detection selects the baseline build; an unsupported target fails.
3. Fast path: receipt present, version and target match, executable present. A mismatching published slot fails closed and is never overwritten.
4. Acquire the permanent version/target mutex, bounded. Re-read the slot after acquisition; another installer may have completed.
5. Create a unique stage on the slots' filesystem and publish `.installing` under the mutex.
6. Download `bun-<target>.zip` from the official release or `GETTY_BUN_MIRROR`; verify the archive SHA256 from the pin block before unpacking; reject an archive with an unexpected or extra member; extract the expected member by name.
7. Check executable type, run a bounded `bun --version` probe, compare it with the pin, write the receipt.
8. Publish the complete stage to an **absent** final slot with one atomic rename while holding the mutex. A cross-filesystem copy or move is not such a primitive.
9. Clear this attempt's status, clean the stage, release the mutex. Keep the permanent lock file.

A crash after publication but before marker cleanup is handled by the next owner validating the slot and cleaning orphan status, not by reinstalling. A failed attempt leaves no partial slot.

## The setup skill: repair and diagnosis

Package a setup skill with the consumer ([setup-skill-template.md](../assets/setup-skill-template.md)). It is no longer the install path; it serves the cases where the automatic install failed or the user asks why the plugin is idle:

- Run the committed starter's `status` and report pin, target, slot and state. `status` is not specified to install.
- Run `ensure` to install explicitly, for example after a lock-wait timeout or a network failure, and report its stderr line.
- A slot that fails closed: report its path. The MVP has no repair command; removing a published slot needs quiescence across every consumer using it and the user's decision. Do not delete it as an incidental fix.
- Windows: an execution policy set by Group Policy takes precedence over `-ExecutionPolicy Bypass` (documented, [about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies)); if it turns scripts off or is `AllSigned`, the starter cannot run, and the setup skill must say so. Application control (AppLocker, WDAC) or antivirus can block it as well (not checked).
- Check that `gettyBun.bunVersion` equals the pin in the committed starters; a mismatch is a release bug, not something to fix on the user machine.

Host onboarding surfaces (Codex `onboardingSkill`) may point to this skill; a context hint may mention it. Neither installs anything.

## Official installer limitations

Official Bun installers accept a release and `BUN_INSTALL`. The Unix installer may edit shell startup files; the inspected Windows script exposes `-NoPathUpdate`, `-NoRegisterInstallation`, and `-NoCompletions`. Sources: [Unix installer](https://bun.com/install), [Windows installer](https://bun.sh/install.ps1). The starters do not use them: they download the reviewed archive, verify it against the pin, and extract it themselves. Running an unpinned mutable installer script is not verification of the resulting runtime.

## Authorization

Honor existing authorization for repair; do not repeatedly request the same permission. Host hook review stays a real boundary: prepare the files, then let the user complete the review; never bypass it. Do not modify global shell configuration, replace system Bun, or add system packages as a side effect of this private-store design.
