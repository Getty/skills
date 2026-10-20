# Upgrades, backup, restore and recovery

Evidence: [G1, G9–G12, S1, S2](sources.md). Use the [upgrade template](../assets/templates/upgrade-checklist.md) to record a deployment-specific decision.

## Upgrade inventory

Record gearmand and libgearman versions independently, every binding/runtime, package/build flags, queue backend and its configuration, storage format, TLS mode, function/schema versions and operation-ledger version. Separate a server upgrade from a client-library upgrade; they can affect different ordering and API behavior.

Read release notes between both endpoints, not only the final release. For 1.x to 2.x, exercise function/priority scheduling, round-robin behavior, task submission ordering, epoch jobs and worker TLS capability. For 2.1, explicitly revisit a configured retry value of zero. Do not transfer stale website defaults into the new service definition.

## Drain and compatibility

Stop or reroute admission to the old owner, keep compatible workers available, and monitor both queue state and unresolved application IDs. Delayed jobs may prevent an ordinary drain from reaching zero soon. Decide whether to keep them on the old owner, replay through a tested migration or reschedule from an authoritative ledger. Do not edit a live backend table and expect the in-memory queue to reflect the edit.

Keep old and new function/schema versions registered during compatible rollout. Do not deploy a worker that rejects every old queued payload. If a migration transforms payloads, preserve original request identity and record the transformation so reconciliation can distinguish a replay from a new operation.

## Backup and restore

Back up configuration, exact binary/package metadata, certificates through the approved secret-backup process, queue backend and application outcome/outbox data. A queue backup alone does not say which external effects already committed. Define consistency points and retention for each store.

Before restore, fence the previous owner. Restore into an isolated environment first, verify row/record readability, binary data, unique IDs, priorities and delayed timestamps, then replay known fixtures. A restored old queue may include operations whose business effects already happened after the backup. The outcome ledger/provider idempotency policy must absorb that replay safely.

## Rollback conditions

Rollback is not just reinstalling an older executable. Check whether the new version changed stored representation or job semantics. Preserve a tested compatible snapshot or migration path. Define measurable rollback triggers, maximum uncertainty and an owner authorized to decide when replay is safer than waiting.

After any change, reconcile accepted application IDs, compare committed effects, inspect rejected/unknown outcomes and verify no queue is stranded on an unreachable origin. Close the change only after an end-to-end control and recovery check pass, not merely when the new process starts.
