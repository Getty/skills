---
name: perl-io-async-future
description: "Use when writing async Perl — IO::Async, Future, Future::AsyncAwait, Net::Async::*, futures lost to GC, cancellation, requests that hang."
---

# Perl IO::Async + Future — Patterns & Pitfalls

PEVANS-style async Perl. The framework is small, but its lifetime rules are unforgiving:
a Future that nobody holds is garbage-collected mid-flight, and the symptom is rarely a
clear error.

## The one rule: hold every Future until it is ready

**You MUST retain every Future you care about until it is ready.**

A Future is a handle to a result that may not exist yet, and also a plain Perl object
with a refcount. When the last reference drops it is destroyed — even while it stands
for an in-flight operation. The op may continue, complete into the void, or wedge;
nobody hears about it. With `Future::AsyncAwait` you see:

> Suspended async sub Foo::bar lost its returning future

The async sub's continuation was destroyed mid-flight. Without async/await you see
*nothing* — a hang, or a callback that never fires.

```perl
# ❌ BUG: $f is local to the closure, GC'd as soon as _reconnect returns
sub _reconnect {
  my $self = shift;
  my $f = $self->loop->delay_future(after => 2)->then(sub { $self->connect });
}
```

Hold it in one of three ways:

1. **Store it on the object** — `$self->{_some_future}`, or any container that outlives
   the operation. Store the *whole chain*, not just the leaf. When a caller drops an
   async sub's Future, the cure is the caller storing it — the async sub does not retain
   its own returning Future, and adding `->retain` inside it is not the fix.
2. **Wait before returning.** A local-variable-only Future is a bug unless the local
   *waits* (`await`, or `->get` in sync code) before the sub returns.
3. **`->retain`** — rare; only for true fire-and-forget, when you need the op to
   *finish* but genuinely don't need its result. Otherwise hold the Future yourself.

```perl
$self->_log_async($msg)
  ->on_fail(sub { warn "log failed: $_[0]" })
  ->retain;
```

`->retain` makes the Future hold itself (a reference cycle) until it completes, then
lets go. Without it this chain has no holder and is destroyed before it runs.

## Holding it without leaking

Nearly every async bug is one of three: nobody held the Future; something held it too
tightly through a captured `$self`; or it was held but never deleted and now blocks the
next operation.

- **Weaken `$self` in callbacks** of a chain stored on `$self`:
  `weaken(my $weak = $self)` (from `Scalar::Util`), then `my $self = $weak or return;`
  inside each callback. A strong capture keeps the object alive forever; reconnect loops
  leak.
- **Delete the held Future in both `on_done` and `on_fail`.** A stale
  `$self->{_reconnect_future}` trips guards like `return if $self->{_reconnect_future}`
  and blocks every later attempt.
- **Kill the stale attempt before starting a new one:** `delete` it from `$self`, then
  `$f->cancel unless $f->is_ready`.

## Other traps

- **`configure`:** `delete` your keys from `%params`, then always chain
  `$self->SUPER::configure(%params)`. Leftover keys throw `configure_unknown`; skipping
  the chain leaves defaults silently missing and unknown keys silently accepted.
- **`$self->loop` is undef until `$loop->add($notifier)`.** Anything that calls it must
  run after the add.
- **In an `async sub`, write `return await $f`, never `return $f`** — returning a Future
  double-wraps the result.
- **`then` chains, `on_done` observes.** `then` returns a *new* Future, and its callback
  returns a Future to chain — use it for control flow. `on_done`/`on_fail` return the
  *same* Future and discard the callback's return value — use them for side effects. A
  "chain" of `on_done` calls is really parallel observers of the original Future.
- **Net::Async::HTTP: the first request fails, then every request to that host hangs
  with no error** — a module loaded at connect time died and leaked the host's
  connection slot. Before the first request, `require` `IO::Async::Internals::Connector`
  (and `IO::Async::SSL` for https) in an `eval` and fail with the module name.

## References

- Notifier subclass skeleton, `configure` vs `new`, child notifiers, `$loop->new_future`,
  running the loop, `->get` in scripts, IO::Async::Test:
  [references/notifier.md](references/notifier.md)
- TCP connect with a protocol handshake, the reconnect loop, failing `_connect_future`
  on disconnect, the Net::Async::HTTP hang in full:
  [references/connect-reconnect.md](references/connect-reconnect.md)
- `then`/`else`, `needs_all`, `wait_any`, `also =>`, timeouts, cancellation rules, a
  decision guide: [references/composition.md](references/composition.md)
- `async sub`/`await` example, `@_` across `await`, `await` in `map`/`grep`:
  [references/async-await.md](references/async-await.md)
