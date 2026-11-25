# Getty integration contract

Status: **proposal v0.2**, checked 2026-11-25. These are Getty design decisions, recorded in the `agent-bun-runtime` repository (`docs/plan.md`, `docs/adr/0001`–`0008`); where this skill and they disagree, they win.

- **Built (agent-bun-runtime phase 1, `262bc95`):** the starters `getty-bun.sh` and `getty-bun.ps1`, the version table and the pin render in `bootstrap/`. `bootstrap/README.md` there is their behavior contract. They passed the phase 1 gate in agent-bun-runtime's CI: runs 45603412444 (pull request) and 45604685681 (`main`), 10 of 10 jobs green ([verification.md](verification.md), "Provider gate"). In this skill, "executed, scenario N" means that suite in run 45603412444, on all legs the scenario runs on.
- **Planned, not built:** the skilletor template `getty-bun-install` that delivers the starters to consumers, the SDK `@getty/agent-bun-runtime`, and every host adapter. How Codex and Claude Code run the starters is not checked; the CI runners are no desktops.

## Responsibilities

| Component | Owns |
| --- | --- |
| Bootstrap (`agent-bun-runtime` `bootstrap/`, built; delivery as template `getty-bun-install`, planned) | Reviewed version table (SHA256 per target, expected archive member), pin render, the two starters: target detection, install on demand under the OS lock, staging, receipt, atomic publish, fast path, `run`, `ensure`, `status`. |
| SDK `@getty/agent-bun-runtime` | Context, host codecs, effects, `main(): Promise<number>`. Never installs, downloads, or edits lockfiles, not even in a diagnostic command. |
| Consumer plugin/tool | `gettyBun` pin in `package.json`, `vars.bun_version` for the template, the committed rendered starters, the committed bundled entry, CI that checks both, host hook adapter, setup skill for repair and diagnosis, hook timeouts above the lock wait plus one download. |
| Agent host | Instruction/skill/hook surfaces, workspace trust, hook review, execution, timeouts. |
| Setup agent | Repair and diagnosis through the packaged setup skill within session authorization; reporting what the starter said. Not the install path. |

Call the provider `getty-bun`; its repository is `agent-bun-runtime`. There is no `getty-bun` command on PATH: the provider is the pair of rendered starters committed into each consumer. Keep the managed executable named `bun` or `bun.exe`. The starter interface is `run`, `ensure`, `status` and nothing else; `repair`, `gc`, upgrade and rollback are later and unspecified. Missing provider behavior (the template, a target, a starter feature) is built in `agent-bun-runtime` first, never worked around in the consumer.

## Starter interface (MVP, built)

```text
getty-bun.sh  run <entry> [args...]   ensure, then exec the absolute Bun with --no-install
getty-bun.sh  ensure                  install if missing; nothing on stdout
getty-bun.sh  status                  one JSON object on stdout: pin, target, slot, state
getty-bun.ps1 <same commands>         identical behavior and exit codes
```

Plan, "Starter interface"; details in agent-bun-runtime `bootstrap/README.md`. Executed unless marked otherwise.

- **Location.** A consumer carries the starters as `<consumer-root>/bootstrap/getty-bun.sh` and `<consumer-root>/bootstrap/getty-bun.ps1`; the consumer root is the parent of the starter's directory, never the working directory. `<entry>` is relative to that root, written with `/` (the PowerShell starter converts it).
- **Install on demand.** `run` and `ensure` take the fast path for a matching slot and install a missing one under the OS lock; concurrent calls wait on the same lock, bounded, then re-check (scenarios 1, 2, 3).
- **`status` never installs.** It prints `pin`, `target`, `slot` (absolute) and `state`, one of `ready`, `missing`, `mismatch`, and exits 0 whenever it printed the object, 1 when the state cannot be determined (for example an unsupported target, or an invalid `GETTY_HOME` or `GETTY_BUN_LOCK_WAIT`).
- **Lock released before Bun.** `getty-bun.sh` holds the lock on a descriptor that only the install's command group has open; `getty-bun.ps1` disposes the lock stream after publishing; an entry never holds it. The rule rests on flock(2)/execve(2) semantics ([installation-locking.md](installation-locking.md), step 6); executed (scenario 2b: while an entry runs after a fresh install, the test takes the lock without waiting).
- **Streams.** stdout belongs to the entry (hook JSON); starter messages go to stderr, also during an install inside `run` (scenario 8). Give hook input on a pipe; for a stdin that is a character device under Git Bash, see [paths-platforms.md](paths-platforms.md) (a hint, not a requirement).
- **Exit codes.** Exit 0 when ready; 1 for every starter failure, with one stderr line beginning `getty-bun: ` that names what failed and where. The starter never exits 2 for its own failures (some hosts read 2 as a block); the entry's exit code passes through unchanged, 2 included (scenario 8: 0, 1, 2, 7, 42). 2 stays the entry's (ADR 0007, superseding that part of ADR 0002).
- **Exit codes on Windows are 0–255.** Bun 1.4.5 on Windows itself exits with the low byte of the entry's code (`process.exit(256)` gives 0), and the starters pass on what Bun exits with (executed, agent-bun-runtime CI 45589361806 and 45597390051). Keep an entry's codes within 0–255.
- **Entry arguments never begin with `-`.** `getty-bun.ps1` runs under `-File`, whose parameter binding may re-parse such an argument (PowerShell 7 splits `-x:foo`: a local run with pwsh 7 on Linux, not in CI; 5.1: not checked). The rule holds on both OS, so one entry call serves both.
- **Fast path.** No network, no hashing, and Bun is not started: the receipt's first three lines name the pinned version and the target, and `bin/bun` (`bin\bun.exe`) is a non-empty regular file (executable on POSIX). Only the install compares `bun --version` with the pin, before publishing (plan, scenario 6; `getty-bun.ps1` also after publishing, see the open difference below). A slot that does not match fails closed with a message naming its path and is never overwritten (scenario 6). A damaged but non-empty executable therefore passes the fast path, and `run` ends with what the OS makes of it, not a `getty-bun: ` line; removing the slot directory lets the next call install it again (`bootstrap/README.md`, "Limit: a damaged executable").
- **Open difference from "identical behavior" (card `agent-bun-runtime k19`).** After publishing and releasing the lock, `getty-bun.ps1` runs `bun --version` on the published `bun.exe` once more and exits 1 if it does not run; the slot stays published, so the next call takes the fast path and the failure shows only once. `getty-bun.sh` has no such probe (source-checked, `getty-bun.ps1:566-572`). agent-bun-runtime decides on `k19` whether to drop it or specify it for both starters.

Environment (built; contract tests):

| Variable | Effect |
| --- | --- |
| `GETTY_HOME` | Absolute root; overrides `~/.getty` (Windows: user profile plus `\.getty`; a drive-absolute or UNC path, UNC not checked). Set but not absolute is a starter failure. Tests always set it. |
| `GETTY_BUN_MIRROR` | Download base URL, `<base>/bun-v<version>/<archive>`. The pinned checksum still decides. Schemes are the downloader's: `getty-bun.sh` with curl (http, https, file) or wget (no file; that path not checked); `getty-bun.ps1` http, https, file. |
| `GETTY_BUN_LOCK_WAIT` | Bounded lock wait in whole seconds, default 300. Must stay below the host hook timeout, which the consumer sets above the wait plus one download (ADR 0007). |

## Canonical consumer requirement

Place this custom object in the consumer's real `package.json`:

```json
{
  "gettyBun": {
    "contractVersion": 1,
    "bunVersion": "1.4.5"
  }
}
```

v0.2 keeps `contractVersion: 1`; the declaration did not change. The version is agent-bun-runtime's pin: Getty confirmed 1.4.5 on 2026-11-25 (plan, "Decided"), and phase 1 tested it. Take the current pin from agent-bun-runtime (plan, "Decided"; `bootstrap/versions.json`) when you integrate; this example is no compatibility certification. Contract version 1 accepts only stable `major.minor.patch`, without a leading `v`, ranges, tags, prereleases, or build suffixes.

[The schema](../assets/requirement.schema.json) validates the `gettyBun` object, not the entire manifest. Bun does not enforce it, and the starter does not read it: the starter's rendered pin block is the only thing that selects a version. The consumer's CI validates the `gettyBun` object against the schema, which rejects any `contractVersion` other than 1 and a malformed `bunVersion`, and checks that the pin block equals `gettyBun.bunVersion`.

Keep ordinary requirements in `dependencies`/`devDependencies` and commit `bun.lock`; with a bundled entry they are build inputs resolved in CI, not on user machines. Do not infer the runtime pin from an arbitrary executable, `engines`, or a lockfile format. Optional toolchain metadata may mirror the exact pin but must not introduce a second runtime provisioner; see [prior-art.md](prior-art.md).

## Delivery of the starters (template planned)

- **Pin block and render, built.** agent-bun-runtime `bootstrap/README.md` ("Pin block", "Render CLI") fixes both. The block is eight `#` lines, byte-identical in both starters: a `version` line, then one `target` line per MVP target with archive name, SHA256 and the one archive member. `bun bootstrap/render-pin.ts --table <versions.json> --version <V> <file>...` writes it; with `--check` it changes nothing and exits 1 when a file differs from a fresh render; a version missing from the table fails (executed: render tests and the static CI job).
- **Template `getty-bun-install`, planned.** It builds on that format and render: it holds the reviewed version table in Getty/skills, and each consumer renders it with its own `vars.bun_version`. An unknown version fails the render (skilletor treats an undefined variable as an error).
- The rendered starters are committed into the consumer under `bootstrap/`, because hosts install plugins by cloning.
- skilletor cannot yet render into a plugin's own tree (planned for phase 3b). Until then, copy the starters from agent-bun-runtime `bootstrap/`, rendered for the consumer's version, by hand, and let the consumer's CI run `render-pin.ts --check` with `--version` set to `gettyBun.bunVersion`. Where that CI takes `render-pin.ts` and the table from is not decided.
- A new Bun version is a change in agent-bun-runtime (table plus tests; `bootstrap/README.md`, "Adding a version"), then a template update in Getty/skills, then one `vars.bun_version` bump per consumer.

## Shared immutable runtime slots

`runtimeRoot` is `<GETTY_HOME>/runtimes`, resolved once per user and execution environment ([paths-platforms.md](paths-platforms.md)).

| Item | Path relative to `runtimeRoot` |
| --- | --- |
| Runtime slot | `bun/<version>/<target>/` |
| Executable | `bun/<version>/<target>/bin/bun` or `bin/bun.exe` |
| Verified receipt | `bun/<version>/<target>/receipt.json` |
| Permanent mutex | `bun/.locks/<version>/<target>/.install.lock` |
| Attempt status | `bun/.locks/<version>/<target>/.installing` |
| Attempt stage | `bun/.staging/<unique-attempt-id>/` (same filesystem as the slots) |

The runtime key is the exact version plus a target from the reviewed table. MVP targets: `linux-x64`, `linux-x64-baseline`, `linux-aarch64`, `windows-x64`, `windows-x64-baseline`; musl, `windows-aarch64` and macOS come later as explicit entries. Validate targets against the table before using them as path components; never accept arbitrary path fragments.

All consumers in that environment requesting the same key reuse one slot. Different versions coexist. Published executables and receipts are immutable: publish once by one atomic rename of the whole staged slot, receipt included; never overwrite or repair in place. A version change installs a new key beside the old one on the first starter call after the consumer update.

Keep the store outside consumer caches and data that clients may erase on plugin upgrade/uninstall. Consumers must not delete shared runtimes on removal. Sharing is per user/execution environment, not across Windows, WSL, containers, remote hosts, or network-mounted homes.

## Integrity

The version table (`bootstrap/versions.json` in agent-bun-runtime, built) lists each approved version with the SHA256 of every supported target's archive and the name of the single expected member. Adding a version means verifying Bun's `SHASUMS256.txt` against its GPG signature `SHASUMS256.txt.asc` with the release key whose fingerprint `bootstrap/README.md` records (done for 1.4.5 with GnuPG 2.4.7 and `--assert-signer`), then running the phase 1 scenarios. The starter never downloads `SHASUMS256.txt` at install time and never trusts a checksum fetched next to the archive.

The starter verifies the archive hash before unpacking, accepts only an archive holding exactly the expected member plus its parent directories, extracts that member by name to `bin/bun` (`bin\bun.exe`), and requires `bun --version` to equal the pin before publishing (scenarios 4, 5, 6; `getty-bun.ps1` probes once more after publishing, card `agent-bun-runtime k19`). Then it writes `receipt.json` into the stage. Its form is fixed in `bootstrap/README.md` ("Slot and receipt"): ASCII, LF, two-space indentation, the keys `version`, `target`, `archiveSha256`, `contractVersion`, `archive`, `member`, `binarySha256`, `executable`, `verifiedAt` in that order. The starters read only its first three lines (`{`, version, target, compared as whole strings); they do not read `executable` but take `bin/bun` (`bin\bun.exe`) in the slot. `executable`, the hashes and the timestamp are diagnostics for other readers, which parse the receipt as JSON and ignore unknown keys. A receipt records a verified operation; it does not prove that today's file is intact.

## Consumer binding

**Bundled entry (normal case):** no consumer lock and no machine-local binding (ADR 0003); `run` needs only the runtime slot. The committed pin block takes the binding's place: every starter call derives the slot from it, and the committed bundle is the only code that runs. A moved or updated plugin needs no rebind.

**Later/optional (plan phase 5, for a consumer that cannot bundle):** a frozen-lockfile dependency install on the user machine under a consumer lock, with a machine-local binding: consumer/content identity, package root, manifest and lockfile digests, runtime key, resolved absolute executable, receipt identity, dependency and smoke-test result. Publish it only after runtime and dependencies pass; reject a mismatch at execution instead of selecting another Bun. The runtime-key mutex does not protect a separate `node_modules` tree. See [dependencies-and-execution.md](dependencies-and-execution.md).

## Portability boundary

Distribute the same bundled TS/JS entry across supported targets without compiling a custom executable per OS. A compatible Bun binary from the table and the matching starter are still required. Shell commands, filesystem conventions, native add-ons (which rule out bundling), and host APIs remain platform-sensitive. Verify these boundaries rather than promising universal execution from a file extension.

## Changes from v0.1

1. **Who installs.** v0.1: hooks only point the agent at a setup skill; context injection does not complete installation. v0.2: the consumer's committed starter installs on demand under the OS lock on every `run`/`ensure`, so after a plugin install or update the first hook (normally `SessionStart`) installs and concurrent hooks wait, bounded. The SDK never installs. The setup skill is repair and diagnosis.
2. **Bundled entry.** v0.1: frozen-lockfile dependency install plus a machine-local binding. v0.2: the consumer commits `bun build --target=bun` output; no `bun install` on user machines. The dependency install, consumer lock and binding are kept as a later option.
3. **Delivery.** v0.2 names the provider: template `getty-bun-install` (planned) renders `vars.bun_version` into the pin block of `getty-bun.sh` and `getty-bun.ps1`; interface `run`, `ensure`, `status`.
4. **Root and environment.** v0.1: an alternative root is one persisted provider setting. v0.2: `GETTY_HOME`, `GETTY_BUN_MIRROR`, `GETTY_BUN_LOCK_WAIT`.
5. **Windows.** PowerShell starter (5.1 and 7), Git Bash/MSYS/Cygwin forwarding, `FileShare.None` lock, Bun run through `System.Diagnostics.Process` with byte copies, Codex `commandWindows`; the Claude Code adapter on Windows is an open decision.
6. **Integrity.** v0.1: reviewed checksums from a documented trusted update path, not named. v0.2: the version table in agent-bun-runtime holds the SHA256 per target, taken from Bun's `SHASUMS256.txt` after verifying its GPG signature; the starter never downloads `SHASUMS256.txt` at install time (ADR 0005).
7. **Starter process rules.** v0.1 reserved stdout for the consumer's protocol and preserved exit codes. v0.2 makes them starter rules: starter messages go to stderr; starter failures exit 1, never 2; the entry's exit code passes through unchanged; `run` closes the lock descriptor before Bun starts.
8. **Unchanged:** the `gettyBun` declaration and its schema, the slot layout, the mutex/status split, immutable slots, `--no-install`.
