---
name: getty-perl-sugar
description: Use when designing, refactoring or reviewing declarative Perl DSL sugar — Moose::Exporter keywords such as `step`, `with_meta` or `caller` ownership, metadata registries, role-shared declarations, a shared runner or plan.
---

# Getty Perl Sugar

Turn repeated domain structure into declarations; keep execution policy in one place.
This is an architecture and implementation skill. The bundled `Example::Sugar` shows
the mechanism; it is not a module to depend on, and project code follows
`getty-perl-core` and `getty-perl-moose`.

## Start here

Read [architecture](references/architecture.md) and the relevant entries in the
[reference index](references/index.md). Read only the references needed for the task.
For a new DSL, read `Sugar.pm`, `Sugar/RoleDSL.pm` and `Sugar/Owners.pm` under
`examples/reference/lib/Example/` first: class entry point, role entry point, and
owner collection across parents and roles.
For an existing caller-based DSL, start with the
[correction and adoption map](references/corrections-and-adoption.md).

Inspect the repository's actual exporters, consumers, role composition, Perl/Moose
versions, and tests before changing its public syntax. A design note about the
project is not a substitute for source inspection.

## Working procedure

1. Identify repeated orchestration and the smallest useful domain vocabulary. Keep a
   plain function or method when there is no meaningful metadata or reuse benefit.
2. Specify descriptors first: stable keys, labels, owners, bodies, conditions, phases,
   prerequisites, result shapes, and versioning. State what is inspectable and opaque.
3. Separate declaration registration, plan compilation/binding, and execution. Validate
   local shape while registering; validate cross-owner conflicts and dependencies after
   composition; validate results before recording success.
4. Preserve existing syntax. For new Moose sugar, prefer `with_meta` and pass `$meta->name`
   into a shared registration backend. For caller-sensitive `as_is` exports, capture
   the owner at the boundary or use a transparent `goto &target` shim.
5. Define composition and scheduling independently. Include inherited class declarations,
   deduplicate role owners, reject merged key collisions, and establish deterministic
   phase/dependency ordering. Do not treat `calculate_all_roles` as a workflow-order API.
6. Add phases, prerequisites, conditions, parallelism, persistence, form metadata, or
   tool schemas only when needed. Without them the minimum is a registry, owner
   collection, and a merged-key check before the first body runs — no planner.
   Each addition needs an explicit contract, negative tests, and observability.
7. Run the relevant tests and report exactly what passed, failed, or was skipped.
   Never describe a dependency-gated test as an executed integration test.

## Non-negotiable boundaries

Declaration keywords register and validate; they do not perform domain I/O or run step
bodies. Loading a Perl module is nevertheless code execution, not safe data parsing.

`step` is an exported declaration function, not a generated instance method. The
runner invokes the stored body with `$self`; bodies may delegate to ordinary methods.

Keep registries separate from instance results and durable checkpoints. Never mutate a
shared role bucket while composing one consumer. Never expose live registry hashes as
public introspection data. Keep bodies and arbitrary predicates explicitly opaque.

Reject unknown options, missing coderefs, duplicate keys, unknown dependencies, cycles,
phase inversions, and incompatible active prerequisites before side effects begin.
Do not `eval` predicate strings. Do not infer semantic equality of separate callbacks.

A Future is not an execution pool. A cached result is not an exactly-once guarantee.
An immutable Moose class is not a frozen external registry. Schema metadata is not
authorization, and UI hints are not server-side validation.

## Example shape

```perl
use Example::Sugar;
step 'Collect inputs' => inputs => sub { return { count => 3 } };
step 'Summarize' => summary => sub {
  return { count => $_[0]->result('inputs')->{count} };
}, phase => 'render', requires => ['inputs'];
no Example::Sugar;
__PACKAGE__->meta->make_immutable;
```

This syntax belongs to the bundled reference implementation, not to any existing
project's API. See [the implementation guide](examples/reference/README.md).

## Deliverable contract

Provide the domain contract, chosen module boundaries, public declaration example,
ordering/conflict policy, focused tests, and compatibility notes. Separate proposed
production extensions from implemented behavior.

`scripts/verify.py` checks this skill package and its reference implementation, not
your work: execute it after editing the skill. [VALIDATION.md](VALIDATION.md) records
what it covers.
