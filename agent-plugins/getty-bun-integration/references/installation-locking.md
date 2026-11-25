# Installation locking and recovery

Status: Getty contract proposal v0.2. The starters `getty-bun.sh` and `getty-bun.ps1` (agent-bun-runtime `bootstrap/`, phase 1) implement these requirements on Linux and Windows; consumers do not write locking code. Use this reference to review or extend the starters in agent-bun-runtime. The layout, metadata, and recovery rules are Getty's design; linked OS documentation supports the underlying primitives. "Executed, scenario N" means agent-bun-runtime's suite in CI 45603412444 ([contract.md](contract.md), status); macOS, WSL, network filesystems and real desktops are not checked.

## Separate the mutex from its status

Coordinate each exact version and artifact target through a stable control directory outside the published runtime slot (`<store>` is `<GETTY_HOME>/runtimes`):

```text
<store>/bun/.locks/<version>/<target>/.install.lock
<store>/bun/.locks/<version>/<target>/.installing
```

Use `.install.lock` as the permanent backing file for an OS-backed exclusive mutex. Use `.installing` as readable status. Its existence, absence, age, or recorded PID never grants ownership. All plugins targeting the same slot must use the same canonical path, protocol, and compatible locking mechanism.

Never unlink, replace, rename, or garbage-collect the mutex file or its containing control directory during concurrent operation. Otherwise, an existing waiter can retain the old file while a new contender locks a replacement. This is a design consequence of the documented [Unix open-file-description lock semantics](https://man7.org/linux/man-pages/man2/flock.2.html).

## Bootstrap and backend requirements

Acquire locks, inspect state, and write metadata using available OS bootstrap tools. Neither Bun nor Node may be required before the first Bun installation. Do not compile or download a custom lock helper as an implicit prerequisite.

Capability-probe the selected backend and its required mode before mutating installation state. Backends:

| Platform | Backend and required behavior |
| --- | --- |
| Linux (MVP, built) | `getty-bun.sh` with util-linux [`flock`](https://man7.org/linux/man-pages/man1/flock.1.html) (`-x -w <wait> -E 3`) on descriptor 9, which only the install's command group has open; the download, `unzip` and the `bun --version` probe run with `9>&-`, and the descriptor is closed before Bun starts. Require exclusive BSD-style locking; do not silently select `--fcntl`, whose locks are independent of BSD-style locks. Executed (scenarios 2, 2b, 3). |
| Windows (MVP, built) | `getty-bun.ps1` with [`.NET File.Open`](https://learn.microsoft.com/en-us/dotnet/api/system.io.file.open?view=netframework-4.8.1) and `OpenOrCreate`, `ReadWrite`, [`FileShare.None`](https://learn.microsoft.com/en-us/dotnet/api/system.io.fileshare?view=netframework-4.7.2), kept in a variable for the whole critical section, disposed right after publishing and in a `finally` around that section, before Bun starts. Waiting is a retry every 200 ms until the deadline; a sharing or lock violation means held, any other error fails. Not a named mutex: `Local\` is per logon session, and the lock must belong to the store path. Runs on Windows PowerShell 5.1 and PowerShell 7. Executed (scenarios 2, 2b, 3). |
| Git Bash, MSYS, Cygwin (built) | `getty-bun.sh` forwards to `getty-bun.ps1` (paths through `cygpath -w`) and does no locking or download of its own, so a slot has exactly one lock implementation. Executed (scenario 11: same slot and lock). |
| WSL | Linux, with its own store under the WSL home; never a Windows `bun.exe` or the Windows lock. Not checked. |
| macOS (phase 4, later) | Candidate: [`lockf(1)`](https://raw.githubusercontent.com/apple-oss-distributions/shell_cmds/main/lockf/lockf.1) in file-descriptor mode on a descriptor the starter shell retains for the critical section. Apple's documentation demonstrates this mode and implies `-k`, keeping the backing file. Check availability on the actual system. |

Distinguish contention from permission errors, unsupported operations, and other I/O failures. A timeout reports busy; it does not authorize breaking a lock. If no supported backend exists, stop before installation. Do not substitute PID-based unlinking or an independently chosen directory lock.

## Bounded wait

Waiters try the mutex for at most `GETTY_BUN_LOCK_WAIT` seconds (default 300); after acquiring it they re-check the slot before installing. A waiter whose wait runs out fails with one stderr line and exit 1, naming `.installing` if it exists, and leaves no partial slot (executed, scenario 3); the starter never exits 2 for its own failures. The wait must stay below the host hook timeout (Codex and Claude Code document 600 s for most command hooks), and the consumer sets hook timeouts above the lock wait plus one download: a waiter that acquires the lock after a crashed holder downloads itself. Concurrent first hooks after a plugin install or update are the normal case: exactly one downloads and publishes, the others wait and reuse.

## Record the installation owner

Phase 1 fixed the record (agent-bun-runtime `bootstrap/README.md`, "Install lock and `.installing`"): the eight fields below, written after acquiring the mutex as a complete temporary file renamed in the same directory. `installId` is the staging directory's name. `processStartToken` and `environmentId` are `null` where the OS does not provide them; on Windows they are `start-filetime:<n>` and `<machine>/windows/<SID>`, and `processName` is `powershell` or `pwsh`. Executed: the record during an install and a timed-out waiter naming it (interface tests). The POSIX form:

```json
{
  "schemaVersion": 1,
  "pid": 12345,
  "processName": "sh",
  "processStartToken": "boot:<boot id>/start-ticks:<n>",
  "installId": "<staging directory name>",
  "environmentId": "<hostname>/linux/uid-<uid>",
  "requestedVersion": "1.4.5",
  "target": "linux-x64-baseline"
}
```

Record the actual coordinator's PID and executable/process name, plus a unique `installId` for this attempt. A wrapper's PID or a download subprocess's name is insufficient. Represent unavailable `processStartToken` as `null`; do not invent precision.

Interpret start identity within its host, boot, and execution environment. Include the boot identity in a boot-relative start token; keep `environmentId` stable across ordinary reboots of the same configured local environment. A reboot alone must not turn a compatible store into a foreign store. Linux exposes process start information through [`/proc`](https://www.kernel.org/doc/html/latest/filesystems/proc.html); Windows exposes [`Process.StartTime`](https://learn.microsoft.com/dotnet/api/system.diagnostics.process.starttime). A name is descriptive, and a PID can be reused. A differing start token identifies a different process; it still does not authorize deleting a held lock. Missing, inaccessible, or coarse identity information means unknown. Never kill a process automatically from this record.

## Acquisition, publication, and cleanup

1. Acquire the exclusive mutex for the requested version and target.
2. Re-read the marker and runtime state after acquisition. Another installer may have completed while this process waited.
3. Validate an existing published runtime; reuse it if valid. Reconcile orphan metadata under the mutex.
4. Create a unique attempt directory and publish the current `.installing` record. Never reuse another attempt's working directory.
5. Download, verify, and publish according to [contract.md](contract.md), retaining protection through all shared-state mutations.
6. Remove this attempt's marker while still holding the mutex, then release the lock. Keep `.install.lock` permanently. **Close the lock descriptor (Windows: dispose the stream) before starting Bun.** A descriptor without close-on-exec survives the `exec` ([execve(2)](https://man7.org/linux/man-pages/man2/execve.2.html)), and a `flock` lock belongs to the open file description ([flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html)); otherwise Bun holds the install lock for the entry's whole run, and waiters run into `GETTY_BUN_LOCK_WAIT`. Our rule, derived from those semantics; executed (scenario 2b on every leg).

Normal cleanup holds the mutex: both starters remove `.installing` before they release the lock, on success and on every failure (`bootstrap/README.md`). A cleanup that runs after release (a delayed handler, which the starters do not have) must reacquire, recheck that `installId` still matches, and only then delete; otherwise it could delete a newer owner's marker. A token check without serialization remains a check-then-delete race.

## Recovery and process lifetime

Successful mutex acquisition authorizes recovery within a known compatible store. No conforming installer still owns that critical section. An empty, truncated, or malformed marker may therefore be recovered under the mutex, including a crash during initialization. While the mutex is held elsewhere, malformed or absent metadata only limits diagnostics.

Two recovery contenders must acquire the same mutex and re-read state; only the winner repairs it. After a crash following successful publication, validate the runtime and clean orphan status instead of reinstalling automatically.

As built (`bootstrap/README.md`; signal handling is not in the scenario suite): a holder stopped by HUP, INT or TERM removes its `.installing` and its stage. One killed outright (SIGKILL, power loss) leaves both; the next holder overwrites `.installing`, and the stale `runtimes/bun/.staging/<id>/` stays, since the MVP has no garbage collection. A stage is safe to delete by hand while no install runs; no published slot refers to it.

Keep every shared-state writer protected for its entire lifetime. Do not assume a supervising lock wrapper survives its child. Either retain lock protection in surviving writers, or restrict workers to unique private staging paths with no publication authority. On Windows, publish inside the PowerShell process retaining the stream, with `[System.IO.Directory]::Move`; antivirus can hold a freshly written `.exe`, so retry moves and deletes on a sharing violation, bounded (about 10 s), then fail (built; the retry is not checked). Never fall back to copying into a slot. Keep staging ids short (MAX_PATH). Do not reuse or blindly delete a previous stage if an orphan worker could still write there.

Candidate rules beyond the phase 1 gate, not built: stop automatic takeover for an unsupported schema, an inconsistent requested version/target, or a foreign `environmentId` until compatible coordination is established. The built starters do not read a previous `.installing` before they overwrite it; the mutex alone serializes them. Do not adopt unknown legacy writers merely because their PID appears absent. Restrict the prototype to a local store with validated locking semantics; network shares, synchronized homes, WSL/native sharing, and cross-container access require separate verification. The [`flock` documentation](https://man7.org/linux/man-pages/man1/flock.1.html) explicitly describes filesystem-dependent limitations. Metadata and elapsed time cannot compensate for an unavailable or incompatible mutex.
