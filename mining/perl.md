# Perl — mined decisions

Candidates extracted from hand-written Getty code, awaiting judgement. Fill in
each `verdict:` with `yes`, `no`, or free text ("yes, but only in modules").
Free text is the most valuable answer — it carries knowledge the code cannot.

**Rejected candidates stay in this file with their verdict.** That record is
what stops a later run from proposing the same thing again.

## Corpus — run 1 (2026-08-19)

| Repo | HEAD | Perl lines | Span | AI commits |
|---|---|---|---|---|
| `sunriser` | `3de3e35` | 3,921 | 2014–2024 | 0 |
| `amigaevent` | `38eb7d4` | 10,522 | 2022–2025 | 0 |

Excluded as vendored third-party code: `sunriser/docker/CDB-TinyCDB-0.05-patched/`,
`amigaevent/lib/PDF/API2/`, `amigaevent/lib/Business/`, `amigaevent/lib/Catalyst/`.

## Landed — run 1, 2026-08-19

| Target | Candidates |
|---|---|
| `getty-perl-core` | C02 C06 C09 C15 C16 C17+C18 C19 C21 C22 C24 C25 C26 C27 C28 C32 C33 C43+C44 C45 C47 |
| `getty-perl-moo` | C05 C07 C08 C11 |
| `getty-perl-moose` | C05 C13 |
| `getty-perl-typing` | C10 |
| `getty-perl-distribution` | C34 C35 C36 C39 C40 C42 |
| `getty-perl-release-author-getty` | C01 C38 C41 |
| already canon before this run | C04 C07 C12 C14 C23 C29 C30 C31 |
| rejected | C03 C20 C37 C46 C48 |

C10 is recorded as an intent, not a finished rule. Run 2 looked for a typing
canon and found none: see `perl-typing.md` for why that corpus was withdrawn.

Counts are `sr=` sunriser, `ae=` amigaevent, over that corpus only. Every line
reference was read back from the file, not recalled.

---

## Axis: file skeleton

### C01 — `# ABSTRACT` on line 2, in modules and scripts alike
Rule:     Put `# ABSTRACT: <one line>` directly under `package`, before any `use`. Executables in `bin/` get one too, under the shebang.
Evidence: sunriser/lib/SunRiser.pm:2 · sunriser/bin/sunriser:3 · amigaevent/lib/AmigaEvent.pm:2
Spread:   sr=21 ae=66, no counter-examples, 2014–2025
Target:   getty-perl-core
verdict:  yes, but that is part of the dist zilla author getty skill! It is useless on distributions or raw files that are not managed with dist zilla and my plugin bundle.

### C02 — no `use strict`/`use warnings` in modules, always in scripts and tests
Rule:     Modules rely on Moo/Moose to enable strict and warnings — do not repeat them. Scripts in `bin/` and every `.t` file declare both explicitly.
Evidence: sunriser/lib/SunRiser.pm (absent) · sunriser/bin/sunriser:7-8 · sunriser/t/load.t:2-3
Spread:   modules sr=0/10 ae=5/66 · scripts+tests sr=17/17 ae=18/21, 2014–2025
Target:   getty-perl-core
verdict:  yes, but i would not say it like that, this is wrong, practical we want to use strict and warnings EVERYWHERE ALWAYS, we just additionally inform that specific modules deliver strict and warnings for us, like Moo and Moose, or Catalyst or any other Module that derived from Moose, so that must be explained technical correct to not make wrong impressions

### C03 — POD block at end of file: empty DESCRIPTION plus SUPPORT
Rule:     End every module with `=head1 DESCRIPTION` (may be empty) and `=head1 SUPPORT` listing repository and issue tracker URLs.
Evidence: sunriser/lib/SunRiser.pm:197,199 · sunriser/lib/SunRiser/Publisher.pm:293
Spread:   sr=10/10 · ae=0/66 (proprietary, no public repo), 2014–2024
Target:   getty-perl-core
verdict:  that is totally wrong, no idea what i even should made out of that, POD topic generally is more a release part thing, remove that completely

### C04 — two-space indent, never tabs
Rule:     Indent with two spaces. Continuation lines indent four.
Evidence: whole corpus
Spread:   0 tab-indented lines in 14,443 lines, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C05 — `with 'Role';` before the remaining `use` statements
Rule:     Place `with '...'` directly after `use Moo;`/`use Moose;`, ahead of the other imports — role composition reads as part of the class declaration, not as code.
Evidence: sunriser/lib/SunRiser/CDB.pm:6 · sunriser/lib/SunRiser/Config.pm:6 · sunriser/lib/SunRiser/Finder.pm:8
Spread:   sr=5/5 classes that consume a role, 2014–2024
Target:   getty-perl-moo
verdict:  yes, but because its anyway the runtime time where it gets executed, this is btw the same on Moose. runtime vs compile time.

---

## Axis: object system

### C06 — one object system per project, never mixed
Rule:     Pick Moo or Moose per distribution and use it everywhere. Do not mix within one codebase.
Evidence: sunriser 10/10 Moo · amigaevent 65/66 Moose (amigaevent/lib/AmigaEvent/Admin/Model/DB.pm:4 is the lone Moo, imposed by RapidApp)
Spread:   2 projects, 2 clean choices, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C07 — `is => 'lazy'` plus a separate `_build_*`, never an inline default
Rule:     In Moo, declare `has x => ( is => 'lazy' );` and write `sub _build_x` below it. Never put the construction into `default => sub {...}`.
Evidence: sunriser/lib/SunRiser.pm:26 · sunriser/lib/SunRiser/Publisher.pm:20
Spread:   sr=44 lazy / 47 builders vs 14 inline defaults, 2014–2024
Target:   getty-perl-moo
verdict:  yes

### C08 — one-line builders drop the argument unpacking
Rule:     A builder that ignores `$self` is written on one line without unpacking: `sub _build_readonly { 0 }`.
Evidence: sunriser/lib/SunRiser.pm:51 · sunriser/lib/SunRiser/Finder.pm:10
Spread:   sr=12, 2014–2024
Target:   getty-perl-moo
verdict:  yes

### C09 — attributes are read-only by default
Rule:     Declare `is => 'ro'` unless the attribute is genuinely mutated; `rw` is the exception that needs a reason.
Evidence: sunriser/lib/SunRiser.pm:65 · sunriser/lib/SunRiser/CDB.pm:30 · amigaevent/lib/AmigaEvent.pm:48
Spread:   ro sr=19 ae=45 · rw sr=1 ae=6, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C10 — types belong in the code: Types::Standard plus a per-distribution type library
Rule:     Type attributes with `Types::Standard`. Where a distribution has domain types of its own, declare them in `<Dist>::Types` using `Type::Library`/`Type::Utils` with `where` and `message`, and import from there.
Evidence: **none in hand-written code.** The estate contains two hand-typed lines total, from 2018: kubernetes-rest/lib/Kubernetes/REST/Error.pm (`use Types::Standard qw/Str/;` + one typed attribute). Everything else post-dates 2025-12 and is AI-written — see `perl-typing.md`.
Spread:   run-1 corpus: 0 typed attributes in 14,443 lines · hand-written elsewhere: 2 lines
Note:     Typing is a stated intent, not a mined convention. Writing the rule is a `skill-authoring` job.
Target:   getty-perl-typing (new)
verdict:  yes — towards Type::Tiny, more typing rather than less. Open: which projects to draw the canon from, and whether the methods get consolidated into their own skill.

### C11 — `init_arg` controls the constructor surface
Rule:     An attribute that must not be set from the constructor gets `init_arg => undef`. Renaming a constructor key uses `init_arg => 'other_name'`.
Evidence: sunriser/lib/SunRiser.pm:27 (`timeout_arg` frees the `timeout` method name) · sunriser/lib/SunRiser/CDB.pm:44
Spread:   sr=4, 2014–2024
Target:   getty-perl-moo
verdict:  that should be actually part of the documentation perl-moo itself if we would have one, but i think its ok to set it here as reminder. but it belongs clearly in a perl-moo, we might want to a perl-moo and a perl-moose skill generally that is build like the class usage skill in DBIO

### C12 — `namespace::autoclean` in Moose classes
Rule:     End the import block of every Moose class with `use namespace::autoclean;`.
Evidence: amigaevent/lib/AmigaEvent.pm:45 · amigaevent/lib/AmigaEvent/Web.pm:6
Spread:   ae=36 · sr=0 (Moo project), 2022–2025
Target:   getty-perl-moose
verdict:  ... yes i would say

### C13 — build sugar that wraps `has` when a pattern repeats
Rule:     When many attributes share a shape, write a generator sub that calls `has` instead of repeating the declaration.
Evidence: amigaevent/lib/AmigaEvent.pm:59 (`sub has_conf`), used as `has_conf is_live => AMIGAEVENT_LIVE => 0;` at :98
Spread:   ae=1 generator, 24 uses, 2022–2025
Target:   getty-perl-moose
verdict:  yes

---

## Axis: subroutines

### C14 — `my ( $self, $x ) = @_;` with inner spacing, as the first line
Rule:     Unpack arguments on the first line of every sub, with a space inside the parentheses.
Evidence: sunriser/lib/SunRiser.pm:35 · sunriser/lib/SunRiser/Finder.pm:40
Spread:   402 with spacing vs 8 without, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C15 — one-liners use `shift->` or `$_[0]->`
Rule:     A delegating or trivial one-line sub skips unpacking: `sub trace { shift->_logger->trace(@_) }`, `sub healthcheck { path($_[0]->healthcheck_file)->... }`.
Evidence: sunriser/lib/SunRiser/Role/Logger.pm:9-10 · amigaevent/lib/AmigaEvent.pm:109-110
Spread:   sr=5 ae=14, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C16 — private subs carry a leading underscore
Rule:     Prefix internal subs and attributes with `_`. Builders for private attributes double up: `sub _build__mp`.
Evidence: sunriser/lib/SunRiser.pm:30 · sunriser/lib/SunRiser/Finder.pm:10
Spread:   sr=61 ae=27, 2014–2025
Target:   getty-perl-core
verdict:  yes for sure, that is even perl standard :D haha

---

## Axis: error handling

### C17 — `croak`, not `die`
Rule:     Raise errors with `croak` so they report the caller's line.
Evidence: sunriser/lib/SunRiser.pm:114,120 · sunriser/lib/SunRiser/Config.pm:45
Spread:   croak sr=41 ae=13 vs die sr=2 ae=10, 2014–2025
Target:   getty-perl-core
verdict:  yes, we always use croak, which somehow combined with C18

### C18 — import croak, do not qualify it
Rule:     Write `use Carp qw( croak );` and call `croak(...)` bare.
Evidence: sunriser/lib/SunRiser.pm:9 · sunriser/lib/SunRiser/CDB.pm:16 · amigaevent/lib/AmigaEvent/DB/Result/Product.pm:9
Spread:   sr=6 ae=8, 2014–2025
Note:     **Contradicts newer code.** `langertha` (2024–2026) uses `use Carp ();` with fully qualified `Carp::croak(...)`. One of the two is your current preference — the verdict decides which.
Target:   getty-perl-core
verdict:  yes, thats how to use croak, which somehow combined with C17

### C19 — error messages name the method that raised them
Rule:     Prefix the message with the origin: `croak __PACKAGE__."->state too many args"`.
Evidence: sunriser/lib/SunRiser.pm:156
Spread:   sr=1 — weak, one occurrence only, 2014–2024
Target:   getty-perl-core
verdict:  yes, or any other fitting to the DSL concept

### C20 — verbose Carp in the application entry class
Rule:     The top-level application class sets `BEGIN { $Carp::Verbose=1; }` so every croak carries a full backtrace.
Evidence: amigaevent/lib/AmigaEvent.pm:9
Spread:   ae=1 — weak, but deliberate and global in effect, 2022–2025
Target:   getty-perl-core
verdict:  not always, i wouldn't say thats a yes, better a no, just ignore that. But we could give it to some perl skill that we might wanna do, but yeah no.. or you can make it a possible suggestion.

---

## Axis: strings

### C21 — concatenate, do not interpolate
Rule:     Build strings with `.`: `'Parsing definition file '.$self->definition_file`. Reserve interpolation for cases where concatenation would be unreadable.
Evidence: sunriser/lib/SunRiser/Config.pm:81,116 · sunriser/lib/SunRiser/CDB.pm:75
Spread:   concatenation sr=26 ae=48 vs interpolation sr=18 ae=16, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C22 — single quotes by default
Rule:     Use `'...'` unless the string needs escapes or interpolation.
Evidence: dominant across the corpus · drift visible in amigaevent/lib/AmigaEvent/DB/Result/Product.pm:16 (`"integer"`) vs :27 (`'text'`)
Spread:   dominant, with local inconsistency in DBIC column definitions
Target:   getty-perl-core
verdict:  yes, do not forget that "" and '' are also different in Perl

### C23 — `qw( ... )` with inner spacing
Rule:     Write import lists as `qw( croak confess )` — space inside the parentheses.
Evidence: sunriser/lib/SunRiser.pm:9 · amigaevent/lib/AmigaEvent.pm:11
Spread:   77 spaced vs 10 unspaced · but `qw/ ... /` also appears (ae=17), 2014–2025
Target:   getty-perl-core
verdict:  yes

---

## Axis: control flow

### C24 — postfix `if`/`unless` for guards and short conditions
Rule:     Write `croak(...) if $self->readonly;` rather than a block.
Evidence: sunriser/lib/SunRiser.pm:156 · amigaevent/lib/AmigaEvent/DB/Result.pm:154,190
Spread:   if sr=56 ae=61 · unless sr=28 ae=97, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C25 — `unless` instead of negated `if`
Rule:     Prefer `unless $x` over `if !$x`.
Evidence: sunriser/lib/SunRiser.pm:85 · sunriser/lib/SunRiser/CDB.pm:177
Spread:   125 occurrences, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C26 — guard clauses return bare
Rule:     Early exits use `return;` or `return unless ...`, not `return undef;`.
Evidence: sunriser/lib/SunRiser.pm:85 · sunriser/lib/SunRiser/CDB.pm:177 · amigaevent/lib/AmigaEvent/Web.pm:188,199
Spread:   bare sr=2 ae=9 vs `return undef` sr=6 ae=3 — **genuinely split**, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C27 — nested ternaries for branching returns
Rule:     A return that picks between several expressions is written as a nested ternary rather than an if/elsif chain.
Evidence: sunriser/lib/SunRiser/CDB.pm:50-54 · sunriser/lib/SunRiser.pm:156
Spread:   sr=4, 2014–2024
Target:   getty-perl-core
verdict:  yes

---

## Axis: data handling

### C28 — return copies of hashes and arrays, not references to lexicals
Rule:     Return `{ %types }` / `[ @data ]`, never `\%types` / `\@data`.
Evidence: sunriser/lib/SunRiser/Config.pm:33 · amigaevent/lib/AmigaEvent/DB/Result.pm:53 · amigaevent/lib/AmigaEvent/Web.pm:217
Spread:   copies sr=2 ae=7 vs refs sr=0 ae=4, 2014–2025
Target:   getty-perl-core
verdict:  actually that is wrong my $a = { %types };   # neue, anonyme Hash-Kopie my $b = \%types;      # Referenz auf den bestehenden Hash, so its 2 different things. that must be considered! i most often dereferenced with that.

### C29 — serialisation is always canonical
Rule:     Configure every serialiser for deterministic output: MessagePack `->canonical`, JSON `canonical => 1`, DBIC `serializer_options => { canonical => 1 }`.
Evidence: sunriser/lib/SunRiser.pm:51 · sunriser/lib/SunRiser/CDB.pm:62 · amigaevent/lib/AmigaEvent.pm:254 · amigaevent/lib/AmigaEvent/DB/Result/Product.pm:61
Spread:   every serialiser in the corpus, no exception, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C30 — `JSON::MaybeXS` is the JSON interface
Rule:     Use `JSON::MaybeXS`, never `JSON::XS` or `JSON::PP` directly.
Evidence: sunriser/lib/SunRiser.pm:8 · amigaevent/lib/AmigaEvent.pm:22 · amigaevent/lib/AmigaEvent/DB/Result.pm:10
Spread:   sr=7 ae=10, no counter-examples, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C31 — `Path::Tiny` for all filesystem access
Rule:     Reach for `path(...)` rather than bare `open`, `File::Spec`, or `File::Slurp`.
Evidence: sunriser/lib/SunRiser/CDB.pm:10 · sunriser/lib/SunRiser/Config.pm:11 · amigaevent/lib/AmigaEvent.pm:25
Spread:   sr=7 ae=7, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C32 — aligned fat commas in hash literals
Rule:     Align `=>` in multi-line hash literals when the keys are of similar length.
Evidence: sunriser/lib/SunRiser/CDB.pm:179-182 (`description`/`author`/`filename`/`timestamp`)
Spread:   sr=1 — weak, one hash only, 2014–2024
Target:   getty-perl-core
verdict:  yes

### C33 — conditional hash entries via `? ( k => v ) : ()`
Rule:     Add an optional pair inline: `$cond ? ( experimental => 1 ) : (),`.
Evidence: sunriser/lib/SunRiser/CDB.pm:183 · sunriser/lib/SunRiser/Publisher.pm:190
Spread:   sr=3, 2014–2024
Target:   getty-perl-core
verdict:  yes

---

## Axis: tests

### C34 — `.t` files start with a shebang
Rule:     Every test file opens with `#!/usr/bin/env perl`, then `use strict; use warnings; use Test::More;`.
Evidence: sunriser/t/load.t:1-4 · sunriser/t/simulator.t:1-4
Spread:   sr=7/7, 2014–2024
Target:   getty-perl-distribution
verdict:  yes

### C35 — `done_testing;` instead of a plan
Rule:     Close tests with `done_testing;`; never declare `plan tests => N`.
Evidence: sunriser/t/load.t:19 · sunriser/t/simulator.t:17
Spread:   sr=7/7, no `plan tests` anywhere, 2014–2024
Target:   getty-perl-distribution
verdict:  yes

### C36 — a load test enumerating every module
Rule:     Ship `t/load.t` that `use_ok`s each module from a `qw( ... )` list.
Evidence: sunriser/t/load.t:6-17
Spread:   sr=1/1 distribution, 2014–2024
Target:   getty-perl-distribution
verdict:  yes

### C37 — applications ship without tests
Rule:     — (withdrawn)
Evidence: sunriser (library+tooling) has t/ · amigaevent (Catalyst app, 10.5k lines) has none
Spread:   2 projects, 2 opposite choices
Target:   —
verdict:  no — circumstance, not policy. amigaevent needs tests too; i just never came to that, but deferred now because it is being rewritten.

---

## Axis: distribution

### C38 — `[@Author::GETTY]` for CPAN, explicit plugin list otherwise
Rule:     Public distributions use the bundle; proprietary ones list plugins explicitly (the bundle assumes a CPAN release).
Evidence: sunriser/dist.ini:7-8 (`[@Author::GETTY]` + `no_cpan = 1`) · amigaevent/dist.ini:7-30 (explicit list)
Spread:   2 projects, 2014–2025
Target:   perl-release-dist-ini
verdict:  yes aber nur für getty stuff also nicht perl-release-dist-ini sondern für das author-getty

### C39 — every `requires` carries an explicit version, `'0'` when unpinned
Rule:     Write `requires 'Path::Tiny', '0';` — never omit the version argument.
Evidence: sunriser/cpanfile:1-38 · amigaevent/cpanfile:1-25
Spread:   every line of both cpanfiles, no exception, 2014–2025
Target:   getty-perl-distribution
verdict:  oh you can omit the version argument on cpanfile, probably btw make it a rule to use cpanfile to cover requirements and no extra 0, that was override, and also (which is what you did sometimes hehe) no '>= 5.0' or so, because that IS the default, '5.0' already means "5.0 or higher"

### C40 — cpanfile sorted alphabetically, phases last
Rule:     Keep `requires` lines in alphabetical order; phase blocks (`on test => sub {...}`) go at the end.
Evidence: sunriser/cpanfile · amigaevent/cpanfile · drift: `Compress::Zlib` appears twice in sunriser/cpanfile:5 and :15
Spread:   both files, one duplicate
Target:   getty-perl-distribution
verdict:  yes

### C41 — `[Run::Release]` carries the project-specific release step
Rule:     Hook deployment into the release with `[Run::Release]` rather than a script invoked by hand.
Evidence: sunriser/dist.ini:10 (`xbin/release.sh %v %a`) · amigaevent/dist.ini:32 (docker build+push)
Spread:   2/2 projects, 2014–2025
Target:   perl-release-dist-ini
verdict:  this is also just for the getty release dist-ini author getty skill not for the generic one and it shouldnt be used for things the dist anyway already did.

### C42 — dist.ini header block: name, author, license, copyright
Rule:     Open dist.ini with `name`, `author`, `license`, `copyright_holder`, `copyright_year`, aligned on `=`.
Evidence: sunriser/dist.ini:1-5 · amigaevent/dist.ini:1-5
Spread:   2/2, 2014–2025
Target:   perl-release-dist-ini
verdict:  that should be already part of the getty-perl-distribution skill explained there on the creating not for the perl-release-dist-ini

---

## Axis: comments and structure

### C43 — ASCII-art banners divide long files
Rule:     Split a long module into sections with a figlet-style ASCII banner comment.
Evidence: amigaevent/lib/AmigaEvent.pm:90-96 (`CONFIG`) · :167
Spread:   ae=6 banners in 871 lines, 2022–2025
Target:   getty-perl-core
verdict:  yes but use figlet and we can define a list of fonts that he should use, and if no figlet is there you can use triplethich ==== lines to make to snappy

### C44 — `#####` rules mark section boundaries in shorter files
Rule:     Use a `##### <Name>` comment where a banner would be too much.
Evidence: sunriser/lib/SunRiser/CDB.pm:69 · sunriser/lib/SunRiser/Publisher.pm:146
Spread:   sr=2, 2014–2024
Target:   getty-perl-core
verdict:  that can be merged with C44

### C45 — commented-out debug lines stay in the file
Rule:     Leave `#use DDP; p($res);` in place rather than deleting it — it marks where debugging was needed before.
Evidence: sunriser/lib/SunRiser.pm:93 · amigaevent/lib/AmigaEvent/Web.pm:83
Spread:   sr=3 ae=5, 2014–2025
Note:     An agent will delete these as dead code unless told not to.
Target:   getty-perl-core
verdict:  yes, actually i think it helps the AI, or? it spares a thinking step so to say, or not?

### C46 — commented-out dist.ini blocks are kept as documentation
Rule:     Keep disabled dist.ini sections and deployment commands as `;` comments instead of removing them.
Evidence: amigaevent/dist.ini:35-45
Spread:   ae=1, 2022–2025
Target:   perl-release-dist-ini
verdict:  no

---

## Axis: environment and configuration

### C47 — configuration comes from prefixed environment variables
Rule:     Read config from `$ENV{PROJECT_SOMETHING}` with the project name as prefix, each with a default in code.
Evidence: amigaevent/lib/AmigaEvent.pm:98,100 · sunriser/lib/SunRiser/CDB.pm:147
Spread:   ae=24 via `has_conf` · sr=2 direct, 2014–2025
Target:   getty-perl-core
verdict:  yes

### C48 — logging goes through a project role over MooX::Role::Logger
Rule:     Define one `<Project>::Role::Logger` composing `MooX::Role::Logger`, exposing `trace/debug/info/notice/warning`; each class sets its category via `sub _build__logger_category`.
Evidence: sunriser/lib/SunRiser/Role/Logger.pm:1-16 · sunriser/lib/SunRiser/Config.pm:8 · sunriser/lib/SunRiser/Publisher.pm:8
Spread:   sr=1 role, 5 consumers, 2014–2024
Target:   getty-perl-core
verdict:  no, that is not our method, but i show you probably a plan that we should use constantly but just dont make a rule here of that topic yet
