# Getty integration contract

Status: **proposal v0.2**, checked 2026-11-25. These are Getty design decisions, recorded in the `getty-bun` repository (`docs/plan.md`, `docs/adr/0001`–`0006`); where this skill and they disagree, they win. **Nothing is implemented yet:** the starters `getty-bun.sh` and `getty-bun.ps1` and the skilletor template `getty-bun-install` are planned (getty-bun phase 1), not built or tested.

## Responsibilities

| Component | Owns |
| --- | --- |
| Bootstrap (`getty-bun`, delivered as template `getty-bun-install`) | Reviewed version table (SHA256 per target, expected archive member), pin render, the two starters: target detection, install on demand under the OS lock, staging, receipt, atomic publish, fast path, `run`, `ensure`, `status`. |
| SDK `@getty/bun-runtime` | Context, host codecs, effects, `main(): Promise<number>`. Never installs, downloads, or edits lockfiles, not even in a diagnostic command. |
| Consumer plugin/tool | `gettyBun` pin in `package.json`, `vars.bun_version` for the template, the committed rendered starters, the committed bundled entry, CI that checks both, host hook adapter, setup skill for repair and diagnosis, hook timeouts above the lock wait plus one download. |
| Agent host | Instruction/skill/hook surfaces, workspace trust, hook review, execution, timeouts. |
| Setup agent | Repair and diagnosis through the packaged setup skill within session authorization; reporting what the starter said. Not the install path. |

Call the provider `getty-bun`. There is no `getty-bun` command on PATH: the provider is the pair of rendered starters committed into each consumer. Keep the managed executable named `bun` or `bun.exe`. The starter interface is `run`, `ensure`, `status` and nothing else; `repair`, `gc`, upgrade and rollback are later and unspecified. If the starters do not exist yet, building them in `getty-bun` is the first task, not a consumer workaround.

## Starter interface (planned, MVP)

```text
getty-bun.sh  run <entry> [args...]   ensure, then exec the absolute Bun with --no-install
getty-bun.sh  ensure                  install if missing; nothing on stdout
getty-bun.sh  status                  one JSON object on stdout: pin, target, slot, state
getty-bun.ps1 <same commands>         identical behavior and exit codes
```

- `run` and `ensure` install on demand: a present, matching slot is a fast local check; a missing one is installed under the OS lock. Concurrent calls wait on the same lock, bounded, then re-check. `status` is not listed as installing (ADR 0002).
- `run` closes the lock descriptor (Windows: disposes the lock stream) before it starts Bun; otherwise Bun inherits the install lock for the entry's whole run. Our rule, derived from flock(2)/execve(2) semantics, not executed ([installation-locking.md](installation-locking.md), step 6).
- The consumer root comes from the starter's own path, never from the working directory. `<entry>` is relative to that root.
- stdout belongs to the entry (hook JSON); starter messages go to stderr.
- Exit 0 when ready; 1 for every starter failure, with one stderr line naming what failed and where. The starter never exits 2 for its own failures (some hosts read 2 as a block); the entry's exit code passes through unchanged, 2 included.
- Fast path: no network, no hashing; the receipt's version and target match the pin, and the executable is present. A slot that does not match fails closed with a message naming the path; it is never overwritten. Whether the fast path also runs `bun --version` (one Bun start per hook) or only the install does is still open in the plan: its scenario 6 expects a `bun --version` mismatch to fail closed.

Environment (planned):

| Variable | Effect |
| --- | --- |
| `GETTY_HOME` | Absolute root; overrides `~/.getty` (Windows: user profile plus `\.getty`). Tests always set it. |
| `GETTY_BUN_MIRROR` | Download base URL. The pinned checksum still decides. |
| `GETTY_BUN_LOCK_WAIT` | Bounded lock wait, default 300 s. Must stay below the host hook timeout, which the consumer sets above the wait plus one download. |

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

v0.2 keeps `contractVersion: 1`; the declaration did not change. The version is illustrative (1.4.5 is the plan's candidate pin, confirmed only after phase 1), not a recommendation or compatibility certification. Contract version 1 accepts only stable `major.minor.patch`, without a leading `v`, ranges, tags, prereleases, or build suffixes.

[The schema](../assets/requirement.schema.json) validates the `gettyBun` object, not the entire manifest. Bun does not enforce it, and the starter does not read it: the starter's rendered pin block is the only thing that selects a version. The consumer's CI validates the `gettyBun` object against the schema, which rejects any `contractVersion` other than 1 and a malformed `bunVersion`, and checks that the pin block equals `gettyBun.bunVersion`.

Keep ordinary requirements in `dependencies`/`devDependencies` and commit `bun.lock`; with a bundled entry they are build inputs resolved in CI, not on user machines. Do not infer the runtime pin from an arbitrary executable, `engines`, or a lockfile format. Optional toolchain metadata may mirror the exact pin but must not introduce a second runtime provisioner; see [prior-art.md](prior-art.md).

## Delivery of the starters (planned)

- The template `getty-bun-install` in Getty/skills holds the reviewed version table. Each consumer renders it with its own `vars.bun_version`; the render writes one pin block (version plus SHA256 per target) into both starters. An unknown version fails the render (skilletor treats an undefined variable as an error).
- The rendered starters are committed into the consumer, because hosts install plugins by cloning.
- skilletor cannot yet render into a plugin's own tree (planned for phase 3b). Until then, copy the rendered starters by hand and let the consumer's CI compare them with a fresh render.
- A new Bun version is a change in getty-bun (table plus tests), then a template update in Getty/skills, then one `vars.bun_version` bump per consumer.

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

The version table (`bootstrap/versions.json` in getty-bun, planned) lists each approved version with the SHA256 of every supported target's archive and the name of the single expected member. Adding a version means verifying Bun's `SHASUMS256.txt` against its GPG signature `SHASUMS256.txt.asc` (observed for bun-v1.4.5) with the release key recorded in the table's README, then running the phase 1 scenarios. The starter never downloads `SHASUMS256.txt` at install time and never trusts a checksum fetched next to the archive.

The starter verifies the archive hash before unpacking, extracts exactly the expected member by name, and requires `bun --version` to equal the pin before publishing. Write `receipt.json` only after that. It records the exact Bun version, the target and the relative executable path, which the fast path reads. Further fields (contract version, asset identity, archive hash, resulting binary hash, verification timestamp) are proposed diagnostics; skill `getty-bun-bootstrap` does not require them, and phase 1 decides which stay. A receipt records a verified operation; it does not alone prove that today's file exists. The fast path therefore checks receipt version and target against the pin and that the executable is present, without network or hashing.

## Consumer binding

**Bundled entry (normal case):** no consumer lock and no machine-local binding (ADR 0003); `run` needs only the runtime slot. The committed pin block takes the binding's place: every starter call derives the slot from it, and the committed bundle is the only code that runs. A moved or updated plugin needs no rebind.

**Later/optional (plan phase 5, for a consumer that cannot bundle):** a frozen-lockfile dependency install on the user machine under a consumer lock, with a machine-local binding: consumer/content identity, package root, manifest and lockfile digests, runtime key, resolved absolute executable, receipt identity, dependency and smoke-test result. Publish it only after runtime and dependencies pass; reject a mismatch at execution instead of selecting another Bun. The runtime-key mutex does not protect a separate `node_modules` tree. See [dependencies-and-execution.md](dependencies-and-execution.md).

## Portability boundary

Distribute the same bundled TS/JS entry across supported targets without compiling a custom executable per OS. A compatible Bun binary from the table and the matching starter are still required. Shell commands, filesystem conventions, native add-ons (which rule out bundling), and host APIs remain platform-sensitive. Verify these boundaries rather than promising universal execution from a file extension.

## Changes from v0.1

1. **Who installs.** v0.1: hooks only point the agent at a setup skill; context injection does not complete installation. v0.2: the consumer's committed starter installs on demand under the OS lock on every `run`/`ensure`, so after a plugin install or update the first hook (normally `SessionStart`) installs and concurrent hooks wait, bounded. The SDK never installs. The setup skill is repair and diagnosis.
2. **Bundled entry.** v0.1: frozen-lockfile dependency install plus a machine-local binding. v0.2: the consumer commits `bun build --target=bun` output; no `bun install` on user machines. The dependency install, consumer lock and binding are kept as a later option.
3. **Delivery.** v0.2 names the provider: template `getty-bun-install` renders `vars.bun_version` into the pin block of `getty-bun.sh` and `getty-bun.ps1`; interface `run`, `ensure`, `status`.
4. **Root and environment.** v0.1: an alternative root is one persisted provider setting. v0.2: `GETTY_HOME`, `GETTY_BUN_MIRROR`, `GETTY_BUN_LOCK_WAIT`.
5. **Windows.** PowerShell starter (5.1 and 7), Git Bash/MSYS/Cygwin forwarding, `FileShare.None` lock, Bun run through `System.Diagnostics.Process` with byte copies, Codex `commandWindows`; the Claude Code adapter on Windows is an open decision.
6. **Integrity.** v0.1: reviewed checksums from a documented trusted update path, not named. v0.2: the version table in getty-bun holds the SHA256 per target, taken from Bun's `SHASUMS256.txt` after verifying its GPG signature; the starter never downloads `SHASUMS256.txt` at install time (ADR 0005).
7. **Starter process rules.** v0.1 reserved stdout for the consumer's protocol and preserved exit codes. v0.2 makes them starter rules: starter messages go to stderr; starter failures exit 1, never 2; the entry's exit code passes through unchanged; `run` closes the lock descriptor before Bun starts.
8. **Unchanged:** the `gettyBun` declaration and its schema, the slot layout, the mutex/status split, immutable slots, `--no-install`.
