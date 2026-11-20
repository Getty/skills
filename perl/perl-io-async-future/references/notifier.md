# Notifier subclasses, the loop and tests

Read when writing an `IO::Async::Notifier` subclass (a Net::Async::* client or server),
running the loop from a script, or testing async code. The `configure` chaining and
`$self->loop` traps are in SKILL.md.

## Notifier subclass skeleton

```perl
package Net::Async::Foo;
use strict;
use warnings;
use parent 'IO::Async::Notifier';

use Future;
use Future::AsyncAwait;
use IO::Async::Stream;

sub configure {
  my ($self, %params) = @_;
  for my $key (qw(host port on_connect on_error)) {
    $self->{$key} = delete $params{$key} if exists $params{$key};
  }
  $self->{host} //= 'localhost';
  $self->SUPER::configure(%params);   # MUST chain — unknown keys die here
}

sub host { $_[0]->{host} }
```

- Parameter validation and defaults go in `configure`, **not** `new` — the Notifier owns
  construction.
- Child notifiers (`IO::Async::Stream`, `IO::Async::Timer`) attach via
  `$self->add_child($child)`; they inherit the loop automatically.
- Create Futures with `$self->loop->new_future`, not `Future->new`, when you need
  loop-aware behaviour: the loop variant integrates with timeouts and is the
  recommended form inside Notifier subclasses.

## Loop, sync waits and tests

```perl
use IO::Async::Loop;
my $loop = IO::Async::Loop->new;
$loop->add($client);

# Block-wait on a Future from sync code (test code, main script):
my @result = $client->connect->get;

# Run loop until a Future is ready (older style):
$loop->await($f);
```

Test pattern:

```perl
use Test::More;
use IO::Async::Test;
use IO::Async::Loop;

my $loop = IO::Async::Loop->new;
testing_loop($loop);                # IO::Async::Test hook

my $client = MyClient->new(...);
$loop->add($client);

my $f = $client->do_thing;
wait_for_future($f);                # spins the loop
ok($f->is_done, 'completed');
is_deeply([$f->result], [...]);
```
