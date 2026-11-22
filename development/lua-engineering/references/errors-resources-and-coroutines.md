# Errors, deterministic cleanup, and coroutine lifecycle

Scope: PUC Lua with explicit version gates. Reviewed 2026-11-22. Cancellation and error policy belong to the host/application; use Lua mechanisms to implement that policy deliberately.

## Contents

- [Choose an error contract](#choose-an-error-contract)
- [Protected boundaries and tracebacks](#protected-boundaries-and-tracebacks)
- [Resource cleanup](#resource-cleanup)
- [Coroutines are cooperative execution](#coroutines-are-cooperative-execution)
- [Cancellation and failed coroutines](#cancellation-and-failed-coroutines)
- [Acceptance cases](#acceptance-cases)

## Choose an error contract

Use one documented convention per API boundary:

| Kind of outcome | Suitable shape | Caller responsibility |
|---|---|---|
| Expected absence or rejection | `nil, reason` or a structured result | Branch deliberately |
| Successful boolean false | `false` as a documented value | Do not confuse with transport/protected-call status |
| Broken invariant/programming error | Raised error | Catch at a meaningful outer boundary |
| Host resource failure | Explicit status plus native detail | Preserve error code and ownership state |
| Cancellation | Dedicated status/error kind | Release owned resources and suppress inappropriate retries |

`pcall` returns its own success flag followed by results or the error object. That flag is distinct from the called function's first result. Error objects need not be strings. Lua 5.5 normalizes a nil error object to a message; do not apply that assumption to older versions. [5.1 pcall](https://www.lua.org/manual/5.1/manual.html#pdf-pcall), [5.5 incompatibilities](https://www.lua.org/manual/5.5/manual.html#8.1).

Keep an error's original structured payload when it carries useful diagnostics. Do not convert every rejection into an exception, and do not swallow every exception to keep an event loop running without a defined degraded state.

## Protected boundaries and tracebacks

Use `xpcall` when a traceback must be captured before unwinding loses context. A closure adapts arguments portably, including PUC 5.1 where `xpcall` does not accept the later argument-forwarding form. The handler itself must remain simple. [5.1 xpcall](https://www.lua.org/manual/5.1/manual.html#pdf-xpcall), [5.4 error handling](https://www.lua.org/manual/5.4/manual.html#2.3).

```lua
-- Requires a trusted host exposing debug.traceback; PUC 5.1–5.5.
local function describe_error(err)
    return { cause = err, trace = debug.traceback('', 2) }
end
local ok, outcome = xpcall(function()
    error({ code = 'invalid_recipe', recipe = 'mill' }, 0)
end, describe_error)
assert(not ok)
assert(outcome.cause.code == 'invalid_recipe')
assert(type(outcome.trace) == 'string')
```

Do not assume that stringifying an arbitrary error is harmless: `tostring` can invoke a metamethod. A robust outer diagnostic path can preserve type and identity while applying bounded, protected formatting separately. Keep the original fault if formatting or cleanup also fails. [tostring](https://www.lua.org/manual/5.4/manual.html#pdf-tostring), [base-library protected-call implementation](https://www.lua.org/source/5.5/lbaselib.c.html#luaB_xpcall).

Choose protected boundaries at requests, jobs, plugin calls, or top-level script entry points. Repeatedly catching errors inside every small function hides where an invariant was violated and adds ambiguous partial-success states.

## Resource cleanup

For PUC 5.4+, `<close>` provides scope-exit cleanup through `__close`, including ordinary return and error unwinding. Closing proceeds in reverse declaration order. A close-bound variable is read-only; nil and false are accepted without invoking a close operation. [5.4 to-be-closed variables](https://www.lua.org/manual/5.4/manual.html#3.3.8).

```lua
-- PUC Lua 5.4+ only.
local released = false
do
    local guard <close> = setmetatable({}, {
        __close = function(_, err)
            released = true
            -- err is nil/no argument on normal close; do not infer success
            -- solely from whether a message string is present.
        end,
    })
end
assert(released)
```

Use explicit close/result checks when flush or commit errors must be reported. `__gc` finalization is not a substitute for a timely close or successful transaction commit. For file output, check the write result and the close result according to the file API. [I/O contracts](https://www.lua.org/manual/5.4/manual.html#6.8), [I/O implementation `f_close`, `f_write`](https://www.lua.org/source/5.5/liolib.c.html#f_close).

On older Lua, write a bounded acquire/use/release helper around a protected call. Specify whether the body can yield, whether release can fail, and which error is primary. A helper that discards cleanup failure or masks the body failure is incomplete. C++ destructors and native exceptions require the embedding-specific guidance; do not infer their behavior from Lua `<close>`.

## Coroutines are cooperative execution

A coroutine suspends and resumes a Lua execution stack. It does not itself provide OS-thread parallelism, nonblocking I/O, an event loop, a timer service, or automatic cancellation. Those are host/application responsibilities. Coroutines in one state share reachable objects and globals. [Coroutine model](https://www.lua.org/manual/5.4/manual.html#2.6).

```lua
local co = coroutine.create(function(initial)
    local next_value = coroutine.yield(initial + 1)
    return next_value * 2
end)
local ok1, yielded = coroutine.resume(co, 4)
assert(ok1 and yielded == 5)
local ok2, result = coroutine.resume(co, 7)
assert(ok2 and result == 14)
assert(coroutine.status(co) == 'dead')
```

Separate the two directions of data flow: resume arguments become function/yield results inside the coroutine; yielded values become resume results outside it. Check the status flag on every resume. `normal` means a coroutine has resumed another coroutine and is waiting, not that it is available to resume arbitrarily. [Coroutine library](https://www.lua.org/manual/5.1/manual.html#5.2), [current `auxresume`/`auxstatus`](https://www.lua.org/source/5.5/lcorolib.c.html#auxresume).

Yieldability depends on the runtime and call boundary. PUC 5.1 restrictions differ from later versions; C functions require the applicable continuation APIs to survive a yield. A callback accepted by a host does not automatically become yieldable. [5.2 continuation model](https://www.lua.org/manual/5.2/manual.html#4.7).

## Cancellation and failed coroutines

Suspension can retain local variables and resources. In PUC 5.4, a coroutine that errors does not automatically unwind and close its pending close variables merely because `resume` returned false. Explicit `coroutine.close` closes a dead or suspended coroutine and reports errors. The `coroutine.wrap` error path has its own closing behavior. [5.4 cleanup details](https://www.lua.org/manual/5.4/manual.html#3.3.8), [coroutine.close](https://www.lua.org/manual/5.4/manual.html#pdf-coroutine.close).

In PUC 5.5, omitting the argument to `coroutine.close()` selects the running coroutine; closing it does not return to that Lua caller. The equivalent C self-close path also exits nonlocally. Do not assume 5.4's required-argument or suspended/dead-only contract when writing cancellation wrappers. The official 5.5.1 bug list, reviewed 2026-11-22, includes self-close problems during error cleanup and garbage collection; review patch status and test the selected close path before using it in a host lifecycle. [5.5 close semantics](https://www.lua.org/manual/5.5/manual.html#pdf-coroutine.close), [C self-close](https://www.lua.org/manual/5.5/manual.html#lua_closethread), [patch errata](https://www.lua.org/bugs.html#5.5.1).

A useful task record includes a task ID, owner/session, status, cancellation token, pending host operation, and cleanup responsibility. On cancellation:

1. Prevent new scheduling and mark the task's intended terminal state.
2. Cancel or detach the pending host operation through its API.
3. At an allowed boundary, close a suspended coroutine where the runtime supports it.
4. Check and record close errors while preserving the original cancellation/failure.
5. Remove subscriptions and references so the task can be collected.

Closing a coroutine does not retroactively cancel a socket operation, native worker, or engine callback. Host callbacks must reject stale task generations or resolve cancellation races deliberately. A timeout policy also needs a clock source and a rule for work already committed externally.

## Acceptance cases

Test success, expected rejection, thrown table/string error, error in the message handler, cleanup failure, suspended cancellation, resume after completion, nil-bearing multiple results, and a callback arriving after cancellation. Run tests through the actual host boundary if yielding or native resources are involved. Record which failures are recoverable and which terminate the containing request, task, or session.
