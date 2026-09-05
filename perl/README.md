![perl](../assets/perl.png)

# Perl skills

Shared Perl knowledge, split by what kind of knowledge it is:

- **`getty-` prefixed** — prescribes something: a house convention chosen over other
  valid options, or the API of software Getty itself wrote. Follow it as given.
- **No prefix** — a reference: how a public module or protocol actually behaves. True
  for anyone using that technology, Getty or not.

`getty-perl-core` is the one to load first — it sets the conventions the others build
on. For a `dist.ini` under `[@Author::GETTY]`, load `perl-release-dist-ini` (the
generic mechanics) and `getty-perl-release-author-getty` (what the bundle adds)
together.

## House conventions

### [getty-perl-core](getty-perl-core/SKILL.md)

The base layer every other Perl skill assumes: module loading, `strict`/`warnings`,
which object system to reach for, singletons, subroutine shape, error handling with
`croak`, string and control-flow style, configuration from prefixed environment
variables, DBIC-ish result classes, comment density, and the `Changes` file.

Two sections carry more weight than the rest. **Methods, not bare subs** — inside a
class every helper is a method on `$self`, per-process caches are attributes on the
singleton rather than `my %CACHE` package variables, and no package-level state
survives unless it is a true constant. And the **cpanfile rules for Getty-authored
dependencies**, which exist because pinning a Getty module's `$VERSION` as a
requirement breaks in ways that are painful to unpick.

Closes with a `Forbidden` list — `require Foo` inside a method, `'0'` as a version
argument, 4-space indent, `File::Spec` in new code, `Data::Dumper` in shipped code,
`die` where `croak` belongs.

**Load when** editing any Perl code in a Getty project.

### [getty-perl-moo](getty-perl-moo/SKILL.md)

Moo classes and roles. The core principle: inheritance sparingly for stable "is-a"
contracts, roles heavily for horizontal reuse — when in doubt, role, not subclass.

House conventions come first (`with '...'` directly under `use Moo;` because
composition is a runtime action and not an import, `is => 'lazy'` plus a separate
`_build_*` for anything non-trivial, `ro` as the default), then thirteen worked
patterns: attribute override via `+attr`, roles with `requires`, thin classes,
`Import::Into` house-style import modules, `handles` delegation, `Sub::HandlesVia`
for native traits, method modifiers, lifecycle hooks, `MooX::StrictConstructor`,
role conflict resolution, parameterized roles, and Moose interop. Ends with a
decision table mapping a situation to the mechanism, plus the recurring pitfalls.

**Load when** writing classes or roles in a Moo distribution.

### [getty-perl-moose](getty-perl-moose/SKILL.md)

The same shape for Moose, and the same core principle — plus `make_immutable` on
every class.

Fourteen patterns, including the ones Moo does not have: `augment`/`inner` inverted
inheritance, `MooseX::Role::Parameterized`, native-trait delegation, the full
constructor lifecycle (`BUILDARGS`, `BUILD`, `DEMOLISH`), and Moose's own type
constraints. The house convention worth calling out is **wrapping `has` when a shape
repeats**: many attributes sharing one pattern get a generator sub that calls `has`,
rather than the declaration copied N times.

**Load when** writing classes or roles in a Moose distribution.

### [perl-mojo](perl-mojo/SKILL.md)

`Mojo::Base` as an object system — attributes and their defaults, overriding an
inherited default, chainable accessors, composing roles, and lazy construction of
expensive members — plus the toolkit around it: `Mojo::UserAgent`, `Mojo::IOLoop`
and the `Mojo::*` helpers worth knowing, with the async patterns and conventions
that come with them.

**Load when** writing Mojolicious or `Mojo::Base` code.

### [getty-perl-typing](getty-perl-typing/SKILL.md)

Two decisions, in this order: does this project need a type system at all, and which
one is cheap enough here. Getting the order wrong is the common failure — pulling
`Type::Tiny` into a 200-line Moo distribution that had no shape problem to begin
with.

A table maps the situation to the tool: Moose already present means Moose's own
types; a small Moo distribution with simple shapes means no type system at all;
genuinely complex data in Moo means `Type::Tiny`; and the same domain type appearing
across many classes is what finally earns a `Type::Library`. Then where typing pays
— data crossing a boundary, public parameters, closed value sets — and where it does
not: an internal attribute your own lazy builder filled does not need a constraint
that cannot fail.

**Load when** typing attributes or parameters, or deciding whether a project needs
types at all.

## Distribution and release

### [getty-perl-distribution](getty-perl-distribution/SKILL.md)

Creating a new CPAN distribution, or bringing an existing one in line. Resolves its
inputs first (dist name, module name, abstract, author, licence, IRC channel), then
reads **one** existing sibling dist closest in topic and matches its layout exactly —
copying from a real sibling beats a template, so the templates it ships are the
fallback for when no sibling fits.

Covers the `dist.ini` metadata block and why `author` carries the cpan.org address
while `copyright_holder` carries the everyday one, test file conventions, the CI
workflow including the Alien/XS variant, and a handcheck list for what to verify
after writing.

**Load when** creating a new CPAN distribution or polishing an existing one.

### [perl-release-dist-ini](perl-release-dist-ini/SKILL.md)

Generic Dist::Zilla reference that holds for any distribution regardless of author
bundle — telling a bundle section from a plugin section, what the common sections
mean, version configuration, prereqs and metadata.

Pairs with `getty-perl-release-author-getty`, which adds what one specific bundle
does on top.

**Load when** reading, editing or debugging any `dist.ini`.

## XS and C libraries

### [perl-xs](perl-xs/SKILL.md)

The Perl/C boundary. Leads with the framing that saves the most time — an `.xs` file
is C with a preprocessor in front of it, and the XS-specific part is only three
decisions: how a C pointer lives inside an SV, how it converts at the boundary, and
what one XSUB looks like inside.

The house answer to the first is `sv_magicext` with a per-type `MGVTBL`: `svt_free`
is a better destructor than a Perl `DESTROY` (it cannot be overridden, it survives
global destruction), and the vtable address doubles as the type check that turns a
hand-blessed hashref into a croak instead of a segfault. Four references carry the
depth: the typemap and its escaping rule, object lifetime including the refcount
chain a child owes its parent and the generation-counter pattern for libraries that
free your children behind your back, XSUB sections and the argument stack, and the
build/test side — `ppport.h`, reading generated C, and testing crashes in a forked
child so a regression fails instead of taking `prove` down.

**Load when** writing or debugging XS, a typemap, or a segfault at the Perl/C
boundary.

### [perl-alien](perl-alien/SKILL.md)

`Alien::Build` — providing a C library or tool to CPAN. One question at install
time: is a usable libfoo already here, and if not, how is one built?

Covers the `probe`/`sys`/`share` split and why `plugin 'PkgConfig'` should write the
first two, the `minimum_version` floor and why the comment explaining it matters more
than the number, bundling the source tarball for network-free installs, and the rule
that no path may be hardcoded because the build prefix is a staging directory. Two
references hold the rest: the alienfile in detail (interpolation, custom `build sub`,
`install_prop` vs `runtime_prop`, gather hooks, the plugin catalogue) and the
consumer side (XS and FFI, `cpanfile`, `Test::Alien`, forcing both install types).

Pairs with `perl-xs` — the Alien resolves the flags, the XS module links against
them.

**Load when** writing or debugging an alienfile, or consuming `cflags`/`libs` from
an Alien.

## Libraries and protocols

### [perl-io-async-future](perl-io-async-future/SKILL.md)

PEVANS-style async Perl. The framework is small; its lifetime rules are unforgiving.

The skill leads with the one rule behind most of the bugs: **retain every Future you
care about until it is ready.** A Future is a Perl object like any other — when the
last reference drops it is destroyed even though the operation is in flight, and the
symptom is usually a silent hang rather than an error. Nine patterns follow (notifier
skeleton, the TCP-connect GC trap, reconnect without losing futures, composition,
`->retain`, `async`/`await`, timeouts, cancellation hygiene, loops and tests) and
close on a mental model: every async bug is either nobody held the Future, somebody
held it too tightly through a `$self` capture, or it was held and never released.

**Load when** writing async Perl — IO::Async, Future, Future::AsyncAwait,
`Net::Async::*`, or debugging a future lost to GC.

### [perl-mcp](perl-mcp/SKILL.md)

Building an MCP server in Perl with `MCP::Server`: server setup, tool definitions
and their input schemas, the handler signature and how to return results, CRUD tool
sets, Kubernetes and database integration patterns, async integration with
Langertha, and a section on writing tool descriptions the calling model can actually
route on.

**Load when** building an MCP server in Perl.
