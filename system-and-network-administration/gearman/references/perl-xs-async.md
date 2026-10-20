# Perl XS and event-loop alternatives

Evidence: [P3–P8](sources.md). Treat each distribution as a distinct API and maintenance decision. The age of a release is a review signal, not proof of either safety or abandonment.

## Gearman::XS

This binding wraps libgearman, so there are at least three compatibility dimensions: Perl/XS ABI, installed libgearman ABI, and the server protocol/behavior. Capture all three. A CPAN distribution version does not prove that the dynamically linked C library exposes a new TLS or scheduling function.

A documented client shape is:

```perl
use Gearman::XS qw(:constants);
use Gearman::XS::Client;
my $client = Gearman::XS::Client->new;
my $rc = $client->add_server('127.0.0.1', 4730);
die "server configuration rejected" if $rc != GEARMAN_SUCCESS;
$client->set_timeout(5000);  # milliseconds; not an end-to-end cancellation guarantee
my ($code, $result) = $client->do('example.bytes.v1', 'payload');
die "request failed or outcome uncertain: $code" if $code != GEARMAN_SUCCESS;
```

The documented two-argument method above does not establish an exposed unique-key parameter; inspect the installed XS source before relying on one. This is a source-documented API sketch, not a locally executed native-binding test. Unlike the classic client, `do` and `do_background` return a code/value pair; the latter's value is a handle. Check the return code before treating the second item as a successful result. For multi-task APIs, inspect callback signatures, context retention, task cleanup and `run_tasks` behavior in the installed version.

An XS worker similarly has its own registration and work-return-code conventions. Do not paste a classic `register_function` callback into an XS `add_function` call. The job object exposes workload/status/result operations through the binding; match memory ownership and terminal-send semantics to its documentation. Model callbacks as a state machine with exactly one terminal decision.

## Event-driven Perl

`AnyEvent::Gearman` and `EV::Gearman` are separate candidates, not alternative import names for XS. The indexed EV documentation describes a direct-protocol XS implementation using EV without a libgearman dependency. Full EV documentation retrieval was unavailable during this review, so this skill deliberately supplies no guessed constructor or TLS methods.

Before selecting an event-loop binding, verify its runtime support, release/source history, reconnect and re-registration behavior, bounded buffering, cancellation semantics, TLS verification, and error handling when a write succeeds but its acknowledgement is lost. Test callbacks after a caller times out or is garbage-collected. Keep CPU-heavy callbacks out of the event loop; use supervised execution slots rather than unbounded fork-per-job behavior.

## Choosing and packaging

Prefer the smallest dependency stack that demonstrably satisfies the application's behavior requirements. An all-Perl deployment can simplify packaging; a C-backed deployment can reuse libgearman features; an event-loop deployment can integrate many concurrent sockets. None is intrinsically an exactly-once system.

For binary packaging record shared libraries, architecture, libc, TLS and optional backend dependencies. Test the built artifact on a clean target with no development tree. Do not assume that a bundled Perl interpreter also bundles dynamically loaded XS libraries or the correct libgearman.
