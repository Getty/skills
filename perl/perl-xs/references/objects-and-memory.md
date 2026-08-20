# Objects and memory

An XS object is a C pointer that has to survive in a garbage-collected language and
be released exactly once, at a moment Perl chooses. That is what magic is for.

## The layout

Two typedefs, each doing a different job:

```c
typedef struct {
    ssh_session   session;
    unsigned int  generation;
} NLSS_Session;                     /* named, so Newxz has a size to allocate */

typedef NLSS_Session *Net__LibSSH;  /* pointer typedef xsubpp uses in generated C */
```

The struct is named so `Newxz(RETVAL, 1, NLSS_Session)` compiles. The second is a
**pointer** typedef, which is why `Net::LibSSH self` in an XS signature carries no
`*`. Its name is the class with `::` written `__`, because that is what xsubpp
emits into C.

Wrap the C handle in your own struct even when it is the only field. Everything
learned later — a generation counter, a flag, a cached SV — needs somewhere to go,
and widening a struct is a local change while replacing a bare handle is not.

## Allocation and release

| Task | Use | Not |
|---|---|---|
| allocate | `Newx(ptr, n, type)` / `Newxz` (zeroed) | `malloc` |
| free | `Safefree(ptr)` | `free` |
| grow | `Renew(ptr, n, type)` | `realloc` |

Perl's allocators are the ones Perl's own debugging and memory accounting see.
`Newxz` zeroes, which is worth taking: a state enum whose zero value is the initial
state costs nothing to initialise.

## The free hook

```c
static int nlss_session_free(pTHX_ SV *sv, MAGIC *mg) {
    NLSS_Session *self = (NLSS_Session *)(void *)mg->mg_ptr;
    if (self->session) { ssh_disconnect(self->session); ssh_free(self->session); }
    Safefree(self);
    return 0;
}
static const MGVTBL Net__LibSSH_magic = { .svt_free = nlss_session_free };
```

`svt_free` runs when the SV is collected. It beats a Perl `DESTROY` on three counts:
it cannot be overridden by a subclass, it still runs during global destruction, and
`CLONE_PARAMS` handling has a place to go (`svt_dup`) if threads ever matter.

The vtable is `static const` and its **address is the type identity** — declare one
per class, never share a vtable between two types.

## Attaching and finding

```c
/* OUTPUT side, in the typemap: bless an SV and hang the pointer off it */
sv_magicext(newSVrv($arg, "Net::LibSSH"), NULL, PERL_MAGIC_ext,
            &Net__LibSSH_magic, (const char *)$var, 0);

/* INPUT side: retrieve, and refuse anything else */
MAGIC *mg = SvROK(sv) && SvMAGICAL(SvRV(sv))
    ? mg_findext(SvRV(sv), PERL_MAGIC_ext, &Net__LibSSH_magic) : NULL;
```

`newSVrv` creates the referent and returns it; the magic goes on **the referent**,
not on the reference. `mg_findext` therefore takes `SvRV(sv)`. Getting this level
wrong is the single most common source of "not a valid object" croaks on objects
that are perfectly valid.

`mg_findext` needs `#define NEED_mg_findext` before `ppport.h` on Perls before 5.14.

## Child objects: the refcount chain

A channel opened on a session must not outlive that session's C handle. The child
holds an owning reference:

```c
RETVAL->session_sv         = SvREFCNT_inc(SvRV(ST(0)));   /* construction */
…
SvREFCNT_dec(self->session_sv);                            /* in the child's svt_free */
```

**Increment `SvRV(ST(0))`, not `ST(0)`.** `ST(0)` is the reference scalar — the
caller's `$ssh` variable; the referent is the blessed, magic-bearing SV whose
`svt_free` calls the C teardown. Holding the reference keeps the referent alive only
as long as the reference still points at it:

| what happens to the parent variable | ref held on `ST(0)` | ref held on `SvRV(ST(0))` |
|---|---|---|
| goes out of scope | works | works |
| `undef $ssh` | **SIGSEGV** | works |
| `$ssh = something_else` | **SIGSEGV** | works |

Note which case survives the bug: the one a test writes first. Cover all three ways
of losing the variable, per child type, and run each in a forked child so a segfault
fails the test instead of taking the suite with it.

Dereferencing `ST(0)` inside the XSUB is safe: the typemap's INPUT block has already
croaked unless `SvROK(sv) && SvMAGICAL(SvRV(sv))`, and OUTPUT overwrites `ST(0)`
only afterwards.

## When the C library frees your children behind your back

Some teardown calls free objects the Perl side still holds pointers to —
`ssh_disconnect()` frees every channel the session owns. A NULL check cannot see it:
the pointer is unchanged and now points at freed memory.

The fix is a **generation counter**. The parent counts the events that invalidate
children; each child stores the count it was born under:

```c
/* parent, before the invalidating call */
self->generation++;
ssh_disconnect(self->session);

/* child, before touching its handle */
static int nlss_session_stale(pTHX_ SV *session_sv, unsigned int generation) {
    MAGIC *mg = session_sv && SvMAGICAL(session_sv)
        ? mg_findext(session_sv, PERL_MAGIC_ext, &Net__LibSSH_magic) : NULL;
    if (!mg) return 1;                       /* no magic → not ours → refuse */
    return ((NLSS_Session *)(void *)mg->mg_ptr)->generation != generation;
}
```

Two rules make it hold:

- **Bump before the call that frees**, so no window exists where a child looks live
  and its memory is gone.
- **A stale child's `svt_free` skips only the C teardown** — it still releases its
  reference on the parent and still `Safefree`s its own struct. Skipping the whole
  body trades a crash for a leak.

The parent's own `svt_free` needs no bump: every child holds a reference on it, so
it runs only once the last child is gone.

## Returning undef

`XSRETURN_UNDEF` returns immediately and **skips the OUTPUT section**. That makes it
the way to say "no object" — and a leak whenever `RETVAL` was already allocated, or
the C resource already created, on that path:

```c
ssh_channel ch = ssh_channel_new(self->session);
if (!ch)
    XSRETURN_UNDEF;
if (ssh_channel_open_session(ch) != SSH_OK) {
    ssh_channel_free(ch);          /* free before returning, or it leaks */
    XSRETURN_UNDEF;
}
Newxz(RETVAL, 1, NLSS_Channel);    /* allocate only once nothing can fail */
```

Allocating last is the discipline that makes those branches trivially correct.

## Guarding a closed handle

After an explicit `close`, set the C handle to `NULL` and croak from every other
method. This is not defensive noise: many C libraries accept a NULL handle and
return a plausible wrong answer — `-1` from an exit-status call, `""` from a read —
so a missing guard produces wrong data rather than a crash, and testing does not
catch it.

Keep exactly one method unguarded: `close` itself, so it stays idempotent and the
`svt_free` path can walk the same code.

Give "the caller closed this" and "the parent was torn down" **different croak
messages**. Collapsing them leaves the caller unable to tell its own teardown from
the library's.
