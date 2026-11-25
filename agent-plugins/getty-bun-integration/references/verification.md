# Integration verification

Status: Getty contract proposal v0.1. Use this to verify an implementation; this file does not record successful runtime tests. Select the cases material to the claimed environments and record concrete evidence.

## Establish the test subject

Record the provider revision/API, consumer revision, exact Bun pin, approved artifact/checksum, OS/architecture/libc/CPU target, agent client version, and distribution surface. Identify the actual process executing the tool. A Windows host and its WSL distribution are separate subjects.

Label each finding: **source-checked**, **schema-checked**, **scenario-reviewed**, **executed**, or **not checked**. Never turn source inspection or a successful `--version` command into an end-to-end support claim.

## Required behavior

| Case | Evidence to collect |
| --- | --- |
| First setup, no external Bun/Node | Setup hint/skill loads; available bootstrap tools are checked; provider runs without requiring the missing runtime. |
| Matching shared runtime | Two projects/consumers bind to the same absolute version/target executable; second setup reuses it. |
| Wrong PATH Bun | Consumer uses its private exact pin; PATH Bun is neither adopted silently nor modified. |
| Wrong/corrupt slot | Mismatched version, target, receipt, or executable fails readiness; no in-place overwrite of an active slot. |
| Native Windows and WSL | Separate environment roots/targets/bindings; neither assumes the other's executable or mutex. |
| Package moved or updated | Old package-root/manifest/lock binding is invalidated and rebuilt for the actual release. |
| Missing lockfile | Consumer setup rejects it before frozen installation. |
| Missing dependency | Normal execution fails with a setup/repair action and performs no package download. |
| Dependency setup failure | No ready consumer binding is published; previous installed release remains usable. |
| Version update A to B | B installs beside A; consumer binding changes only after verification; another consumer pinned to A continues using A. |
| Failed update/rollback | Existing binding remains valid; rollback selects retained verified runtime and matching consumer dependencies. |
| Paths and protocols | Spaces/Unicode survive argument passing; correct package/project roots; logs do not corrupt hook or MCP stdout. |
| Host trust/activation | Changed hooks obey native review; active loaded definitions are verified; setup hints do not claim readiness. |
| Consumer uninstall | Only consumer-owned state is removed; shared runtimes used by other consumers remain. |

## Lock and crash cases

Exercise the implementation of [installation-locking.md](installation-locking.md) with real concurrent processes:

1. Start multiple requests for one missing key. Observe one publisher; waiters re-read and reuse.
2. Hold the mutex with an old, missing, or malformed marker. Others wait or time out without deleting state.
3. Interrupt before marker creation, during marker write, after marker publication, and after runtime publication. Verify the next owner recovers or validates without exposing a partial ready slot.
4. Reuse a PID/name with a different start identity; separately deny process inspection. Neither condition bypasses a held mutex or kills a process.
5. Start two stale-state recoverers together. Verify serialization and re-reading after acquisition.
6. Delay an earlier owner's cleanup until a new attempt starts. The new marker survives; the permanent lock object remains unchanged.
7. Kill the coordinator while a worker survives. The worker stays protected or confined to its unique stage and cannot publish shared state.
8. Exercise missing lock capability, foreign environment/protocol, and unverified filesystem semantics. Automatic installation/recovery stops before unsafe mutation.

For process termination tests, use isolated fixture stores and fixture processes. Never kill a user's unrelated process or corrupt their real runtime store for a test. A local Linux result does not validate Windows or macOS semantics.

## Adequate verification and reporting

Prioritize the real release gate and concrete failure risks. Do not add tests that merely repeat metadata literals or unrelated broad suites. After meaningful checks pass, stop optional expansion and deliver the work.

For documentation-only changes, validate frontmatter, schema/examples, relative references, and an independent realistic integration scenario. Record runtime cases as not executed. For executable installer or adapter changes, run them in the claimed environments or narrow the support statement to what was observed.

Use [the review template](../assets/integration-review-template.md) to summarize decisions, evidence, limitations, and any required host activation step.
