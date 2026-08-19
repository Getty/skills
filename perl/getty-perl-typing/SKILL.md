---
name: getty-perl-typing
description: "Use when typing Perl attributes or parameters — isa, Moose constraints, Type::Tiny, Types::Standard, Type::Library, Maybe/Optional/Enum, or whether a project needs types at all."
---

# Perl Typing — Getty House Rules

The tendency is to type — but not everything, and not with the same tool
everywhere. Two decisions, in this order: **does this project need a type system
at all**, and **which one is cheap enough here**.

Getting that order wrong is the common failure: pulling `Type::Tiny` into a
200-line Moo distribution that had no shape problem to begin with.

## Choosing the tool

| Situation | Use |
|---|---|
| Moose is already in the project | **Moose's own type system.** `isa => 'Str'`, `ArrayRef[Str]`, `enum` from `Moose::Util::TypeConstraints`. It ships with Moose — no new dependency, and it is enough for tightening a handful of places. |
| Small Moo distribution, simple shapes | **No type system.** `required => 1` and a clear attribute name carry it. Do not add a dependency to state that a string is a string. |
| Moo, and the data genuinely is complex | **`Type::Tiny` / `Types::Standard`.** Moo has no types of its own; this is the standard answer, and it is fast. |
| The same domain type appears across many classes | **A `<Dist>::Types` library** on `Type::Library`. The heaviest option — it earns its place once the definition of "a valid account name" would otherwise be written out in five files. |

**Do not start a type library because a distribution has types.** Start one when
the same type is imported in several places and its definition needs one home.

Moose and `Type::Tiny` coexist fine, but pick one per distribution rather than
having two vocabularies for `Str` in the same tree.

## Where typing pays

Type what arrives from outside; be sparing inside.

| Place | Worth it? |
|---|---|
| Data crossing a boundary — API responses, config, user input | **Yes.** This is where wrong shapes actually arrive. |
| Public method parameters | **Usually.** A validated signature is documentation the runtime enforces. |
| Result / data objects wrapping a foreign response | **Yes.** Naming the shape is the point of the class. |
| A closed set of allowed values | **Yes** — `enum` / `Enum` beats a `Str` with the values listed in a comment. |
| Internal attributes built by your own lazy builder | **Rarely.** The value came from your own code. `_cache` holding a hashref does not need `HashRef`. |
| Everything else, for consistency | **No.** A type that cannot fail is noise with a maintenance cost. |

## Rules

- **Type the boundary, not every field.** If you cannot say which wrong value the type would have caught, leave it off.
- **Parametrise instead of loosening:** `ArrayRef[Str]` over `ArrayRef`. An unparametrised container type rarely earns its line.
- **`Maybe[X]` for anything the source may omit** — not `Str` with a default that invents data.
- **A declared type states its failure:** give `message { ... }` when the default ("did not pass type constraint") would not tell the reader what to fix.
- **No `coerce` for anything lossy.** Coercion is for the same value in another notation — a string to a `Path::Tiny`, an epoch to a `DateTime`. Anything that guesses, truncates, or fills in a default belongs in explicit code.
- **Never type an attribute you then also check by hand** — one place decides validity.
- **Import the exact types you use:** `use Types::Standard qw( Str Maybe );` — spaces inside the parens. `-types` only inside a type library.

## Moose — tightening a few places

No extra dependency, no library. Built-in types cover most of it:

```perl
package MyApp::Job;
# ABSTRACT: A queued job

use Moose;
use Moose::Util::TypeConstraints;
use namespace::autoclean;

enum 'MyApp::JobState', [qw( pending running done failed )];

has id      => ( is => 'ro', isa => 'Str',            required => 1 );
has state   => ( is => 'rw', isa => 'MyApp::JobState', default  => 'pending' );
has retries => ( is => 'rw', isa => 'Int',            default  => 0 );
has tags    => ( is => 'ro', isa => 'ArrayRef[Str]',  default  => sub { [] } );

__PACKAGE__->meta->make_immutable;
1;
```

`enum` registers a named constraint the whole application can reuse. That is
often all the typing a Moose project needs.

## Moo plus Type::Tiny — when the shapes are the problem

```perl
package WWW::Example::Result::Account;
# ABSTRACT: Account as returned by the API

use Moo;
use Types::Standard qw( Str Int Maybe );
use namespace::clean;

has id      => ( is => 'ro', isa => Str,          required => 1 );
has plan    => ( is => 'ro', isa => Str,          required => 1 );
has memo    => ( is => 'ro', isa => Maybe[Str] );
has quota   => ( is => 'ro', isa => Maybe[Int] );

1;
```

`Maybe[Str]` says the API may send null. `required => 1` says it must be present
at construction. They are different statements and both may apply.

## A type library, once it has earned it

```perl
package WWW::Example::Types;
# ABSTRACT: Domain types for WWW::Example

use Type::Library -base, -declare => qw( AccountName PlanName );
use Type::Utils -all;
use Types::Standard -types;

declare AccountName,
  as Str,
  where { /\A[^\s@]+@[^\s@]+\.[^\s@]+\z/ },
  message { "$_ is not a valid account name" };

declare PlanName, as Enum [qw( basic profi reseller )];

1;
```

Consumers import by name: `use WWW::Example::Types qw( AccountName );`

## Validating parameters

Only where a method is a real entry point — a public API call, a CLI command.
Internal methods take their arguments and get on with it.

```perl
use Type::Params qw( signature_for );

signature_for add => (
  method => 1,                    # without this, $self is read as an argument
  named  => [
    account  => AccountName,
    password => Str,
    memo     => Optional[Str],
  ],
);

sub add {
  my ( $self, $arg ) = @_;
  return $self->_rpc('account.add', {
    account  => $arg->account,
    password => $arg->password,
    $arg->has_memo ? ( memo => $arg->memo ) : (),
  });
}
```

The signature compiles once at load. A rejection reports through the type:

```
kaputt is not a valid account name (in $_{"account"})
Value "gibtsnicht" did not pass type constraint "PlanName" (in $_{"plan"})
  "PlanName" is a subtype of "Enum["basic","profi","reseller"]"
```

The permitted values appear without anyone writing them into an error string.

**`method => 1` is not optional** — without it `signature_for` treats `$self` as
the first argument and every call fails with a parameter-count error that says
nothing about the cause.

`Params::ValidationCompiler` does the same job with a `%validators` hash and also
appears in the estate; either is fine, but not both in one distribution.

## Maybe, Optional, required

Three different questions:

- **`Optional[Str]`** — the key may be absent from the arguments. For parameters.
- **`Maybe[Str]`** — the value may be `undef`. For fields a data source sends as null.
- **`required => 1`** — must be supplied at construction. Orthogonal to both.

## Edge cases

- **A type would need the object's other attributes** → that is a `BUILD` check, not a type. Types see one value.
- **A third-party class instance** → Moose: `isa => 'DateTime'`. Type::Tiny: `InstanceOf['DateTime']`.
- **Performance in a hot path** → install `Type::Tiny::XS`; do not remove the type.
- **`MooseX::Types`** → superseded. In a Moose project use the built-in constraints; if you want more, use `Type::Tiny`.

## Related

- `getty-perl-core` — the house rules these examples otherwise follow.
- `getty-perl-moo` / `getty-perl-moose` — attribute mechanics per object system.
