# Updates and retention

Checked: 2026-11-25. **Getty contract proposal v0.1:** these lifecycle rules are our policy. This skill supplies no installed updater, retention service, or `getty-bun` CLI. Read [contract.md](contract.md) before implementing an actual provider API.

## Update by adding a runtime key

Treat a runtime key as an exact Bun version plus verified target. Provision a new key alongside existing keys; never upgrade an occupied slot in place. Bun exposes a self-upgrade command, but it does not implement Getty's binding/retention protocol. Do not use it on managed slots. [Bun installation and upgrading](https://bun.com/docs/installation#upgrading)

Keep existing executables and receipts immutable. In particular, do not overwrite `bun.exe` on Windows or try to replace a running executable. A corrupt slot needs coordinated quiescence and repair under [installation-locking.md](installation-locking.md), not an ordinary update disguised as replacement.

## Publish the consumer binding last

1. Preserve the current consumer release, dependencies, and working binding. Identify exactly which consumer release is being updated; do not silently change every project sharing its runtime.
2. Review the new runtime requirement and trusted release/target metadata. Acquire the required runtime coordination, provision into unique staging, verify integrity and executable behavior, then publish the new slot according to the installation protocol.
3. Prepare the candidate consumer release separately, using its shipped manifest and lockfile. Coordinate its dependency setup independently of the runtime lock. Follow [dependencies-and-execution.md](dependencies-and-execution.md).
4. Validate the candidate with its selected runtime: exact version/target, dependencies, entry point, and the consumer's meaningful smoke tests. Recheck that the candidate requirement has not changed during setup.
5. Publish the new machine-local binding atomically only after validation. Retain the previous binding and its complete release/dependency identity for rollback. Coordinate binding changes with launches so an execution receives one complete release/runtime tuple.

A failed download, dependency installation, or smoke test leaves the previous binding active. Keep failure diagnostics tied to the candidate attempt. A candidate slot successfully installed before later consumer failure can remain unused; that is safer than deleting shared state opportunistically.

## Preserve coexistence and rollback

If consumer A requires the old version and B adopts a new version, both keys remain available. Updating B must not repoint A. An already-running process stays attached to the executable/release it launched; subsequent starts resolve the current verified binding.

Rollback restores the previous consumer release, its dependencies, and its matching runtime binding together. Do not run a new release declaring a new exact version under the old Bun merely because it starts. Reverify restored files and retain any candidate still referenced or running. Do not use a mutable shared `current` alias as the binding mechanism.

## Retain conservatively

Consumer uninstall removes only consumer-owned state. Even uninstalling the last known consumer does not automatically remove shared runtimes: incomplete bookkeeping and active processes must not become deletion evidence.

Default to manual, explicit pruning with a reviewable candidate list. Automated pruning requires reliable accounting for installed bindings, rollback retention, active executions, concurrent setup, and all supported environments. Serialize pruning against provisioning and new launches, then recheck references under that coordination. If liveness or ownership is uncertain, retain the slot. Preserve the permanent mutex objects required by the locking protocol; cleaning old attempt data is a separate operation.
