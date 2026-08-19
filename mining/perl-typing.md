# Perl typing — proposals (run 2, corpus withdrawn)

Run 2. Same format as `perl.md`: fill each `verdict:` with `yes`, `no`, or free
text. Rejected candidates stay with their verdict.

## Corpus — run 2: WITHDRAWN

**This run has no corpus. The rules below are not mined evidence.**

The first pass filtered on the `Co-Authored-By: Claude` trailer alone and
concluded that mailboxorg was hand-written. It is not — it is AI-generated
throughout. The trailer was not yet set consistently when it was built, and four
signals that were in plain sight said so:

| Signal | In mailboxorg |
|---|---|
| Repo starts after the first AI commit in the estate (2025-12-28) | begins 2026-05-07 |
| A commit message names it | `Fixes Changes cause AI is dumb` |
| The repo commits `CLAUDE.md` / skills | `Add CLAUDE.md and perl-mailbox-org-api skill` |
| A whole distribution lands in one day | 12 commits on 2026-05-07 |

Filtered by date instead of by trailer, the hand-written typing in the entire
estate amounts to **two lines, from 2018**:

```perl
# kubernetes-rest/lib/Kubernetes/REST/Error.pm, commit 4a19da73, 2018-09-23
use Types::Standard qw/Str/;
has type => (is => 'ro', isa => Str, required => 1);
```

Typing is something Getty *wants*, not something the hand-written record can
describe. That makes it a case for `skill-authoring`, not for mining.

**What the rules below actually are:** a description of how the AI-written repos
type things. They are readable as proposals — Getty saw this code and asked for
more typing, not less — but nothing here is evidence of house practice, and a
verdict on them is a design decision, not a confirmation.

Run 1 (`perl.md`) is unaffected: sunriser ends 2024-05, amigaevent 2025-10-18,
both entirely before the boundary.

---

## Axis: parameter validation

### T01 — validate method parameters with Params::ValidationCompiler
Rule:     API methods taking named parameters validate them through `Params::ValidationCompiler`'s `validation_for`, not by hand-checking `%params`.
Evidence: p5-www-mailboxorg/lib/WWW/MailboxOrg/API/Account.pm:7,18
Spread:   13/13 API modules in mailboxorg, all hand-written
Target:   getty-perl-typing (new) or getty-perl-moo
verdict:

### T02 — one `%validators` hash per class, keyed by method name
Rule:     Build the validators once at package level: `my %validators = ( add => validation_for(...), del => validation_for(...) );` — compiled at load, not per call.
Evidence: p5-www-mailboxorg/lib/WWW/MailboxOrg/API/Account.pm:17-44
Spread:   13/13 API modules
Target:   getty-perl-typing
verdict:

### T03 — every parameter states `optional` explicitly
Rule:     Write `{ type => Str, optional => 0 }` even for required parameters — never rely on the default.
Evidence: p5-www-mailboxorg/lib/WWW/MailboxOrg/API/Account.pm:20-24,27
Spread:   every parameter in the corpus, no exception
Target:   getty-perl-typing
verdict:

### T04 — the method looks its validator up and tolerates its absence
Rule:     `my $v = $validators{'add'}; %params = $v->(%params) if $v;` — a method without a validator still works.
Evidence: p5-www-mailboxorg/lib/WWW/MailboxOrg/API/Account.pm:63-64
Spread:   every validated method in the corpus
Note:     The `if $v` guard is deliberate defensiveness; worth deciding whether it stays or a missing validator should be an error.
Target:   getty-perl-typing
verdict:

### T05 — `Enum [qw( ... )]` inline for closed value sets
Rule:     A parameter with a fixed set of allowed values gets `Enum [qw( basic profi profixl reseller )]` at the call site rather than a named type.
Evidence: p5-www-mailboxorg/lib/WWW/MailboxOrg/API/Account.pm:22
Spread:   2 occurrences, both hand-written
Target:   getty-perl-typing
verdict:

---

## Axis: the distribution's own type library

### T06 — domain types live in `<Dist>::Types`
Rule:     Each distribution that has domain types of its own declares them in one `<Dist>::Types` module built on `Type::Library`, and consumers import from there by name.
Evidence: p5-www-mailboxorg/lib/WWW/MailboxOrg/Types.pm:5 · imported at API/Account.pm:9
Spread:   1 library, 13 consumers
Target:   getty-perl-typing
verdict:

### T07 — the type module's three-line preamble
Rule:     `use Type::Library -base, -declare => qw( A B );` then `use Type::Utils -all;` then `use Types::Standard -types;` — in that order.
Evidence: p5-www-mailboxorg/lib/WWW/MailboxOrg/Types.pm:5-7
Spread:   1/1 type library
Target:   getty-perl-typing
verdict:

### T08 — a declared type carries `as`, `where` and `message`
Rule:     `declare EmailAddress, as Str, where { ... }, message { "$_ is not a valid email address" };` — the message names the value and what it should have been.
Evidence: p5-www-mailboxorg/lib/WWW/MailboxOrg/Types.pm:11-14
Spread:   2/2 declared types
Target:   getty-perl-typing
verdict:

### T09 — the type library ends with `make_immutable`
Rule:     Close `<Dist>::Types` with `__PACKAGE__->meta->make_immutable;`.
Evidence: p5-www-mailboxorg/lib/WWW/MailboxOrg/Types.pm:21
Spread:   1/1
Target:   getty-perl-typing
verdict:

### T10 — consumers import only the types they use, the library imports all
Rule:     A consuming module writes `use Types::Standard qw( Str Enum HashRef );` — the exact list. Only the type library itself uses `-types`.
Evidence: p5-www-mailboxorg/lib/WWW/MailboxOrg/API/Account.pm:8 vs Types.pm:7
Spread:   13 consumers, all explicit lists
Target:   getty-perl-typing
verdict:

---

## Axis: typed data objects

### T11 — result classes type every attribute
Rule:     A class that wraps an API response types all of its attributes; `is => 'ro'` throughout, `required => 1` for what the API always sends.
Evidence: p5-www-metaforge/lib/WWW/MetaForge/ArcRaiders/Result/Arc.pm:8-18
Spread:   4 result classes in metaforge, hand-written
Target:   getty-perl-typing
verdict:

### T12 — `Maybe[X]` for anything the source may omit
Rule:     A field the API can leave out is `isa => Maybe[Str]`, never bare `Str` with a default.
Evidence: p5-www-metaforge/lib/WWW/MetaForge/ArcRaiders/Result/Arc.pm:22 · Result/Item.pm:48,63 (`Maybe[Int]`, `Maybe[Num]`)
Spread:   dominant form in the result classes
Target:   getty-perl-typing
verdict:

### T13 — `namespace::clean` in Moo classes
Rule:     Moo classes end their import block with `use namespace::clean;` (Moose classes use `namespace::autoclean` — see getty-perl-core).
Evidence: p5-www-metaforge/lib/WWW/MetaForge/ArcRaiders/Result/Arc.pm:6
Spread:   metaforge result classes
Note:     `getty-perl-core` currently names only `namespace::autoclean`. Is `clean` the Moo-side rule, or drift?
Target:   getty-perl-core / getty-perl-moo
verdict:

---

## Conflicts with run 1 — resolved, not conflicts

Both apparent contradictions came from the same bad corpus and dissolve with it.

- **4-space indentation in mailboxorg** does not contradict C04. The repo is
  AI-generated; it is evidence of what an agent does without the skill, which is
  precisely the failure C04 exists to prevent.
- **`qw(Str)` without inner spacing** in mailboxorg and metaforge is the same
  story against C23.

Both are worth keeping in view as **verification cases**: an agent that has read
`getty-perl-core` should now produce `qw( Str )` and two-space indentation in
those repos. If it does not, the skill is not landing.
