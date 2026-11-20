# Connect, reconnect and disconnect

Read when writing a client that opens a TCP connection with a protocol handshake or
reconnects after a drop, or when Net::Async::HTTP requests hang.

## TCP connect with a handshake (the GC trap)

```perl
async sub connect {
  my ($self) = @_;

  my $stream = IO::Async::Stream->new(
    on_read       => sub { $self->_on_read(@_) },
    on_read_eof   => sub { $self->_on_disconnect('read_eof') },
    on_read_error => sub { $self->_on_error("read: $_[1]") },
  );
  $self->{_stream} = $stream;
  $self->add_child($stream);

  # ⚠️ RETAIN the connect Future. If GC'd, the stream never gets its
  # handle and on_read never fires — silent hang.
  $self->{_tcp_connect_future} = $stream->connect(
    host    => $self->{host},
    service => $self->{port},
  )->on_fail(sub {
    my $err = shift;
    $self->{_connect_future}->fail("connect: $err")
      unless $self->{_connect_future}->is_ready;
  });

  $self->{_connect_future} = $self->loop->new_future;
  return await $self->{_connect_future};
}
```

**Why both futures?** `_tcp_connect_future` resolves when the *socket* is up.
`_connect_future` resolves when your *protocol handshake* is done. The handshake
completes inside `on_read`, so you need a separate Future to await.

Clean up `_tcp_connect_future` once the handshake succeeds
(`delete $self->{_tcp_connect_future}`).

## Reconnect without losing Futures

The reconnect path is where Future-lifetime bugs cluster. The wrong version is the
example in SKILL.md; right:

```perl
sub _reconnect_attempt {
  my ($self) = @_;
  return if $self->{_connected};

  weaken(my $weak = $self);

  $self->{_reconnect_future} = $self->loop
    ->delay_future(after => $self->{reconnect_wait})
    ->then(sub {
      my $self = $weak or return Future->done;
      return Future->done if $self->{_connected};
      return $self->connect;
    })
    ->on_done(sub {
      my $self = $weak or return;
      delete $self->{_reconnect_future};
    })
    ->on_fail(sub {
      my $self = $weak or return;
      delete $self->{_reconnect_future};
      $self->_reconnect_attempt;        # try again
    });
}
```

It applies the holding rules from SKILL.md: the whole chain lives in
`$self->{_reconnect_future}`, callbacks reach `$self` only through the weakened copy
(`use Scalar::Util qw(weaken);`), and both `on_done` and `on_fail` delete the held
Future.

- On disconnect, **fail the old `_connect_future`** so its async sub unwinds:
  ```perl
  if (my $f = delete $self->{_connect_future}) {
      $f->fail("disconnected: $reason") unless $f->is_ready;
  }
  ```

## Net::Async::HTTP: one failed connect, then every request hangs

Seen in Net::Async::HTTP 0.50: a module that dies while loading at connect time leaks
the host's connection slot. The first request fails; every later one to that host hangs
forever, with no error.

- The modules are loaded by name only when a connection opens:
  `IO::Async::Internals::Connector`, and for https `IO::Async::SSL` — so a missing
  `IO::Socket::SSL`/`Net::SSLeay`/libssl, or a PAR binary that didn't pack them,
  triggers it too.
- With the default `max_connections_per_host => 1` the slot never frees; raising it
  only postpones the hang.
- Before the first request, `require` those modules in an `eval` and fail with the
  module name.
- List `IO::Async::SSL` as a hard dependency whenever anything speaks https — upstream
  it is only a recommends.
- Redirects to https need the same check (`on_redirect` runs before the new connect).
