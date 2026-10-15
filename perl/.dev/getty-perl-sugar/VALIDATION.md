# Validation record

Review and execution date: **2026-10-13**.

## Result summary

| Scope | Actual result |
|---|---|
| Core Perl suite | **130 assertions passed** across 6 test files |
| Moose integration (`t/70-moose.t`) | **13 assertions passed** against real Moose |
| Future contract (`t/80-future.t`) | **5 assertions passed** against real Future |
| Real IO::Async loop (`t/90-io-async.t`) | **3 assertions passed** on a real loop |
| Python JSON Schema tests | **5 test methods passed**, including 8 invalid-payload subcases |
| Determinism | Planner tests and the core demo passed under 4 hash-seed configurations |
| Strict integration gate | Ran with `--require-integrations --require-schema`: nothing skipped |
| Agent evaluations | 12 manual cases included; no independent-agent evaluation executed |
| Production extensions | Not implemented or integration-tested; see scope below |

The Perl harness ran all 9 test files, 151 assertions, with no skip. Where a
dependency is missing the three integration files skip instead, and an overall PASS
then does not mean the integrations ran. The four seeded planner runs repeat existing
assertions; they are not counted as additional unique test coverage.

## Runtime environment

| Component | Executed version |
|---|---|
| Perl | 5.40.1, x86_64-linux-gnu-thread-multi |
| Test::More | 1.302222 |
| JSON::PP | 4.16 |
| Python | 3.13.5 |
| Python jsonschema | 4.26.0 |
| JSON Schema dialect | Draft 2020-12 |
| Moose | 2.4000 |
| Future | 0.52 |
| IO::Async | 0.805 |

No dependency was replaced by a fake implementation. These are the versions of one
machine, not a tested version range. Primary documentation was checked separately;
that is not execution evidence for other library versions.

## What the executed tests establish

Registration rejects duplicate keys, unknown/repeated/odd options, missing bodies,
invalid dependencies and predicates, and post-seal changes. Rejected declarations
do not commit entries. Registration and lookup protect nested metadata from mutation.

Real Perl call-frame tests distinguish direct calls, ordinary wrappers, and transparent
`goto &` forwarding. These do not verify Moose::Exporter behavior.

The Moose test verifies `with_meta` ownership for a class and a role, automatic
runner-role application, cleanup of both DSL keywords, per-instance result isolation,
a `with` placed after the declarations, and inherited parent-class declarations.
The Future and IO::Async tests verify aggregation and real timer overlap on their
own; the executor does not use either.

The planner merges explicit owners, deduplicates owner visits, rejects merged key
conflicts and invalid DAGs, obeys phase/dependency order, binds conditions once, rejects
active-to-disabled prerequisites, and emits serializable opaque-callback manifests.

The synchronous executor validates result shapes, retains legitimate empty and
false-valued results, records failures, supports explicit same-instance reruns,
returns copies, rejects reentrant calls, and rejects reuse with another live subject.
Its tests do not prove durable resume or safe repetition of arbitrary side effects.

Schema tests cover pure construction, deep non-mutation, correct JSON booleans,
bounds, required fields, additional properties, nullable enums, null versus omission,
integer versus fractional input, and invalid payloads with a real validator.

## Reproduction and evidence files

Run from the package root:

```sh
python scripts/verify.py
```

The verifier checks local documentation links, fenced blocks, skill metadata,
reference count, file inventory and hashes, Perl tests, Python tests, and seed-stable
core planning. It never installs dependencies or accesses external services.

To fail instead of skipping when Moose, Future, IO::Async or the Python `jsonschema`
package is missing — the mode this record was produced in:

```sh
python scripts/verify.py --require-integrations --require-schema
```

[Verification transcript](tests/verification.txt),
[strict-gate failure recorded on a machine without Moose](tests/strict-gate.txt),
[executed core demo output](tests/core-demo.json), and
[generated tool-parameter schema](tests/generated-schema.json).

## Not established

No production concurrency scheduler, timeout/cancellation adapter, persistent
checkpoint store, exactly-once side-effect protocol, multi-worker coordination,
form renderer, localization integration, validation-cache promotion, or provider-
specific LLM tool dispatcher is implemented by the teaching executor. These are
separately labeled design references. No load or memory benchmark was executed.

The production DSL the pattern was distilled from was not audited. No API
compatibility with it, or with any other existing DSL, is certified.

## Maintenance

After an intentional edit, execute `python scripts/verify.py --update-manifest`: it
rewrites MANIFEST.json from the files on disk and then verifies. Without it the
verifier correctly reports modified file hashes. Re-run actual integrations on the
project's pinned dependency versions before adopting the Moose adapter or async
examples. Update this record with real results; never remove a skip notice without
executing the corresponding check.
