# Future composition, timeouts and cancellation

Read when combining Futures — sequencing, running them in parallel, racing them, adding
a timeout — or cancelling one. `then` vs `on_done` is a trap in SKILL.md.

## Combinators

```perl
# Sequential dependency (then = "after this, do that")
$f1->then(sub { do_b(@_) })           # done → done branch
   ->else(sub { recover(@_) })        # fail → recovery branch
   ->then(sub { do_c(@_) });

# Parallel, all must succeed (fails fast, cancels siblings)
my $f = Future->needs_all($fa, $fb, $fc);
my @results = await $f;

# Race — first one wins, losers are cancelled
my $f = Future->wait_any($work, $self->loop->delay_future(after => 5)
                                   ->then_fail('timeout'));

# Observe without composing (does NOT chain — return value ignored)
$f->on_done(sub { warn "done: @_" });
$f->on_fail(sub { warn "failed: $_[0]" });
```

**Protective composition** (Future ≥ 0.51): a component prefixed with `also =>` is not
cancelled when the convergent Future is — for a shared or cached Future that other
observers still wait on. Each `also` covers only the one Future after it: here `$f2` is
protected and `$f3` is an ordinary component.

```perl
Future->needs_all($f1, also => $f2, $f3);
```

## Timeouts

```perl
# delay_future returns a Future that resolves with no value after N seconds
my $timer = $self->loop->delay_future(after => 5);

# Race the work against the timer
my $result = await Future->wait_any(
  $work_future,
  $timer->then_fail('timeout'),
);
```

`then_fail($msg)` is shorthand for "when the upstream Future is done, fail with this
message" — perfect for timeouts. `$loop->timeout_future(after => N)` is a ready-made
timer Future that fails with `"Timeout"`.

## Cancellation hygiene

```perl
# Before starting a new attempt, kill stale ones
if (my $f = delete $self->{_connect_future}) {
  $f->cancel unless $f->is_ready;
}
```

- `->cancel` is idempotent but only meaningful on a non-ready Future.
- `needs_all` cancels siblings on the first failure; `wait_any` takes the first
  component to be ready — done or failed — and cancels the rest. You usually don't
  need to cancel manually inside a composition.
- A cancelled Future is *neither* done nor failed: `is_ready` is true, but `result`
  throws and `failure` returns nothing. Check `is_cancelled` if you need to distinguish.
- Cancel a Future from outside, never inside its own callback — the behaviour is
  undefined.

## Decision guide

| Situation | Use |
|---|---|
| Subclassing IO::Async object | `parent 'IO::Async::Notifier'`, override `configure` |
| Storing async state on $self | `$self->{_foo_future}` — never bare lexicals |
| Sequential dependent ops | `->then` / `async`+`await` |
| Parallel, all required | `Future->needs_all` |
| First-to-finish race | `Future->wait_any` |
| Add timeout to op | `wait_any($op, $loop->delay_future(after=>N)->then_fail('timeout'))` |
| Side-effect observation | `->on_done` / `->on_fail` (don't chain) |
| Truly fire-and-forget | `->retain` (rare — usually you should hold it) |
| Closure capturing $self | `weaken(my $weak = $self)` + null-check inside |
| Cancelling stale attempt | `delete $self->{_f}; $f->cancel unless $f->is_ready` |
| Sync block-wait (tests/scripts) | `$f->get` |
