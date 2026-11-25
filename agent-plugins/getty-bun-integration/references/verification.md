# Integration verification

Status: Getty contract proposal v0.2. Use this to verify an implementation. The starters passed the provider gate below; no consumer integration and no host run (Codex, Claude Code) is recorded here. Select the cases material to the claimed environments and record concrete evidence.

## Establish the test subject

Record the getty-bun revision the starters were rendered from, the consumer revision, the exact Bun pin, the table's checksum for each target, OS/architecture/libc/CPU target, agent client version, and distribution surface. Identify the actual process executing the tool. A Windows host and its WSL distribution are separate subjects.

Label each finding: **documented** (vendor documentation says so; not run), **source-checked**, **schema-checked**, **scenario-reviewed**, **executed** (with command, host version and platform; for getty-bun's CI the run ID and commit), **measured by windows-developer** (executed there; cite the hub document), or **not checked**. Never turn source inspection or a successful `--version` command into an end-to-end support claim. A mocked stdin/stdout test proves the codec, not the host. A Windows claim needs a run on Windows.

## Provider gate (getty-bun, phase 1)

The starters are verified in getty-bun, not in each consumer. The gate passed at `262bc95`: CI 45603412444 (pull request) and 45604685681 (`main`), 10 of 10 jobs green. One shared `bun:test` suite ran the plan's scenarios 1–10 against both starters on `ubuntu-latest` (linux-x64), `ubuntu-24.04-arm` (linux-arm64) and `windows-latest` under `powershell` (5.1) and `pwsh` (7), scenario 11 on both Windows shells, and further cases: 2b (Bun does not inherit the lock), 8b (the host keeps stdin open), a `file://` mirror, the starter contract and interface details. Each case used `GETTY_HOME` in a fresh temporary directory, a `PATH` without Bun and a fixture server through `GETTY_BUN_MIRROR`; two jobs downloaded from GitHub for real (linux-x64, Windows PowerShell 5.1). `shellcheck` and the pin-block check passed, and the per-hook cost is in getty-bun `docs/hook-cost.md`. A consumer cites that gate for the getty-bun commit its starters came from; it does not re-test locking.

Outside the gate, not checked: any host (Codex, Claude Code); a Windows desktop (Defender real-time protection on, an OEM code page, a proxy, AppLocker or WDAC, Constrained Language Mode); a CPU without AVX2; WSL, macOS, musl; the wget download path; hook cost on `linux-aarch64`.

## Consumer behavior

| Case | Evidence to collect |
| --- | --- |
| First hook, no external Bun/Node | The first hook after plugin install installs through the starter; no hint, setup skill or agent turn is needed. |
| Concurrent first hooks | Two sessions or matching hooks: one download, one publish, all run or fail clearly. |
| Lock wait runs out | One stderr line, exit 1, no partial slot; the hook timeout was above the lock wait plus one download. |
| Matching shared runtime | Two consumers with the same pin use the same absolute slot; the second takes the fast path without network. |
| Wrong PATH Bun | Ignored; neither adopted nor modified. |
| Wrong/corrupt slot | Receipt version or target not matching the pin, or the executable missing or empty: fails closed with the path; no overwrite. A Bun whose `--version` differs from the pin is rejected at install only; the fast path never starts Bun, so a damaged non-empty executable is not caught there (plan, scenario 6). |
| Pin consistency | CI: `gettyBun` validates against the schema (`contractVersion` 1 only); the starters' pin block equals `gettyBun.bunVersion`; the committed starters equal a fresh render (`render-pin.ts --check`, through `getty-bun-install` once it exists). |
| Bundled entry | CI: a rebuild with the pinned Bun is byte-identical; no `external` packages; a missing import fails at run time without a download. |
| Offline after install | `run` works without network. |
| Native Windows and WSL | Separate roots, targets and slots; Git Bash forwarding uses the same slot and lock as PowerShell. |
| Windows PowerShell | Works on 5.1 and 7 under the host; stdin reaches the entry including end of input, and the hook ends when the entry ends; a blocking execution policy is reported by the setup skill. |
| Paths and protocols | Spaces and non-ASCII characters in `GETTY_HOME` and the consumer root; under Codex also a plugin root with `"`, `$` or `` ` `` (textual `${PLUGIN_ROOT}` substitution, [codex.md](codex.md)); stdout byte for byte (UTF-8); the starter never exits 2 for its own failures; the entry's exit code passes through unchanged, 2 included, and stays within 0–255; no entry argument begins with `-`. |
| Version update A to B | B installs beside A on the first call after update; another consumer pinned to A keeps A. |
| Rollback | The previous plugin release runs on its still-present slot. |
| Host trust/activation | Changed hooks obey native review; Codex re-review after a changed bundled script observed; active definitions verified. |
| Consumer uninstall | Only consumer-owned state is removed; shared runtimes remain. |
| Dependency install (later, phase 5 only) | Missing lockfile rejected before frozen install; failed setup publishes no binding; the previous release stays usable. |

## Lock and crash cases

Exercise the implementation of [installation-locking.md](installation-locking.md) with real concurrent processes (provider side, in getty-bun). The phase 1 gate executed these (CI 45603412444, every leg):

1. Start multiple requests for one missing key. Observe one publisher; waiters re-read and reuse (scenario 2).
2. Hold the mutex until a waiter's `GETTY_BUN_LOCK_WAIT` runs out: clear message, no partial slot, no state deleted (scenario 3; the holder is a fixture process without a marker).
3. Feed a wrong checksum and an archive with an unexpected or extra member. Nothing is published; staging is cleaned (scenarios 4, 5).
4. Start `run` on a fresh install and take the install lock while the entry runs: Bun does not hold it (scenario 2b).

Candidates beyond the phase 1 gate, proposed for getty-bun and not in its suite:

5. Hold the mutex with an old or malformed marker. Others wait or time out without deleting state.
6. Interrupt before marker creation, during marker write, after marker publication, and after runtime publication, by a handled signal and by SIGKILL. Verify the next owner recovers or validates without exposing a partial ready slot.
7. Reuse a PID/name with a different start identity; separately deny process inspection. Neither condition bypasses a held mutex or kills a process.
8. Start two stale-state recoverers together. Verify serialization and re-reading after acquisition.
9. Delay an earlier owner's cleanup until a new attempt starts. The new marker survives; the permanent lock object remains unchanged.
10. Kill the coordinator while a worker survives. The worker stays protected or confined to its unique stage and cannot publish shared state.
11. Exercise missing lock capability, foreign environment/protocol, and unverified filesystem semantics. Installation and recovery stop before unsafe mutation.

For process termination tests, use isolated fixture stores and fixture processes. Never kill a user's unrelated process or touch the real `~/.getty`, `~/.codex` or `~/.claude`. A local Linux result does not validate Windows or macOS semantics.

## Adequate verification and reporting

Prioritize the real release gate and concrete failure risks. Do not add tests that merely repeat metadata literals or unrelated broad suites. After meaningful checks pass, stop optional expansion and deliver the work.

For documentation-only changes, validate frontmatter, schema/examples, relative references, and an independent realistic integration scenario. Record runtime cases as not executed. For starter or adapter changes, run them in the claimed environments or narrow the support statement to what was observed.

Use [the review template](../assets/integration-review-template.md) to summarize decisions, evidence, limitations, and any required host activation step.
