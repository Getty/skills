# LuaJIT and Luau: choose and port deliberately

Use when a host exposes LuaJIT or Luau, when performance motivates a runtime change, or when code described simply as “Lua” fails to parse or behave consistently. PUC-version details are in the language/runtime references; this file covers the two distinct implementation families.

## Contents

- [Record implementation identity](#record-implementation-identity)
- [LuaJIT](#luajit)
- [LuaJIT FFI and numerical boundaries](#luajit-ffi-and-numerical-boundaries)
- [Luau](#luau)
- [Porting and selection workflow](#porting-and-selection-workflow)
- [Sources](#sources)

## Record implementation identity

Record more than `_VERSION`: executable/library path, upstream project or vendor fork, commit/build, enabled features, OS/architecture, host-provided libraries, and bytecode/compiler version. A vendor-patched LuaJIT is not necessarily interchangeable with the upstream branch; a host embedding Luau decides which APIs scripts actually receive.

Choose based on an application requirement:

| Requirement | Candidate to evaluate | Evidence needed |
|---|---|---|
| Existing PUC 5.4/5.5 integration | Matching PUC runtime | Host ABI and extension support |
| Existing 5.1 ecosystem, native FFI, measured JIT benefit | LuaJIT 2.1 | Real workload profile, target JIT availability, dependency behavior |
| Typed scripting and an intentionally restricted embedded API | Luau | Host integration, accepted syntax/library differences, actual sandbox setup |
| Source shared across several hosts | Explicit common subset plus adapters | Tests on every supported runtime |

This is an evaluation matrix, not a speed ranking. Changing runtime also changes debugging, deployment, extension loading, and potentially the saved-data or module boundary.

## LuaJIT

As checked on 2026-11-22, upstream identifies **v2.1** as its production branch and uses rolling releases. The old `master` is pinned to v2.0; an old beta tag is not a reliable description of the currently maintained v2.1 code. Pin the tested commit and record `luajit -v` rather than silently following a moving branch. [Upstream status and release policy](https://luajit.org/status.html).

LuaJIT's baseline is Lua 5.1, including the 5.1 C API/ABI. It adds selected language/library features and extensions; partial 5.2 compatibility does not imply 5.3–5.5 compatibility. Inspect build options as well as code. [Extensions and compatibility](https://luajit.org/extensions.html).

Check syntax against the pinned commit. Current v2.1 documentation lists backported bit operators (`~`, `&`, `|`, `<<`, `>>`, `~>>`) and other LuaJIT syntax extensions; an older 2.1 build need not accept them. These operators use `bit.*` semantics, which differ from PUC integer bit operations. Test width, signedness, shift counts, and cdata conversions even when an expression parses on both runtimes. The documented 2.1 backports exclude floor division `//`, bit-operator metamethods, and named vararg parameters. Keep the 2.1 availability list separate from the broader 3.0 design document. [Current backports and bytecode restriction](https://luajit.org/extensions.html); [upstream operator semantics](https://github.com/LuaJIT/LuaJIT/issues/1475).

Practical porting rules:

- Parse source on the target before testing behavior. Later PUC syntax cannot be hidden behind a runtime `if` in a file that the older parser must read.
- Keep runtime-specific code in separate modules selected before loading.
- Review integer/bitwise operations, environment APIs, coroutine error/yield paths, and table/library helpers individually.
- Run native-module and FFI tests on the production architecture; source compatibility does not prove an ABI declaration.
- Verify the host actually enables JIT. Platform or build configuration can change execution mode.

Useful diagnostics from upstream:

```sh
luajit -v
luajit -jp workload.lua
luajit -jv workload.lua
luajit -joff workload.lua
```

The last command provides an interpreter comparison, not an alternative equivalent sandbox. `-jdump` can expose compilation details when trace behavior matters, but start with a profile rather than tuning the compiler blindly. [CLI](https://luajit.org/running.html); [profiler](https://luajit.org/ext_profiler.html).

Measure cold and warmed execution, trace churn/fallback, native time, GC time, and tail latency. A microbenchmark that remains inside one numeric loop cannot predict a host that performs thousands of reflected calls or blocking operations.

For untrusted inputs, read `sandboxing-and-capabilities.md` before selecting this backend. LuaJIT's upstream security position and compiled-code hook behavior require an explicit process-containment decision; interpreter mode alone does not establish a sandbox. [Official FAQ](https://luajit.org/faq.html).

## LuaJIT FFI and numerical boundaries

The FFI calls native C functions and manipulates C types from LuaJIT. It is part of LuaJIT, not a portable standard Lua package. [FFI overview](https://luajit.org/ext_ffi.html).

Before adding an FFI binding, document:

| Boundary | Required check |
|---|---|
| Declaration | Exact header type, alignment, calling convention, and platform variation |
| Buffer | Length, element count, read/write access, and owner |
| Pointer | Whether storage is retained; whether the pointed-to owner stays alive |
| Callback | Lifetime, thread of invocation, explicit freeing, reentrancy |
| Library | Lifetime at least as long as every function/cdata/callback using it |
| Numeric ID | Preservation across cdata, Lua number, serialization, and host conversion |

Do not convert a large 64-bit ID through an ordinary floating-point number and expect exact preservation. Keep a suitable integer/cdata representation at native boundaries and an explicit lossless external encoding where needed. Arithmetic and conversion rules depend on the cdata type; verify them in the FFI semantics rather than borrowing PUC 5.3 integer assumptions. [FFI conversions and operations](https://luajit.org/ext_ffi_semantics.html).

Pointers inside cdata do not root their pointed-to Lua allocations. Keep owners alive explicitly. Prefer explicit callback allocation when a callback needs eventual release. Avoid repeated implicit conversions that retain callbacks for the process lifetime. See `native-lifetime-and-async.md` for teardown.

Treat bytecode as implementation-specific build output. Follow upstream's exact compatibility conditions for branch/build modes; never send LuaJIT bytecode to a PUC or Luau loader. Source remains the simpler cross-runtime deployment representation when portability is needed. [LuaJIT bytecode controls](https://luajit.org/running.html#opt_b).

## Luau

Luau derives from Lua 5.1 but maintains its own language, compiler, VM, type system, and compatibility decisions. Features removed for isolation and features added for ergonomics make it a distinct target. The project's compatibility table is the authority for each later Lua feature; “based on 5.1” is not a complete contract. [Compatibility](https://luau.org/compatibility/); [project](https://github.com/luau-lang/luau).

Separate three concerns:

1. **Language:** typed declarations, Luau syntax/extensions, and its standard library.
2. **Runtime:** object lifetime, VM callbacks, compiler/bytecode interface, and performance behavior.
3. **Host:** filesystem/network access, module loading, scheduling, application objects, and permissions.

Do not assume standalone Luau contains a particular game platform's object model or task scheduler. Those APIs belong to the embedding host. Conversely, a restricted host can omit facilities present in a standalone executable.

Use Luau's analyzer for Luau source. LuaCATS comments in ordinary Lua and Luau's type syntax are different workflows. Type information does not validate external data at runtime; schema checks remain necessary where data enters the application.

The host API differs from PUC. Use the exact Luau headers/compiler/VM combination, configure the documented sandbox helpers when isolation is required, and supply interrupts/memory accounting. Luau uses host userdata destructors instead of the PUC `__gc` model. Port resource wrappers accordingly. [C API](https://luau.org/api/); [sandbox design](https://luau.org/sandbox/).

For performance, start with the optimized interpreter's profile. Luau documents table/import/closure optimizations, specialized libraries, and a native vector representation; apply those rules only to Luau. A PUC tuning recipe can conflict with Luau's compiler assumptions. [Performance design](https://luau.org/performance/); [profiling](https://luau.org/guides/profile/).

## Porting and selection workflow

1. Inventory syntax, library calls, C modules, FFI, environment manipulation, bytecode, and host globals.
2. Classify each dependency as portable, adapter-required, or unavailable on the proposed target.
3. Run syntax probes on isolated files for each supported language version.
4. Add semantic probes for numerical boundaries, table shapes, errors, callbacks, and resource closing.
5. Exercise the actual host path with production-shaped data.
6. Benchmark complete operations after correctness is established.
7. Retain the runtime change only if its benefit justifies the compatibility and operational cost.

A migration report must distinguish verified behavior, upstream documented behavior, vendor-specific behavior, and untested assumptions. Avoid a blanket “Lua compatible” label.

## Sources

Checked 2026-11-22:

- LuaJIT: [status](https://luajit.org/status.html), [extensions](https://luajit.org/extensions.html), [syntax-extension semantics](https://github.com/LuaJIT/LuaJIT/issues/1475), [FAQ](https://luajit.org/faq.html), [CLI](https://luajit.org/running.html), [profiler](https://luajit.org/ext_profiler.html), [FFI](https://luajit.org/ext_ffi.html), [FFI semantics](https://luajit.org/ext_ffi_semantics.html).
- Luau: [project](https://github.com/luau-lang/luau), [compatibility](https://luau.org/compatibility/), [API](https://luau.org/api/), [sandbox](https://luau.org/sandbox/), [performance](https://luau.org/performance/), [profiling](https://luau.org/guides/profile/).
