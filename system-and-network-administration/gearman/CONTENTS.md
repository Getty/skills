# Complete package inventory

**89 files** including the manifest; **34 reference Markdown files**
(32 focused chapters, one source register and one index). The central SKILL.md has
53 lines; the reference directory contains approximately 16,224 words.
Counts describe this artifact, not a coverage guarantee for every third-party binding.

## Directory roles

| Area | Role |
|---|---|
| Root | Agent entry point, optional human README, inventory, validation, integrity, license/notice |
| references/ | Selectively loaded technical knowledge and evidence register |
| scripts/ | Bounded protocol lab, read-only operations, isolated live runner, integrity tool |
| examples/ | Python, classic Perl, PHP and C implementations plus their limitations |
| assets/ | Job schemas, systemd/Compose/Kubernetes examples and engineering templates |
| tests/ | 85 executed offline tests plus 20 unexecuted model-evaluation rubrics |
| validation/ | Actual test, syntax, inventory and unavailable-integration evidence |

## Files

### Root

- [.dockerignore](.dockerignore)
- [.gitignore](.gitignore)
- [CONTENTS.md](CONTENTS.md) — Package inventory
- [LICENSE](LICENSE)
- [NOTICE.md](NOTICE.md) — Scope and attribution
- [README.md](README.md) — Gearman engineering skill
- [SKILL.md](SKILL.md) — Gearman engineering and operations
- [VALIDATION.md](VALIDATION.md) — Validation report
- [MANIFEST.json](MANIFEST.json)

### references

- [references/INDEX.md](references/INDEX.md) — Reference index
- [references/application-patterns.md](references/application-patterns.md) — Application patterns and limits
- [references/c-libgearman.md](references/c-libgearman.md) — C/C++ with libgearman
- [references/client-design.md](references/client-design.md) — Production client design
- [references/foundations.md](references/foundations.md) — Foundations and responsibility boundaries
- [references/installation-build.md](references/installation-build.md) — Installation, builds, and reproducibility
- [references/job-contracts.md](references/job-contracts.md) — Job contracts, identities and schema evolution
- [references/kubernetes.md](references/kubernetes.md) — Kubernetes design: state, identity and execution pools
- [references/observability-admin.md](references/observability-admin.md) — Observability and native administration
- [references/outbox-results.md](references/outbox-results.md) — Transactional outbox, durable outcomes, and cancellation
- [references/performance-capacity.md](references/performance-capacity.md) — Capacity planning and performance investigation
- [references/perl-classic.md](references/perl-classic.md) — Classic Perl: Gearman::Client and Gearman::Worker
- [references/perl-xs-async.md](references/perl-xs-async.md) — Perl XS and event-loop alternatives
- [references/persistence-backends.md](references/persistence-backends.md) — Persistence backends and storage-specific review
- [references/persistence-model.md](references/persistence-model.md) — Persistence: what is and is not recovered
- [references/php.md](references/php.md) — PHP extension clients and long-running workers
- [references/protocol-client.md](references/protocol-client.md) — Client protocol state machine
- [references/protocol-framing.md](references/protocol-framing.md) — Binary protocol framing and parser design
- [references/protocol-worker.md](references/protocol-worker.md) — Worker protocol state machine
- [references/python-other.md](references/python-other.md) — Python and other language integrations
- [references/reliability.md](references/reliability.md) — Retries, duplicates, idempotency, and poison jobs
- [references/scheduling.md](references/scheduling.md) — Priorities, fairness, delayed work, and ordering
- [references/security-tls.md](references/security-tls.md) — Security, TLS, and the execution boundary
- [references/server-configuration.md](references/server-configuration.md) — Server configuration and operational policy
- [references/server-extensions.md](references/server-extensions.md) — Developing server extensions and persistence backends
- [references/server-internals.md](references/server-internals.md) — Gearmand internals and source navigation
- [references/sources.md](references/sources.md) — Source register and evidence policy
- [references/systemd-containers.md](references/systemd-containers.md) — Supervision, systemd and containers
- [references/testing.md](references/testing.md) — Testing strategy and acceptance matrix
- [references/topology-failover.md](references/topology-failover.md) — Topology, failover, and queue ownership
- [references/troubleshooting.md](references/troubleshooting.md) — Incident-oriented troubleshooting
- [references/upgrades-recovery.md](references/upgrades-recovery.md) — Upgrades, backup, restore and recovery
- [references/version-compatibility.md](references/version-compatibility.md) — Versions, implementations, and compatibility
- [references/worker-design.md](references/worker-design.md) — Production worker design

### scripts

- [scripts/gearman_ops.py](scripts/gearman_ops.py)
- [scripts/gearman_wire.py](scripts/gearman_wire.py)
- [scripts/run_lab.py](scripts/run_lab.py)
- [scripts/verify.py](scripts/verify.py)

### examples

- [examples/README.md](examples/README.md) — Executable examples and integration guide
- [examples/c/client.c](examples/c/client.c)
- [examples/c/worker.c](examples/c/worker.c)
- [examples/perl/client.pl](examples/perl/client.pl)
- [examples/perl/contract_cli.pl](examples/perl/contract_cli.pl)
- [examples/perl/lib/GearmanSkill/Contract.pm](examples/perl/lib/GearmanSkill/Contract.pm)
- [examples/perl/worker.pl](examples/perl/worker.pl)
- [examples/php/client.php](examples/php/client.php)
- [examples/php/contract.php](examples/php/contract.php)
- [examples/php/contract_cli.php](examples/php/contract_cli.php)
- [examples/php/worker.php](examples/php/worker.php)
- [examples/python/client.py](examples/python/client.py)
- [examples/python/contract.py](examples/python/contract.py)
- [examples/python/result_store.py](examples/python/result_store.py)
- [examples/python/worker.py](examples/python/worker.py)

### assets

- [assets/containers/Dockerfile](assets/containers/Dockerfile)
- [assets/containers/compose.yaml](assets/containers/compose.yaml)
- [assets/contracts/job-request.schema.json](assets/contracts/job-request.schema.json)
- [assets/contracts/job-result.schema.json](assets/contracts/job-result.schema.json)
- [assets/contracts/sample-request.json](assets/contracts/sample-request.json)
- [assets/kubernetes/network-policy.yaml](assets/kubernetes/network-policy.yaml)
- [assets/kubernetes/server.yaml](assets/kubernetes/server.yaml)
- [assets/kubernetes/worker.yaml](assets/kubernetes/worker.yaml)
- [assets/systemd/gearman-skill-server.service](assets/systemd/gearman-skill-server.service)
- [assets/systemd/gearman-skill-worker.service](assets/systemd/gearman-skill-worker.service)
- [assets/templates/deployment-plan.md](assets/templates/deployment-plan.md) — Deployment decision record
- [assets/templates/incident-runbook.md](assets/templates/incident-runbook.md) — Incident record
- [assets/templates/job-design.md](assets/templates/job-design.md) — Job contract design
- [assets/templates/library-compatibility-matrix.csv](assets/templates/library-compatibility-matrix.csv)
- [assets/templates/upgrade-checklist.md](assets/templates/upgrade-checklist.md) — Upgrade / recovery gate

### tests

- [tests/evaluation-cases.json](tests/evaluation-cases.json)
- [tests/test_contract.py](tests/test_contract.py)
- [tests/test_tools.py](tests/test_tools.py)
- [tests/test_wire.py](tests/test_wire.py)
- [tests/test_worker.py](tests/test_worker.py)

### validation

- [validation/asset-static-checks.json](validation/asset-static-checks.json)
- [validation/lab-plan.json](validation/lab-plan.json)
- [validation/language-syntax.json](validation/language-syntax.json)
- [validation/live-integration-attempt.json](validation/live-integration-attempt.json)
- [validation/local-inventory.json](validation/local-inventory.json)
- [validation/offline-tests.txt](validation/offline-tests.txt)
- [validation/results.json](validation/results.json)

