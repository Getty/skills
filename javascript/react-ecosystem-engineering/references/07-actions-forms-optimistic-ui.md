# Actions, pending states, and optimistic mutations

**Read when:** implementing submission workflows, optimistic changes, or server actions.

## Define the mutation protocol first

Specify a stable operation ID, validated input, authorization check, idempotency behavior, conflict model, and canonical response. A disabled button improves interaction but is not a duplicate-submission guarantee. Enforce critical invariants at the service boundary. Separate form field errors, business-rule rejection, transport failure, and unknown completion after a timeout.

React action-related APIs can coordinate action state, pending UI, and optimistic display. Adopt them only after inspecting the React/framework version and how action functions are dispatched. `useActionState` and `useOptimistic` do not replace authorization, a database transaction, or a durable offline queue. Keep the optimistic calculation pure and deterministic.

## Design optimistic behavior

Choose an operation suitable for prediction: toggling a preference is easier than allocating scarce inventory. Record the base revision and temporary client IDs. On success reconcile with the canonical server result; on rejection remove only the optimistic operation that failed. Avoid rolling back an entire stale snapshot over another mutation's successful result. For concurrent operations, maintain a pending-operation layer or serialize conflicting edits.

Show pending, confirmed, failed, and retryable states deliberately. Preserve user input after failure. An operation that may have succeeded remotely needs status reconciliation before blind retry; use an idempotency key where supported.

## Tests

Complete two mutations in the reverse order, reject the first, retry after a timeout, submit twice, and navigate away during submission. Verify no duplicate entity, no lost acknowledged change, and no hidden failure. Test optimistic list ordering and temporary-ID replacement. For server actions, review the actual framework transport, request-size limits, same-origin/CSRF protections, and authorization at every callable operation.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R07: useActionState](https://react.dev/reference/react/useActionState)
- [R08: useOptimistic](https://react.dev/reference/react/useOptimistic)
- [R09: use](https://react.dev/reference/react/use)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
