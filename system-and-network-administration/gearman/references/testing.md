# Testing strategy and acceptance matrix

Read [VALIDATION.md](../VALIDATION.md) for what actually ran. A test plan is not execution evidence. The package separates source inspection, static checks, offline socket/contract tests and real-daemon integration.

## Offline suite

Run `python3 -B -m unittest discover -s tests -v` from the skill root. The tests use controlled local socket pairs and temporary SQLite files; they do not contact an existing Gearman server. They exercise framing, fragmentation, EOF, limits, deadlines, terminal state, bounded events, administrative parsing, worker decisions, strict request contracts and transaction-local idempotency. Cross-language subprocess tests use installed Perl/PHP runtimes but do not load unavailable Gearman bindings.

Run `python3 -B scripts/verify.py` to check package structure, relative Markdown links, JSON/Python syntax and the recorded file hashes. It does not install dependencies or rewrite the manifest. After intentional edits, regenerate hashes explicitly with `--write-manifest` and rerun validation.

## Isolated live runner

`python3 -B scripts/run_lab.py` prints a plan only. Add `--execute` to start a locally installed gearmand on a selected loopback port with temporary state, execute the declared smoke scenarios and stop only processes it created. Add `--persistence` to request SQLite replay testing when the binary supports it. Read its plan and logs first. Missing dependencies fail explicitly rather than becoming a passing skipped integration test.

The runner is a bounded smoke harness, not a complete production certification. It does not test every backend, multi-server failover, native bindings, live TLS, container deployment or Kubernetes behavior. Its selected free port can race with another process before bind; a startup failure aborts rather than probing an unrelated server.

## Production failure matrix

| Injection | Observe separately |
|---|---|
| Producer disconnect before/after acknowledgement | Acceptance uncertainty, deduplication policy, reconciliation |
| Worker exits before effect | Assignment/requeue count and retry threshold |
| Worker exits after effect before completion | Duplicate assignment versus committed effect count |
| WORK_FAIL / WORK_EXCEPTION | Terminal behavior and persistent cleanup |
| Server restart with queued/in-flight jobs | Replay, lost foreground work, duplicate effects |
| Backend unavailable or commit reply lost | Admission response, blocking limits, recovery |
| Queue/payload/result limits | Explicit rejection, memory cap, no uncontrolled retry loop |
| Mixed priority/functions | Starvation and version-specific ordering |
| Delayed job, restart and idle workers | Scheduling time, wakeup and replay |
| TLS negative cases | Wrong CA/name/expiry, missing client cert, plaintext fallback |
| Rolling worker/schema upgrade | Compatibility with old queued payloads |
| Multi-server loss/recovery | Stranded requests, origin-aware status and dedup across replay |

Record exact versions/options, expected invariants, assignment count, transport terminal count, committed business effects and artifacts. Do not assert exactly-once from observing one successful run. Use deliberately stable request IDs to reveal duplicate execution rather than hiding it behind newly generated IDs.
