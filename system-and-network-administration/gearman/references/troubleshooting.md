# Incident-oriented troubleshooting

Evidence anchors: [G3–G7, S1, S2](sources.md). Procedures are engineering guidance. Start read-only; preserve request IDs and avoid replay until the effect state is understood.

| Symptom | First evidence | Likely branches / next step |
|---|---|---|
| Connection refused or TLS failure | Process/listener state, endpoint, ECHO, certificate error | Wrong bind/address, stopped process, firewall, build without TLS, trust/name mismatch |
| Waiting jobs but no work | Per-function status on every server; exact registered name | No capable worker, version/prefix mismatch, workers on another server, future epoch |
| All workers appear registered but latency rises | Running counts, execution duration, dependency waits | Registration is not idle capacity; blocked DB/API, CPU limits, saturation |
| Duplicate external effect | Stable request ID, assignment history, transaction/provider IDs | Ack loss, timeout overlap, server replay, failover resubmission, missing idempotency |
| Job vanishes without result | Terminal logs and outcome store; original server identity | WORK_FAIL/EXCEPTION, retry exhaustion, volatile restart, querying wrong server |
| Server RSS grows despite persistence | Backlog, payload sizes, result buffering, per-process memory | Durable queue still has live memory structures; no worker/admission limits |
| Restart is slow | Backend replay logs, row counts, backend latency | Large backlog, backend failure or incompatible stored representation |
| High-priority starvation or changed order | Exact server/libgearman versions and registered functions | 2.x scheduling changes, high-priority flood, dependencies on incidental ordering |
| Repeated reconnects | Close reason, TLS, keepalive, proxy timeouts, server/resource logs | Idle connection policy, bad frame, worker timeout, library lifecycle bug |

## Collect a minimum evidence bundle

Capture UTC interval, deployment revision, server/library versions and redacted options; topology and origin endpoint; relevant function names; read-only snapshots; representative request IDs; producer and worker return codes; sanitized server/backend logs; resource and latency metrics. Separate a failing path from a successful control request.

Use `scripts/gearman_ops.py inventory` for local binary evidence and the explicit endpoint modes for remote read-only checks. Do not upload complete workload dumps, credentials or database snapshots by default. A packet capture can contain both secrets and administrative traffic.

## Unknown outcome procedure

A client timeout after submission is not proof the server rejected the job. Consult the application operation ledger by request ID. If it is committed, return the existing outcome. If it is pending, investigate ownership/deadline and whether a live attempt can still finish. Republish only under a policy that tolerates duplication and rejects conflicting payloads. Record every reconciliation action.

For a background handle that is now unknown, inspect the ledger rather than declaring success. For a crash after an external effect, query the external provider using its idempotency key or transaction identifier before repeating the request.

## Controlled recovery

When safe, stop admission before disturbing execution. Drain compatible workers where possible. For a persistently failing job, quarantine its logical operation with a bounded retry policy; do not kill the entire queue. For a backend outage, distinguish rejected new writes from already accepted jobs and potential replay duplicates. A forced restart may increase uncertainty; describe that tradeoff before executing it.

Keep a clear record of actions that changed state. End the incident with a test reproducing the failure, an outcome reconciliation result, and a verified prevention change—not only a green process-health check.
