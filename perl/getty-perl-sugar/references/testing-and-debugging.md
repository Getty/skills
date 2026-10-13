# Testing and debugging declarative sugar

**Read when:** verifying a new DSL, reviewing a refactor, or finding missing steps.

## Test boundaries independently

Registration tests should prove local validation, stable local order, provenance,
correct ownership, and no body invocation. Test malformed argument lists before a
hash conversion can hide duplicate or missing options. Ensure rejected declarations
do not leave partially committed metadata.

Composition tests should cover two classes consuming the same role, nested roles,
diamond reuse, late `with`, parent-class declarations, inherited roles, duplicate
keys, explicit overrides if supported, and the exact ordering policy. Distinguish
core tests of an explicit owner list from real Moose role traversal.

Planner tests should cover unknown prerequisites, cycles, phase inversions, stable
ready-order ties, disabled prerequisites, and opaque callbacks in manifests.
Bind conditions once and verify that planning failures precede side effects.

Execution tests should cover empty/false-valued successes, missing results, invalid
result types, exceptions, explicit retries, per-instance isolation, observer failures,
and cancellation where supported. Persistence tests should inject crashes around
effect/checkpoint boundaries, not just round-trip JSON successfully.

## Caller debugging procedure

Build a tiny reproduction with a direct export, an ordinary wrapper, and a `goto &`
wrapper. Record `caller` at the public declaration boundary, not halfway through
registration. For a `with_meta` implementation, record `$meta->name` instead.
Inspect whether the wrong bucket already contains data before investigating the
planner. Real Perl call-frame tests are included in `t/10-caller.t`.

If a role disappears, check whether it was loaded and composed, whether lookup
includes its owner, whether a cache was built before composition, and whether the
step was filtered by phase or predicate policy. Do not fix a missing owner by
copying that role's data into every class during import.

If a class can call `step` as a method, inspect namespace cleanup. If cleanup removes
real methods, inspect the exact exporter or cleaning pragma and its timing.
If inherited steps disappear, inspect parent-class buckets separately from inherited
role discovery.

## Determinism and regression checks

Run ordering tests in fresh processes with several `PERL_HASH_SEED` values and
`PERL_PERTURB_KEYS` settings. Snapshot public manifests, not live closures or memory
addresses. Compare the old and new behavior on representative real consumers before
changing a project's default order.

A refactor should preserve stable step keys and output schemas unless migration is
intentional. For changed behavior, add a regression test that demonstrates the old
failure and the new policy. Do not conflate a syntax-only test with an integration
or crash-safety test.

## Running the bundle

From the package root, `python scripts/verify.py` checks package links and manifest
hashes, runs Perl tests, runs the Python schema tests, and checks deterministic output.
Use `python scripts/verify.py --require-integrations` in a prepared environment to
fail rather than skip when Moose/Future/IO::Async are missing. `--require-schema`
requires the Python JSON Schema validator too.

Read [VALIDATION.md](../VALIDATION.md). A test marked `skip_all` is not executed;
a green overall `prove` status can include skipped integrations. The bundle's
validation report separates these facts explicitly.
