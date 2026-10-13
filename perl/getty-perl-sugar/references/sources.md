# Sources and evidence boundaries

Documentation review date: **2026-10-13**. These are primary documentation sources.
Links to live documentation can change and may resolve to different cached releases.
They do not establish a tested dependency-version matrix; the versions actually
executed are recorded in [VALIDATION.md](../VALIDATION.md).

Architectural policies, original examples, threat models, and proposed production
extensions are this package's engineering design, not copied upstream guarantees.
Source references support the corresponding library/language facts.

<a id="s01"></a>

## S01: Moose::Exporter

[Primary documentation](https://metacpan.org/pod/Moose::Exporter)

Checked scope: Exporter modes, initialization hooks, target metadata, and cleanup caveats.

<a id="s02"></a>

## S02: Perl caller, version 5.40.1

[Primary documentation](https://perldoc.perl.org/5.40.1/functions/caller)

Checked scope: Caller package and call-frame behavior; version matches the local Perl runtime.

<a id="s03"></a>

## S03: Perl goto

[Primary documentation](https://perldoc.perl.org/functions/goto)

Checked scope: Tail-call replacement with goto &NAME and argument/localization consequences.

<a id="s04"></a>

## S04: Perl use

[Primary documentation](https://perldoc.perl.org/functions/use)

Checked scope: Compile-time loading and import behavior.

<a id="s05"></a>

## S05: Perl require

[Primary documentation](https://perldoc.perl.org/functions/require)

Checked scope: Loading and executing module code; module-loading semantics.

<a id="s06"></a>

## S06: Moose::Meta::Class

[Primary documentation](https://metacpan.org/pod/Moose::Meta::Class)

Checked scope: Role discovery versus inherited-role discovery; no workflow ordering guarantee.

<a id="s07"></a>

## S07: Moose cookbook: Moose-style sugar

[Primary documentation](https://metacpan.org/pod/Moose::Cookbook::Extending::Mooseish_MooseSugar)

Checked scope: Metadata-bound sugar as an extension pattern.

<a id="s08"></a>

## S08: namespace::autoclean

[Primary documentation](https://metacpan.org/pod/namespace::autoclean)

Checked scope: Removing imported functions from method namespaces.

<a id="s09"></a>

## S09: Moose best practices

[Primary documentation](https://metacpan.org/pod/Moose::Manual::BestPractices)

Checked scope: Namespace hygiene and class immutability are separate operations.

<a id="s10"></a>

## S10: Class::MOP::Class

[Primary documentation](https://metacpan.org/pod/Class::MOP::Class)

Checked scope: linearized_isa and class metadata traversal.

<a id="s11"></a>

## S11: Moose roles manual

[Primary documentation](https://metacpan.org/pod/Moose::Manual::Roles)

Checked scope: Role composition, requirements, aliases, exclusions, and method conflicts.

<a id="s12"></a>

## S12: Future

[Primary documentation](https://metacpan.org/pod/Future)

Checked scope: needs_all, wait_all, result ordering, cancellation, and reference lifetime.

<a id="s13"></a>

## S13: IO::Async::Loop

[Primary documentation](https://metacpan.org/pod/IO::Async::Loop)

Checked scope: Loop-bound Futures, timers, and waiting at the outer execution boundary.

<a id="s14"></a>

## S14: Moose cookbook: attribute traits

[Primary documentation](https://metacpan.org/dist/Moose/view/lib/Moose/Cookbook/Meta/Labeled_AttributeTrait.pod)

Checked scope: Attaching labels through attribute metaclass traits.

<a id="s15"></a>

## S15: JSON Schema: objects

[Primary documentation](https://json-schema.org/understanding-json-schema/reference/object)

Checked scope: Properties, required fields, and additional properties.

<a id="s16"></a>

## S16: JSON Schema: types

[Primary documentation](https://json-schema.org/understanding-json-schema/reference/type)

Checked scope: Type constraints, including null and boolean distinctions.

<a id="s17"></a>

## S17: JSON Schema: combinations

[Primary documentation](https://json-schema.org/understanding-json-schema/reference/combining)

Checked scope: anyOf union semantics underlying the nullable helper.

<a id="s18"></a>

## S18: DBIO::Candy, release 0.900000

[Primary documentation](https://metacpan.org/release/GETTY/DBIO-0.900000/view/lib/DBIO/Candy.pm)

Checked scope: Public primary documentation for the metadata-sugar analogy.

<a id="s19"></a>

## S19: Locale::TextDomain

[Primary documentation](https://metacpan.org/pod/Locale::TextDomain)

Checked scope: Deferred extraction markers such as N__ and later translation.

<a id="s20"></a>

## S20: DBIO::Cake, release 0.900002

[Primary documentation](https://metacpan.org/release/GETTY/DBIO-0.900002/view/lib/DBIO/Cake.pm)

Checked scope: DDL-style schema sugar; an analogy to this pattern, not an instance of it.

## Project source

The pattern was distilled from a production Moose task DSL and a design note
describing it. That codebase is not public; no repository revision or source audit
of it is claimed. Public checks support the Perl/Moose/Future/JSON Schema concepts,
not the behavior of any particular project. See the
[correction map](corrections-and-adoption.md).

## What was not verified

No existing task-DSL implementation, provider-specific LLM tool integration,
production checkpoint adapter, deployment workflow, performance benchmark, or
independent agent evaluation was executed. Runtime evidence for bundled material
is recorded separately in [VALIDATION.md](../VALIDATION.md).
