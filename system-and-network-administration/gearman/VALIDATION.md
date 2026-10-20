# Validation report

**Snapshot:** 2026-10-14. **Package:** gearman 1.0.0.
**Server source baseline:** gearmand 2.1.0, tag commit
`516ffac9376a533413a748eef9295808f1bf319a`.

## Executed checks

| Layer | Result | What this establishes |
|---|---|---|
| Offline regression suite | **85 passed; 0 failed; 0 skipped** | Actual Python protocol/domain/worker/tool behavior under controlled fixtures |
| Cross-language domain fixtures | Passed within the offline suite | Perl/PHP success values, selected type boundaries and rejection cases agree with the specified fixtures |
| Perl syntax | 4 files passed | Syntax/load of bundled domain module; not installed Gearman binding behavior |
| PHP syntax | 4 files passed | Syntax; not extension/runtime interoperability |
| JSON Schemas | Draft 2020-12 metaschema checks passed | Both schema documents are structurally valid; sample request validates |
| YAML assets and skill frontmatter | Parsed successfully | YAML syntax only, not Kubernetes/Compose/systemd runtime acceptance |
| Local tool inventory | Completed | gearmand, libgearman pkg-config and Docker unavailable here |
| Live runner default | Plan-only gate passed | No daemon installation/start without explicit execution |
| Live runner execution attempt | Exit 2, **not executed** | Missing daemon is reported as a failure to run, not a passing integration test |
| Package structure and integrity | Checked by `scripts/verify.py` during packaging | Required files, local links, Python/JSON syntax and SHA-256 file inventory |

The suite completed in 0.717 seconds in this environment. This is a test-run duration,
**not** a Gearman throughput measurement. The 20 agent evaluation prompts are rubrics,
not 20 additional executed model evaluations.

## What the offline suite actually exercises

Framing and network-byte order; binary NULs; fragmented/coalesced frames; bad magic;
truncated headers/bodies; byte/deadline limits; TLS configuration guards (mocked context,
not live TLS); ECHO/option handshakes; foreground/background distinctions; terminal failure
and exception handling; intermediate events; mismatched handles; ambiguous disconnects
without automatic resend; read-only administrative allowlists and response parsing;
worker sleep/wakeup/stop and single terminal decisions; strict JSON types/limits;
request fingerprints; transaction rollback; concurrent repeated requests; reopening a
local result database; cross-language domain CLI fixtures; helper execution/ownership gates.

The SQLite example proves only that its **local counter and result** commit atomically
and deduplicate within that transaction design. It does not prove exactly-once remote
effects, distributed fencing, native Gearmand persistence or backend replication.

## Source review, not execution

The current release baseline and behavior changes were checked against upstream release
notes and selected tagged server code. Inspected paths cover active unique lookup,
queue admission/addition, interruption/requeue thresholds, terminal handlers,
worker registration/sleep/grab behavior, epoch wakeup and the queue interface. The source
register identifies exact scope, tag and important inspected functions/ranges.

The classic Perl worker callback path was inspected on upstream's default branch and is
not silently equated with every CPAN distribution version. Full EV::Gearman page retrieval
and the upstream systemd manual fetch were unsuccessful; corresponding limits are recorded.

## Not executed / outstanding acceptance gates

No real gearmand daemon or libgearman was installed in the execution environment. Network
and archive/dependency retrieval limitations prevented installing/building a matching copy.
Consequently the following **remain unverified locally**:

- Native Gearmand smoke/replay/interruption tests and every native persistence backend.
- C compilation/linking and C, Perl Gearman/XS, or PHP Gearman-extension integration.
- Live TLS/mTLS, wrong-CA/hostname/expiry handshake tests and native TLS fail-closed behavior.
- Docker image build/runtime, Compose runtime, Kubernetes schema/apply/runtime and systemd unit execution.
- Multi-server failover/fencing, production recovery/load benchmarks, upstream sanitizer/regression suites,
  and actual model runs against the agent rubrics.

The isolated runner is provided for the first group of smoke tests; its implementation
has safety-gate tests but its real-daemon execution remains untested. Treat examples and
deployment assets as reviewable starting points, not production-certified artifacts.

## Reproduce

From the package root:

```sh
python3 -B scripts/verify.py
python3 -B -m unittest discover -s tests -v
python3 -B scripts/gearman_ops.py inventory
python3 -B scripts/run_lab.py
# Deliberate isolated integration only, after installing a suitable daemon:
python3 -B scripts/run_lab.py --execute
python3 -B scripts/run_lab.py --execute --persistence
```

The live runner requires Linux `/proc` listener-ownership inspection and an installed
daemon. It never installs dependencies, and it has no option to target a pre-existing
remote service. Its temporary daemon and child adapters are stopped by owned process
handles. All deployments and service changes remain explicit operator actions.

## Recorded evidence

[Machine-readable results](validation/results.json) · [Offline test log](validation/offline-tests.txt) ·
[Language syntax results](validation/language-syntax.json) · [Asset static checks](validation/asset-static-checks.json) ·
[Tool inventory](validation/local-inventory.json) · [Lab plan](validation/lab-plan.json) ·
[Unavailable live attempt](validation/live-integration-attempt.json) · [Source register](references/sources.md).

Environment: Python 3.13.5, Perl v5.40.1, PHP 8.4.24,
Debian GNU/Linux 13. Hash validation records integrity of the distributed bytes, not their
semantic correctness; SHA-256 here is not a signed upstream provenance attestation.
