# Server configuration and operational policy

Read when writing service arguments or investigating effective configuration. Evidence: [G4, G5, S1](sources.md).

## Inspect before editing

Capture the service's executable and arguments, package configuration includes, environment sources, listener addresses, file permissions, resource limits and backend connection settings. Redact secrets before saving an inventory. Do not assume an `/etc/default` variable is consumed just because an old Debian recipe uses it. Likewise, do not assume a `gearmand.conf` path or INI syntax exists in every package.

| Setting family | Engineering question |
|---|---|
| Listen address and port | Which hosts can reach both submission and administrative commands? |
| Queue backend | What exact build plugin, storage identity, permissions and replay capacity are used? |
| Retry threshold | What happens to a repeatedly disconnected job under this server version? |
| Threads and wakeups | Which measured bottleneck is being changed? |
| File descriptors/backlog | What connection burst and steady-state demand must fit? |
| Keepalive | How quickly must dead peers be noticed, and what middlebox limits exist? |
| Logging | Is a persistent sink writable, bounded, and free of sensitive payloads? |

I/O thread count is not worker execution concurrency. Increasing `--threads` does not run application functions inside the daemon. Worker parallelism is controlled by your worker processes, application event loops and resource budgets.

## Queue admission control

Use application admission limits first: bound request payload, per-tenant rate, in-flight submissions and backlog age. Native `maxqueue` is an additional server-side guard, not a complete resource quota. The inspected admission path compares a function's total job count with the selected priority threshold. Do not describe three configured thresholds as three independent physical queues with independently reserved memory.

Treat administrative queue-limit changes as mutations. Capture the current policy, obtain approval, apply to each intended independent server, and verify behavior by an isolated saturation test. Do not assume runtime administrative settings persist across restart unless tested or reapplied by configuration management.

## Timeouts are separate budgets

Maintain a table for DNS/connect, TLS handshake, socket inactivity, foreground end-to-end wait, worker registration timeout, business deadline, downstream timeout and supervisor kill grace. Record units explicitly. The CLI `-t` is milliseconds; other bindings have different interfaces. A timeout response must not be translated automatically into “the work never happened.”

Prefer a job budget greater than bounded downstream work plus reporting overhead. A process-kill grace must account for in-flight work, while the application still tolerates abrupt loss. Keepalive detects some dead connections; it neither guarantees a business deadline nor prevents duplicate execution.

## Configuration rollout

Change one policy class at a time. Validate arguments using the binary's supported mechanism, start a disposable instance with the intended flags, inspect its listener and logs, and record a rollback. With a persistent queue, a restart plan must include storage replay time and producers' behavior during the outage. Never use a configuration typo as an implicit migration strategy.
