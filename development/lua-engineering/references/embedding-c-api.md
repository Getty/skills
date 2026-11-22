# Embedding Lua through the C API

Use for adding a Lua runtime to a native application, reviewing bindings, or diagnosing stack and call failures. Baseline examples target **PUC Lua 5.4/5.5**; LuaJIT and Luau require their own API contracts.

## Contents

- [Establish the host contract](#establish-the-host-contract)
- [Stack discipline](#stack-discipline)
- [Protected calls and error objects](#protected-calls-and-error-objects)
- [Binding data without accidental coercion](#binding-data-without-accidental-coercion)
- [State, allocation, and library exposure](#state-allocation-and-library-exposure)
- [Porting a native host from 5.4 to 5.5](#porting-a-native-host-from-54-to-55)
- [Yielding and concurrency](#yielding-and-concurrency)
- [Choosing a host binding](#choosing-a-host-binding)
- [Review and sources](#review-and-sources)

## Establish the host contract

Before writing bindings, record the exact runtime headers/library, numeric configuration, exception model, host thread, and ownership of every transferred value. Agree whether a callback may yield, reenter the host, retain a parameter, fail, or outlive the caller. These are API design decisions; Lua syntax does not resolve them.

Treat the Lua state as part of an application/session lifecycle. A documented owner creates it, installs capabilities, loads modules, dispatches work, cancels outstanding work, releases references, and closes it. Keep state pointers out of unrelated global singletons.

Build `assets/minimal_host.c` against a matching runtime. It is a synchronous **trusted-script** example: all standard libraries are opened, source files are loaded in text mode, and failures return a nonzero process status. Extend it only after documenting which properties must change.

Its diagnostics intentionally simplify failures: a loader error rethrown through `lua_error` is reported with the enclosing protected call's runtime-error status; the original parser/file status is not retained. The traceback handler replaces non-string payloads with a message and passes string errors through a NUL-terminated traceback API, so it does not preserve arbitrary binary error data. A production error protocol that needs exact status, type or bytes must retain those separately before formatting.

## Stack discipline

The C API communicates through a stack. Positive indices count from the call frame's bottom; negative indices move with the top. An index that was correct before a push can refer to another value afterward. `lua_absindex` stabilizes an acceptable relative index; it does not keep an object alive after its stack slot is removed. [C API, §4.1](https://www.lua.org/manual/5.4/manual.html#4.1); [implementation: `index2value`, `lua_absindex`](https://www.lua.org/source/5.5/lapi.c.html).

Use the following review convention:

| Boundary | Record explicitly |
|---|---|
| Native function called from Lua | Accepted argument positions/types; pushed results; returned result count |
| Host calling Lua | Initial top; callable position; argument count; result count; handler index |
| Helper touching the stack | Stack delta on success and every failure path |
| Temporary lookup | Whether a metamethod may execute; whether the lookup can fail or allocate |
| Retained value | Registry reference or another strong Lua root; its release point |

For helpers that promise a balanced stack, compare `lua_gettop` on entry and exit in diagnostic builds. Reserve capacity with `lua_checkstack` when constructing variable-sized calls. Do not substitute a C array bounds check for a Lua stack check.

Use the API documentation's `[-pops, +pushes, errors]` annotations while reviewing a function sequence. Avoid guessing stack effects from a function name. In 5.4+, operations that remove to-be-closed slots can run closing methods; a generic stack reset is not universally free of user code. Inspect `lua_settop` and `lua_closeslot` in the matching manual. [API implementation](https://www.lua.org/source/5.5/lapi.c.html#lua_settop).

## Protected calls and error objects

`lua_pcall` returns a status and preserves either results or an error object. The error object need not be a string. A message handler can collect a traceback before the Lua call stack unwinds; it is not invoked for every class of failure, including memory errors. Unprotected errors can reach the panic handler and terminate the host. [Error handling](https://www.lua.org/manual/5.5/manual.html#4.4); [`luaD_throw`, `luaD_pcall`](https://www.lua.org/source/5.5/ldo.c.html).

Design the boundary to cover **preparation as well as execution**. Calling `lua_pcall` around the final function does not protect an earlier allocating API operation. A useful pattern is a small C thunk invoked through `lua_pcall`; the thunk performs initialization, loading, marshaling, and the Lua call inside that protected region. The bundled host demonstrates this pattern.

For error reporting:

1. Preserve the original operation and context in host data.
2. Capture traceback inside a message handler when available.
3. Render known string errors directly; report other values by type or through an explicitly safe serializer.
4. Copy diagnostic data before removing its Lua root or closing the state.
5. Keep the error path small enough to work under allocation pressure.

Avoid blindly calling `tostring` on an error object: that can invoke another user-defined metamethod. Error handlers can fail too. Treat an error status as a failed operation, not as proof that the application state was rolled back.

## Binding data without accidental coercion

Write down the marshaling policy before choosing convenient helpers:

| Data | Binding decision |
|---|---|
| Integer ID | Require an integer subtype or validate range/integrality deliberately; do not round an arbitrary number |
| Boolean | Distinguish a required boolean from Lua truthiness |
| Binary/string data | Use length-aware APIs; embedded NUL is valid data |
| Optional argument | Decide separately what absence and explicit `nil` mean |
| Array | Accept a documented dense sequence or an explicit count; reject ambiguous holes where required |
| Record | Validate known fields and unknown-field policy; avoid surprise metamethod execution during validation |
| Native object | Specify owned, borrowed, shared, or ID-based lifetime; see the native-lifetime reference |

`lua_isnumber` and checking helpers can accept conversions that a strict schema might reject. A type contract that says “number only” should first inspect the actual value type. `lua_tolstring` returns a Lua-owned pointer and may convert numbers; retain the Lua value or copy the bytes before storing them elsewhere. Exact conversions are defined in the API, not by C casts. [Conversion implementation: `lua_tonumberx`, `lua_tointegerx`, `lua_tolstring`](https://www.lua.org/source/5.5/lapi.c.html).

Raw table operations are useful when the contract requires raw storage semantics. They do not validate a domain object or turn a mutable table into a safe capability.

## State, allocation, and library exposure

Use `luaL_newstate` for ordinary initialization. A custom allocator is appropriate when memory accounting or allocation control is required. It must honor Lua's allocation contract, including realloc-like failure behavior. In **5.5**, `lua_newstate` has an added hash seed parameter; a 5.4 two-argument call must be ported deliberately. [5.5 state API](https://www.lua.org/manual/5.5/manual.html#lua_newstate); [`lua_newstate` source](https://www.lua.org/source/5.5/lstate.c.html#lua_newstate).

Do not expose all libraries by habit in an embedded product. Decide whether scripts need filesystem, processes, dynamic libraries, debugging, clocks, and module search paths. Opening selected libraries still leaves the host responsible for its own functions. Read `sandboxing-and-capabilities.md` for hostile or user-supplied scripts.

## Porting a native host from 5.4 to 5.5

Rebuild the runtime and every native consumer from matching headers. Regenerate FFI declarations and review manually copied constants, struct layouts, symbol lookup and address-taking code. In 5.5, registry/GC constants and `lua_Debug` layout differ, `luaL_openlibs` and the compatibility `lua_resetthread` are macros, and `lua_setcstacklimit` is no longer declared. A successful link alone does not validate a hand-written binding. Compare [5.4 lua.h](https://www.lua.org/source/5.4/lua.h.html), [5.5 lua.h](https://www.lua.org/source/5.5/lua.h.html), and [5.5 lualib.h](https://www.lua.org/source/5.5/lualib.h.html).

Three behavioral changes deserve dedicated review:

- `lua_pushvfstring` returns NULL and leaves an error message on failure in 5.5; it no longer raises the error itself. `lua_pushfstring` still raises errors. A wrapper must handle the correct contract before using the returned pointer, and finish `va_end` before propagating an error through a nonlocal exit. [Formatting API](https://www.lua.org/manual/5.5/manual.html#lua_pushvfstring).
- `lua_gc(L, LUA_GCSTEP, ...)` takes an `int` in Kbytes in 5.4 and a `size_t` in bytes in 5.5. Port both units and variadic argument type; stale code may compile without diagnosing the mismatch. [5.4 GC API](https://www.lua.org/manual/5.4/manual.html#lua_gc), [5.5 GC API](https://www.lua.org/manual/5.5/manual.html#lua_gc).
- `lua_closethread(L, L)` closes the running coroutine without returning to the caller and requires a resume context. Account for this nonlocal exit in native lifetime design; it is not an ordinary cleanup call. [Coroutine API](https://www.lua.org/manual/5.5/manual.html#lua_closethread).

Also record `LUA_FAILISFALSE` when an embedding enables it: it changes `luaL_pushfail` from its default nil result to false. This affects schemas that distinguish those values. See [5.5 lauxlib.h](https://www.lua.org/source/5.5/lauxlib.h.html) and the complete [5.5 migration reference](lua55-changes.md). Review the selected patch's [known bugs](https://www.lua.org/bugs.html) before relying on new closing or GC paths.

## Yielding and concurrency

A callback that can suspend requires a yield-aware host protocol. In PUC Lua, continuation APIs (`lua_callk`, `lua_pcallk`, `lua_yieldk`) exist because a yield cannot return through an ordinary suspended C frame. A continuation receives explicit context; native stack locals are not durable async storage. [Yielding in C](https://www.lua.org/manual/5.5/manual.html#4.5).

Treat a state and its coroutines as owned by one execution thread unless the selected embedding's concurrency contract explicitly permits another arrangement. Queue native completion messages to that owner. Independent states are appropriate when isolation or parallel execution is required; exchanging Lua pointers between independent states is not serialization.

## Choosing a host binding

These are evaluation routes, not automatic compatibility promises:

| Host | Primary project | Evaluate first |
|---|---|---|
| C | [PUC C API](https://www.lua.org/manual/5.5/manual.html#4) | Explicit stack/lifetime/error control |
| C++ | [sol](https://sol2.readthedocs.io/en/latest/) | Protected call policy, usertype ownership, exceptions, exact Lua version |
| Rust | [mlua](https://github.com/mlua-rs/mlua) | Selected runtime feature, async/send options, userdata borrowing, vendored/system linkage |
| Python | [Lupa](https://github.com/scoder/lupa) | Explicit runtime module, object exposure, conversion and lifetime boundaries |
| Go | [GopherLua](https://github.com/yuin/gopher-lua) | Separate Go VM/compiler and its compatibility limits; do not assume PUC native-module support |

Read the wrapper's current build/features documentation before producing setup commands. A wrapper can hide stack bookkeeping while still exposing a dangerous native capability or permitting stale host references.

## Review and sources

For a binding change, exercise correct input, incorrect type, error object, repeated call, callback retention, host destruction, and any claimed yield path. For a native crash, reduce to one state and one binding before attributing it to Lua.

Primary sources checked 2026-11-22:

- [PUC 5.4 C API](https://www.lua.org/manual/5.4/manual.html#4) and [PUC 5.5 C API](https://www.lua.org/manual/5.5/manual.html#4).
- [5.5.1 `lapi.c`](https://www.lua.org/source/5.5/lapi.c.html), [`ldo.c`](https://www.lua.org/source/5.5/ldo.c.html), [`lauxlib.c`](https://www.lua.org/source/5.5/lauxlib.c.html), [`lstate.c`](https://www.lua.org/source/5.5/lstate.c.html).
- Host projects are linked individually in the selection table. Their moving default branches must be pinned before an integration is declared tested.
