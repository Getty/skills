# Testing and debugging

## Contents

- Establish what is actually running
- Choose useful test boundaries
- Diagnose semantics and modules
- Debug native boundaries and performance
- Use the bundled utilities
- Record verification limits

## Establish what is actually running

Record interpreter path, exact version/build, numeric configuration, host, module roots and native extension versions. _VERSION identifies a language version but may not identify a patch release or a host fork. Use build metadata as well. Read versions-and-portability.md before interpreting a mismatch.

Run a minimal reproduction under the failing host. A standalone interpreter can isolate language behavior, but it cannot reproduce missing engine libraries, lifetime rules or a different Lua ABI. Compile every relevant source with the target parser before attributing a syntax failure to business logic.

If valid new syntax is rejected only by tooling, inspect parser support. If code runs only in an editor, inspect staged files, case-sensitive paths, dependency availability and host startup.

## Choose useful test boundaries

Prefer observable contracts: rejected command leaves state unchanged, resources release on failure, callback never touches a destroyed context, serialization preserves IDs, and a module produces the documented result count.

| Boundary | Representative cases |
|---|---|
| Pure function | Normal input, empty input, false/nil, numeric boundaries |
| Mutable operation | Success, validation rejection, partial-work failure policy |
| Module loader | Missing module, cache, reload and retained references |
| Coroutine | Yield/resume values, error, cancellation, non-yieldable boundary |
| Persistence | Round trip, old version, malformed/truncated input |
| Native callback | Ownership, error conversion, teardown, stack balance |
| Async adapter | Timeout, duplicate/stale completion, cancellation |

Use the project's framework. Busted provides a Lua testing framework; LuaUnit provides xUnit-style assertions and several report formats. Verify their installed versions and dependency compatibility rather than assuming every new Lua syntax is supported. [Sources: Busted](https://github.com/lunarmodules/busted), [LuaUnit](https://github.com/bluebird75/luaunit).

For a small pure module, dependency-free assertions may be enough. Avoid building a framework just to test a few invariants. Add generated/property cases only when they explore a meaningful domain risk; keep seeds and failure inputs reproducible.

Inject time, RNG and I/O for deterministic tests. Do not globally replace standard functions across parallel tests unless isolation and restoration are controlled. Keep independent instances to detect leaked module/global state.

## Diagnose semantics and modules

Reduce the input before rewriting an algorithm. Common causes include a false value replaced by an or default, a lost nil in varargs, a hole in a sequence, a method called with dot instead of colon, shadowed locals, an unexpectedly shared table or stale require cache.

Inspect value types and result counts at boundaries. A function returning nil, error is different from returning false or throwing. Lua allows arbitrary error values. Traceback construction must respect this; avoid executing an untrusted __tostring handler while reporting a failure. [Sources: errors](https://www.lua.org/manual/5.5/manual.html#2.3), [debug.traceback](https://www.lua.org/manual/5.5/manual.html#pdf-debug.traceback).

For module errors, log the requested module name and controlled search configuration. Check spelling/case, root selection, package.loaded/preload, C entry-point naming and native ABI. Do not fix a missing module by blindly appending every directory to package.path/cpath.

For reload bugs, identify who still holds the old function/table and whether it captures old upvalues. Clear ownership or replace a stable dispatch indirection deliberately. Restarting a clean VM can distinguish stale state from source behavior.

## Debug native boundaries and performance

Assert stack-height contracts around C entry points in debug builds. Trace reference ownership and callback registration/unregistration. Reproduce invalid handles after destruction; force collection in a controlled test if it helps expose retained or prematurely released references.

Use platform sanitizers/debuggers where the native toolchain supports them. A Lua traceback cannot diagnose every C heap corruption or C++ longjmp problem. Preserve symbolized native stacks and exact build identity.

Profile separately: Lua execution, host calls, allocations/GC, I/O waits and application queues. Warm up JIT-dependent paths when measuring them; keep cold-start results if startup matters. Observe real throughput/tail latency before adding caches or data-layout changes. Read performance-and-gc.md.

## Use the bundled utilities

runtime_probe.lua reports implementation-visible features and compiles trusted syntax probes without executing them. It does not discover every host restriction or certify conformance. semantic_checks.lua verifies language traps and the original rules example. Neither imports the user's project or downloads dependencies.

run_lua_checks.py runs both with explicit executable paths, clears LUA_INIT startup variables and uses a bounded timeout. It emits JSON with stdout, stderr and exit status for each selected runtime. Run from any directory through the Python wrapper; direct Lua checks expect this skill directory as the working directory.

~~~sh
python3 scripts/run_lua_checks.py --lua /path/to/lua54 --lua /path/to/lua55
~~~

The rules fixture accepts trusted plain tables, uses a documented 2^31-1 quantity cap, and makes no writes when validation returns a rejection. It is not a concurrent transaction engine and does not promise rollback after process termination or memory exhaustion.

## Record verification limits

Use precise status labels: parsed, unit-tested, exercised in host, packaged, platform-tested. State which runtimes were actually executed and which were only source-reviewed. A Python validator cannot prove Lua runtime behavior; a Lua test cannot prove a C++ plugin compiles.

For defects, retain the smallest failing input, expected/observed result, runtime/build and command. For performance, retain workload size, machine, warmup, measurement method and enough repetitions to understand variation. Stop testing when the concrete remaining risk is resolved.
