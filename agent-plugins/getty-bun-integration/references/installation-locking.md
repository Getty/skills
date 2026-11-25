# Installation locking and recovery

Status: Getty contract proposal v0.2. The planned starters `getty-bun.sh` and `getty-bun.ps1` implement these requirements; consumers do not write locking code. Use this reference to build or review the starters in getty-bun. The layout, metadata, and recovery rules are Getty's design; linked OS documentation supports the underlying primitives. Neither starter exists yet, so no installer has been run on any platform.

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

Capability-probe the selected backend and its required mode before mutating installation state. Planned backends; none is implemented or validated on a platform yet:

| Platform | Backend and required behavior |
| --- | --- |
| Linux (MVP) | `getty-bun.sh` with util-linux [`flock`](https://man7.org/linux/man-pages/man1/flock.1.html) on a descriptor the starter shell retains for the critical section and closes before it starts Bun. Require exclusive BSD-style locking; do not silently select `--fcntl`, whose locks are independent of BSD-style locks. |
| Windows (MVP) | `getty-bun.ps1` with [`.NET File.Open`](https://learn.microsoft.com/en-us/dotnet/api/system.io.file.open?view=netframework-4.8.1) and `OpenOrCreate`, `ReadWrite`, [`FileShare.None`](https://learn.microsoft.com/en-us/dotnet/api/system.io.fileshare?view=netframework-4.7.2), kept in a variable for the whole critical section and disposed in a `finally` around that section, before Bun starts. Waiting is a retry loop with a short sleep until the deadline. Not a named mutex: `Local\` is per logon session, and the lock must belong to the store path. Must run on Windows PowerShell 5.1 and PowerShell 7. |
| Git Bash, MSYS, Cygwin | `getty-bun.sh` forwards to `getty-bun.ps1` (paths through `cygpath -w`) and does no locking or download of its own, so a slot has exactly one lock implementation. |
| WSL | Linux, with its own store under the WSL home; never a Windows `bun.exe` or the Windows lock. |
| macOS (phase 4, later) | Candidate: [`lockf(1)`](https://raw.githubusercontent.com/apple-oss-distributions/shell_cmds/main/lockf/lockf.1) in file-descriptor mode on a descriptor the starter shell retains for the critical section. Apple's documentation demonstrates this mode and implies `-k`, keeping the backing file. Check availability on the actual system. |

Distinguish contention from permission errors, unsupported operations, and other I/O failures. A timeout reports busy; it does not authorize breaking a lock. If no supported backend exists, stop before installation. Do not substitute PID-based unlinking or an independently chosen directory lock.

## Bounded wait

Waiters try the mutex for at most `GETTY_BUN_LOCK_WAIT` seconds (default 300); after acquiring it they re-check the slot before installing. A waiter whose wait runs out fails with one stderr line and exit 1, leaving no partial slot; the starter never exits 2 for its own failures. The wait must stay below the host hook timeout (Codex and Claude Code document 600 s for most command hooks), and the consumer sets hook timeouts above the lock wait plus one download: a waiter that acquires the lock after a crashed holder downloads itself. Concurrent first hooks after a plugin install or update are the normal case: exactly one downloads and publishes, the others wait and reuse.

## Record the installation owner

Fields beyond `requestedVersion` and `target` are proposed diagnostics: skill `getty-bun-bootstrap` does not require them, and phase 1 decides which stay.

Write `.installing` only after acquiring the mutex. Prefer a complete temporary record followed by same-directory rename. The following values are illustrative, not a recommended Bun version or real process identity:

```json
{
  "schemaVersion": 1,
  "pid": 12345,
  "processName": "bash",
  "processStartToken": "example-linux-boot-a/start-ticks:424242",
  "installId": "example-attempt-7d65bb44",
  "environmentId": "example-host-a/native-linux/user-1000",
  "requestedVersion": "1.2.3",
  "target": "linux-x64"
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
6. Remove this attempt's marker while still holding the mutex, then release the lock. Keep `.install.lock` permanently. **Close the lock descriptor (Windows: dispose the stream) before starting Bun.** A descriptor without close-on-exec survives the `exec` ([execve(2)](https://man7.org/linux/man-pages/man2/execve.2.html)), and a `flock` lock belongs to the open file description ([flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html)); otherwise Bun holds the install lock for the entry's whole run, and waiters run into `GETTY_BUN_LOCK_WAIT`. Our rule, derived from those semantics, not executed.

Normal cleanup must hold the mutex and check that the (proposed) `installId` still matches. A delayed handler running after release must reacquire and recheck; otherwise it could delete a newer owner's marker. A token check without serialization remains a check-then-delete race.

## Recovery and process lifetime

Successful mutex acquisition authorizes recovery within a known compatible store. No conforming installer still owns that critical section. An empty, truncated, or malformed marker may therefore be recovered under the mutex, including a crash during initialization. While the mutex is held elsewhere, malformed or absent metadata only limits diagnostics.

Two recovery contenders must acquire the same mutex and re-read state; only the winner repairs it. After a crash following successful publication, validate the runtime and clean orphan status instead of reinstalling automatically.

Keep every shared-state writer protected for its entire lifetime. Do not assume a supervising lock wrapper survives its child. Either retain lock protection in surviving writers, or restrict workers to unique private staging paths with no publication authority. On Windows, publish inside the PowerShell process retaining the stream, with `[System.IO.Directory]::Move`; antivirus can hold a freshly written `.exe`, so retry moves and deletes on a sharing violation, bounded (about 10 s), then fail. Never fall back to copying into a slot. Keep staging ids short (MAX_PATH). Do not reuse or blindly delete a previous stage if an orphan worker could still write there.

Stop automatic takeover for an unsupported schema or an inconsistent requested version/target until compatible coordination is established. Doing the same for a foreign `environmentId` is a candidate rule beyond the phase 1 gate, tied to that proposed field. Do not adopt unknown legacy writers merely because their PID appears absent. Restrict the prototype to a local store with validated locking semantics; network shares, synchronized homes, WSL/native sharing, and cross-container access require separate verification. The [`flock` documentation](https://man7.org/linux/man-pages/man1/flock.1.html) explicitly describes filesystem-dependent limitations. Metadata and elapsed time cannot compensate for an unavailable or incompatible mutex.
