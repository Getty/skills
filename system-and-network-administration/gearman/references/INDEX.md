# Reference index

Start with the row matching the task. Read one or two focused chapters, then follow
cross-links only as needed. The central [SKILL.md](../SKILL.md) contains the workflow
and safety contract; do not load this entire directory for a narrow question.

## Fast routes

| Question | Initial route |
|---|---|
| “Run a production server” | Configuration → persistence → security → chosen deployment |
| “Write a Perl worker/client” | Classic or XS → worker/client design → job contracts → reliability |
| “Why did this job run twice?” | Reliability → outbox/results → troubleshooting |
| “Add a second server” | Topology/failover → capacity → recovery acceptance |
| “Implement a binding” | Framing → client/worker state machines → testing |
| “Modify gearmand or add storage” | Server internals → extensions → tagged source register |
| “Upgrade old installation” | Version compatibility → upgrades/recovery → acceptance matrix |

## Model and application decisions

- [Foundations and responsibility boundaries](foundations.md)
- [Application patterns and limits](application-patterns.md)
- [Versions, implementations, and compatibility](version-compatibility.md)
- [Job contracts, identities and schema evolution](job-contracts.md)

## Server engineering and deployment

- [Installation, builds, and reproducibility](installation-build.md)
- [Server configuration and operational policy](server-configuration.md)
- [Persistence: what is and is not recovered](persistence-model.md)
- [Persistence backends and storage-specific review](persistence-backends.md)
- [Topology, failover, and queue ownership](topology-failover.md)
- [Security, TLS, and the execution boundary](security-tls.md)
- [Supervision, systemd and containers](systemd-containers.md)
- [Kubernetes design: state, identity and execution pools](kubernetes.md)

## Client and worker programming

- [Production client design](client-design.md)
- [Production worker design](worker-design.md)
- [Classic Perl: Gearman::Client and Gearman::Worker](perl-classic.md)
- [Perl XS and event-loop alternatives](perl-xs-async.md)
- [C/C++ with libgearman](c-libgearman.md)
- [PHP extension clients and long-running workers](php.md)
- [Python and other language integrations](python-other.md)

## Protocol and daemon development

- [Binary protocol framing and parser design](protocol-framing.md)
- [Client protocol state machine](protocol-client.md)
- [Worker protocol state machine](protocol-worker.md)
- [Priorities, fairness, delayed work, and ordering](scheduling.md)
- [Gearmand internals and source navigation](server-internals.md)
- [Developing server extensions and persistence backends](server-extensions.md)

## Reliability and operations

- [Retries, duplicates, idempotency, and poison jobs](reliability.md)
- [Transactional outbox, durable outcomes, and cancellation](outbox-results.md)
- [Observability and native administration](observability-admin.md)
- [Incident-oriented troubleshooting](troubleshooting.md)
- [Capacity planning and performance investigation](performance-capacity.md)
- [Upgrades, backup, restore and recovery](upgrades-recovery.md)
- [Testing strategy and acceptance matrix](testing.md)
- [Source register and evidence policy](sources.md)

## Executable and planning material

[Example guide](../examples/README.md) · [Package validation](../VALIDATION.md) ·
[Complete file inventory](../CONTENTS.md) · [Deployment decision template](../assets/templates/deployment-plan.md) ·
[Job design template](../assets/templates/job-design.md) · [Incident record](../assets/templates/incident-runbook.md).

Runtime evidence is independent of source evidence. Unexecuted integration, TLS,
backend and deployment gates remain unverified even when all offline tests pass.
