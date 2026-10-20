# Transactional outbox, durable outcomes, and cancellation

Read when acceptance must survive crashes or clients need later results. This is an **application architecture**. Native acceptance/status semantics are described by [G3, H2](sources.md).

## Transactional outbox

In the same database transaction as the business request, insert a request record and an outbox row. A dispatcher claims eligible rows with an owner/lease mechanism appropriate to that database, sends a Gearman delivery, records the origin server/handle when known, and releases or advances the row. Multiple dispatchers must not race without a coordinated claim.

Do not mark a row definitively completed because the server accepted the job. Conversely, do not delete a row before submission is acknowledged. A crash after send but before updating the outbox is ambiguous: republishing may be necessary, so worker deduplication remains required. No ordering of two unrelated systems' writes makes them one transaction.

Store request ID, delivery ID, business fingerprint, function/version, attempt metadata, next eligible time, claim owner/expiry and safe failure class. Keep raw secrets out of the outbox. Use a unique delivery ID per application-controlled publication attempt when needed; keep the request ID stable across those attempts.

## Results store and reconciliation

Use explicit states such as accepted, executing, completed, failed, cancelled and outcome-unknown; define allowed transitions and ownership. A worker persists a terminal outcome before reporting terminal completion where the effect/outcome boundary permits it. A reconciler finds accepted requests that have exceeded their expected progress window and checks the authoritative business outcome before authorizing another delivery.

A Gearman handle disappearing means the native server does not currently know that handle. It does not distinguish success, failure, restart, cancellation, wrong origin server or loss. A result endpoint should query application state, never implement `unknown => succeeded`.

The included SQLite `ResultStore` has a deliberately narrower contract: a successful result and an illustrative effect counter commit atomically; duplicate requests return the committed result; conflicting payloads fail; an injected pre-commit crash rolls back both. It does not implement dispatcher leasing, a production outbox, shared multi-host storage, retention or external side effects.

## Cooperative cancellation

Persist a cancellation request by business identity. A worker checks it before execution and at defined safe points, and records whether the operation was prevented, partially performed, or already completed. Cancellation arriving after an irreversible effect is not retroactive rollback.

Native queued-job cancellation is a different operational action and is version/command-specific. Removing queue state cannot kill arbitrary work already running in another process. Preserve authorization, audit and impact information for native cancel/drop commands. Cancelling a client's local future also does not establish remote cancellation.

## Retention and recovery

Retain dedup/outcome records longer than the maximum replay/redelivery horizon, including backups that might resurrect old jobs. Define expired-result behavior explicitly. During disaster recovery restore queue and business state to a compatible recovery point or reconcile their difference by request identity. Never delete the dedup ledger while leaving old persistent jobs eligible to replay.
