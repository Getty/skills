# Durable timing and state

## Choose by required survival

| Mechanism | Use | Recovery concern |
| --- | --- | --- |
| Short delay/wait | Transient sequence | Execution is lost when the run/process stops |
| Trigger `for:` | Debounce a continuously satisfied condition | Restart/reload resets the pending wait |
| Timer helper with restore | Visible countdown | Expiry while HA is down does not emit `timer.finished` on startup |
| Absolute datetime + pending flag | Deadline requiring reconciliation | Must define overdue behavior and duplicate handling |
| Device-side schedule/auto-off | Continues without HA if device supports it | Verify exact device semantics and feedback |

The timer limitation is explicitly documented; a restored timer is not an exactly-once job queue. [Timer](https://www.home-assistant.io/integrations/timer/). Use an absolute date/time helper when timing intent must survive reloads. [Input Datetime](https://www.home-assistant.io/integrations/input_datetime/).

## Reconciliation pattern

Store `deadline` and `pending`. Trigger evaluation at the deadline, HA startup, relevant device recovery, and a low-rate fallback if needed. If pending and due, inspect current conditions, perform an idempotent action, and clear pending only after acceptable success. On failure, keep pending and bound retries/alerts; do not silently lose the operation.

The bundled light-session package illustrates this pattern for a harmless lamp. It retries at minute boundaries when necessary and does not depend on a timer completion event. Map its fictional entity and review its manual-control policy before installing. It does not guarantee physical execution or exactly-once delivery.

All start, cancel, and reconcile operations use one queued script, so a finishing old run cannot clear a newly requested session while it is executing. Call `script.study_light_session` with `operation: start` to create/renew ten minutes, `cancel` to remove the deadline without changing power, or `reconcile` to check overdue work. Do not bypass that owner with other helper-writing automations. Here, renew means ten minutes from the new request; adding ten minutes to the old deadline is a different operation and must use the same serialized owner. In-memory queued requests do not survive a restart. Only the persisted intent can be reconciled, and HA cannot perform the due action while HA itself is down. Test helper restoration and abrupt interruption separately from an orderly restart.

This file is a configuration package, not a standalone automation-editor entry. Use the instance's existing package setup, or first follow the official [package configuration](https://www.home-assistant.io/docs/configuration/packages/) and validate before reload/restart. Script direct calls and queued modes follow the [script contract](https://www.home-assistant.io/integrations/script/). Keep a copy of prior configuration for removal/rollback.

## Define overdue policy

“Run immediately,” “skip if too late,” and “ask the household” are different contracts. Turning off an overdue study lamp may be acceptable; replaying a door unlock, irrigation cycle, or appliance start after an outage usually needs different logic. Store enough state to distinguish an old session from a new one. Never replay a stale command solely because it survived on disk.

## Race analysis

Consider a new request arriving while the old one executes, cancellation just before the deadline, device unavailability, and startup before helpers have restored. Recheck pending/deadline immediately before action. Prefer explicit set-state actions over toggle. Use one owner for the deadline and serialized short critical sections where practical.

For non-idempotent commands, use device feedback or a transaction identifier if the actual API supports it. A HA context ID helps tracing but is not automatically a remote device deduplication key.

## Verification

Test ordinary completion, restart before due, restart after due, manual cancellation, changed deadline, unavailable actuator, and a second request. Static YAML parsing checks structure only. An end-to-end physical test remains necessary before trusting a protective application.
