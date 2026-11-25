# Updates and retention

Checked: 2026-11-25. **Getty contract proposal v0.2:** these lifecycle rules are our policy. The MVP starter interface is `run`, `ensure`, `status`; there is no updater, `gc`, upgrade or rollback command, and none may be invented. Read [contract.md](contract.md) first.

## Update by adding a runtime key

A runtime key is an exact Bun version plus a target from the reviewed table. A new key installs beside existing ones; an occupied slot is never upgraded in place. Bun's self-upgrade command does not implement Getty's protocol; never use it on managed slots. [Bun installation and upgrading](https://bun.com/docs/installation#upgrading)

Keep published executables and receipts immutable. Do not overwrite `bun.exe` on Windows or try to replace a running executable. A slot that does not match fails closed; it is not repaired by an update.

## Change a consumer's Bun version

1. **Version in the table.** If the version is new: change agent-bun-runtime (table plus phase 1 scenarios, signature verified; procedure in agent-bun-runtime `bootstrap/README.md`, "Adding a version"), then update the template `getty-bun-install` in Getty/skills (ADR 0001). The table and the procedure are built; the template is planned.
2. **Consumer bump.** Set `vars.bun_version`, re-render both starters (until the template exists: `render-pin.ts` in agent-bun-runtime), set `gettyBun.bunVersion` to the same value, rebuild the bundled entry with the new Bun. CI checks that the pin block matches `package.json` and that the bundle rebuild is byte-identical.
3. **Release.** Ship starters, bundle and `package.json` together in one plugin release. The first starter call after users update installs the new key on demand; concurrent hooks wait on its lock.
4. **Host review.** Codex documents that a plugin update changing a bundled script needs a new hook review (documented, not executed; [codex.md](codex.md)). Expect it after a pin bump or rebuilt entry and note it in `Changes`.

A failed install leaves the previous slot untouched and the hook fails with one stderr line; the plugin stays idle until a starter call succeeds (the next hook or `ensure`). An already-running process keeps the executable it launched; subsequent starts use the pin of the installed plugin release.

## Coexistence and rollback

If consumer A pins the old version and B adopts a new one, both keys stay available; updating B does not touch A, because each consumer's committed pin selects its own slot.

Rollback in the MVP means installing the previous plugin release: its starters, pin and bundle come back together, and its slot is still present because nothing deletes slots. Do not run a new release under the old Bun merely because it starts. Do not use a mutable shared `current` alias.

**Later/optional, with the dependency install (plan phase 5):** a machine-local binding with a retained last-working binding. Then publish the new binding atomically only after the candidate's runtime, dependencies, and smoke test pass; keep the previous binding and its complete release/dependency identity for rollback; coordinate binding changes with launches so an execution receives one complete release/runtime tuple. A candidate slot installed before a later consumer failure can remain unused.

## Retain conservatively

Retention and pruning are later, not in the MVP. Consumer uninstall removes only consumer-owned state; even uninstalling the last known consumer does not remove shared runtimes, because incomplete bookkeeping and active processes are no deletion evidence.

Until a `gc` exists, do not delete slots by hand as routine maintenance. Automated pruning later requires reliable accounting for every consumer pin, rollback retention, active executions, concurrent installs, and all environments; serialize it against installs and launches, and recheck references under that coordination. If liveness or ownership is uncertain, retain the slot. Never delete the permanent mutex objects; cleaning old attempt data is a separate operation.
