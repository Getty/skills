---
name: gearman
description: "Use when building, running or debugging Gearman — gearmand, persistent queues, clients and workers in Perl, PHP, C or Python, the binary or admin protocol, retries, idempotency, stuck or lost jobs, scaling, deployment, upgrades."
---
# Gearman engineering and operations

## Working contract

Treat Gearman as a work-distribution system, not a durable workflow engine with an implied result database. Cover the client, job server, worker, application state, and deployment boundary appropriate to the task. This skill is standalone; its README is optional. All required knowledge is here or in the linked references.

**Evidence baseline:** reviewed 2026-10-14; C/C++ gearmand tag **2.1.0**, commit `516ffac9376a533413a748eef9295808f1bf319a`. The baseline is source-reviewed, **not locally daemon-tested**. Inspect installed versions and build capabilities before applying commands. Never transfer options or guarantees between the C server, Perl server, library bindings, and test servers.

## Workflow

1. **Identify the system.** Record server implementation/version, linked library and binding versions, topology, persistence backend, transport security, functions, workload sizes, concurrency, and failure budget. Run only read-only inventory/probes without change authorization.
2. **State the contract.** Define foreground versus background, application request identity, payload schema, deadlines, result ownership, retry owner, duplicate handling, and side-effect boundaries.
3. **Read selectively.** Use the routing table below; consult the full [reference index](references/INDEX.md) only when the request spans several areas.
4. **Implement the smallest correct path.** Keep transport adapters separate from business logic. Validate bytes and schemas. Bound memory, I/O waits, child processes, concurrency, and retries. Return exactly one terminal response per assignment.
5. **Exercise failure boundaries.** Include ambiguous submit outcomes, worker disconnect after a side effect, explicit failure, restart/replay, invalid input, and rolling-version overlap. Use an isolated daemon, never a production queue, for destructive tests.
6. **Deliver evidence.** Separate observed facts, source-derived behavior, design recommendations, and untested assumptions. Report commands, versions, artifacts, results, limitations, rollback, and remaining acceptance gates.

## Reference routing

| Task | Read |
|---|---|
| Learn the model; choose boundaries | [Foundations](references/foundations.md), [patterns](references/application-patterns.md) |
| Install, build, inventory, migrate versions | [Compatibility](references/version-compatibility.md), [installation](references/installation-build.md), [upgrades](references/upgrades-recovery.md) |
| Run and configure the server | [Configuration](references/server-configuration.md), [systemd/containers](references/systemd-containers.md), [Kubernetes](references/kubernetes.md) |
| Make background queues recoverable | [Persistence model](references/persistence-model.md), [backends](references/persistence-backends.md) |
| Scale or design failover | [Topology](references/topology-failover.md), [capacity](references/performance-capacity.md) |
| Secure connections and workers | [Security/TLS](references/security-tls.md) |
| Write a client or worker | [Client design](references/client-design.md), [worker design](references/worker-design.md), [contracts](references/job-contracts.md) |
| Retries, effects, outcomes, cancellation | [Reliability](references/reliability.md), [outbox/results](references/outbox-results.md) |
| Perl | [Classic binding](references/perl-classic.md), [XS and asynchronous bindings](references/perl-xs-async.md) |
| C/C++, PHP, Python, other runtimes | [libgearman](references/c-libgearman.md), [PHP](references/php.md), [Python/other](references/python-other.md) |
| Implement or debug the protocol | [Framing](references/protocol-framing.md), [client state machine](references/protocol-client.md), [worker state machine](references/protocol-worker.md) |
| Priorities, delayed jobs, fairness | [Scheduling](references/scheduling.md) |
| Operate, monitor, investigate incidents | [Admin/observability](references/observability-admin.md), [troubleshooting](references/troubleshooting.md) |
| Modify the server or add a backend | [Internals](references/server-internals.md), [extensions](references/server-extensions.md) |
| Validate behavior or this package | [Testing](references/testing.md), [validation report](VALIDATION.md), [sources](references/sources.md) |

## Non-negotiable distinctions

- Background acceptance is not completion; an unknown handle is not proof of success. Persistent job storage is not a completed-result store or server-to-server replication.
- Coalescing by function/unique key is not durable business idempotency. Keep request identity separate from delivery identity; reconcile ambiguous submissions before resubmitting side-effecting work.
- `WORK_FAIL` is terminal on the reviewed C server. Disconnect/requeue is a different path. Never invent built-in exponential retry, dead-letter queues, workflow dependencies, leases, or exactly-once execution.
- In 2.1.0, `--job-retries=0` changed meaning. Read the compatibility reference; do not copy old retry defaults, assume positive values mean N additional attempts, or silently change scheduling during upgrades.
- A client timeout does not kill the worker. A namespace is not authorization. Restrict access to the job/admin port and test certificate rejection, not just successful TLS handshakes.
- Do not delete backend rows, cancel jobs, drop functions, restart servers, change queue limits, or run lab submissions against an existing service without authorization and an impact/rollback plan.

## Included tools

`python3 scripts/gearman_ops.py inventory` inspects local help/version output. `probe` uses binary ECHO; `admin` permits only version/status/workers. Neither submits jobs. `python3 scripts/verify.py` checks package integrity; `python3 -m unittest discover -s tests -v` runs offline tests. The [lab runner](scripts/run_lab.py) requires `--execute` to start an isolated local daemon. Examples and deployment assets are teaching/reference implementations, not a production certification.
