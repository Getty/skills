# Future::AsyncAwait (`async` / `await`)

Read when writing or calling an `async sub`. Its lifetime rules — the caller holds the
returned Future, `return await $f` — are in SKILL.md.

```perl
use Future::AsyncAwait;

async sub fetch_user {
  my ($self, $id) = @_;
  my $row = await $self->db->query("SELECT ...", $id);
  my $perms = await $self->perms->for($id);
  return { %$row, perms => $perms };
}

# Caller MUST hold the returned Future:
my $f = $client->fetch_user(42);
my $user = await $f;        # ok
# OR:
my $user = await $client->fetch_user(42);   # also ok — await holds it
```

- **`@_` is not preserved across `await` on Perl < 5.24.** Unpack args into lexicals at
  the top of the sub.
- **`await` inside `map`/`grep` does not work.** Convert to a `for` loop with an
  accumulator.
