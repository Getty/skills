# PUC Lua 5.5: applying new features without breaking the host

Reviewed 2026-11-22 against the official 5.5.1 documentation and source. This is a migration/reference module, not an instruction to upgrade every embedded runtime.

## Contents

- [Version contract](#version-contract)
- [Global declarations](#global-declarations)
- [Named vararg tables](#named-vararg-tables)
- [Loop variables and library changes](#loop-variables-and-library-changes)
- [Embedding and GC changes](#embedding-and-gc-changes)
- [Patch-specific defects](#patch-specific-defects)
- [Migration acceptance](#migration-acceptance)

## Version contract

Lua 5.5.0 was released 2025-12-22; the official current release at review time is 5.5.1. The current 5.5 manual is the language authority. The [release overview](https://www.lua.org/manual/5.5/readme.html#changes) lists features, while [manual §8](https://www.lua.org/manual/5.5/manual.html#8) lists incompatibilities. Keep the runtime's patch release and compile options in the build manifest.

A host embedding 5.4 does not gain these features when a separate system CLI is updated. Parser, C API, native modules, bytecode, and application semantics must be considered together. [Version/ABI policy](https://www.lua.org/versions.html).

## Global declarations

Lua 5.5 introduces `global` as a reserved word. A chunk initially has an implicit permissive global declaration; using an explicit global declaration changes name checking in its lexical scope. Global declarations without initializers leave existing values unchanged. An initializer for an already non-nil global raises a runtime error. [Environment/name rules](https://www.lua.org/manual/5.5/manual.html#2.2), [variable declarations](https://www.lua.org/manual/5.5/manual.html#3.3.7).

```lua
-- PUC Lua 5.5 only: declare the global names this chunk reads.
global <const> assert, math
local result = math.floor(3.8)
assert(result == 3)
```

This is useful for detecting accidental free names in controlled code. It is lexical checking, not object immutability or a security boundary: a constant binding to `math` does not freeze the table, and a referenced function can still have side effects. Explicit `_ENV` access also has its own meaning.

Do not insert `global print` into a large file without enumerating other free names in its affected scope. Previously permitted accidental globals may become compile errors. Test migration at module boundaries, and agree whether declarations are an application convention or merely an optional feature.

Existing source that uses `global` as an identifier must change or deliberately use the compatibility option while migrating. Do not make that flag an undocumented deployment assumption. [Language incompatibilities](https://www.lua.org/manual/5.5/manual.html#8.1), [parser declarations](https://www.lua.org/source/5.5/lparser.c.html).

## Named vararg tables

A vararg parameter can have a name after `...`. The name is a read-only binding to a table whose numeric fields contain the arguments and whose `n` field preserves their count. The table's contents can be changed; doing so can affect a later `...` expansion. [Function parameters](https://www.lua.org/manual/5.5/manual.html#3.4.11).

```lua
-- PUC Lua 5.5 only.
local function inspect(... args)
    return args.n, args[1], args[3]
end
local n, first, third = inspect(nil, 'middle', 'last')
assert(n == 3 and first == nil and third == 'last')
```

Use `.n` for arity. This feature does not make holes safe for `#` or `ipairs`. When supporting older runtimes, retain an explicit `table.pack`/`select` adapter in separately compatible source.

The implementation can avoid constructing a table for constrained access patterns; do not promise zero allocation after capturing or passing the vararg table elsewhere. Benchmark the actual use case. [Optimization conditions](https://www.lua.org/manual/5.5/manual.html#3.4.11).

A wrapper with named varargs should document whether it may modify them. Avoid surprising callers with transformations that alter subsequent forwarding. For logging adapters, bound values and cardinality before stringification.

## Loop variables and library changes

Loop control variables are read-only in 5.5. If application logic needs a mutable working value, create a new local in the body. [Language incompatibilities](https://www.lua.org/manual/5.5/manual.html#8.1).

```lua
-- Parses across PUC Lua 5.1–5.5.
local total = 0
for i = 1, 3 do
    local adjusted = i * 2
    total = total + adjusted
end
assert(total == 12)
```

Review code generators and old generic-loop bodies that assign to loop variables. A runtime branch around incompatible source cannot repair a parser rejection.

| Change | Operational implication |
|---|---|
| `table.create(nseq, nrec)` | Capacity hints for a new empty table; no fill value or logical length is established |
| `utf8.offset` returns start and end positions | Check forwarded multi-results and assignment cardinality |
| Float printing uses round-trip-capable decimal output | Golden text output can change; define serialization format intentionally |
| A nil error object becomes a string message | Preserve version-aware error assertions |
| `__call` chains have a documented object limit | Do not generate unbounded callable-wrapper chains |

Sources: [new library behavior](https://www.lua.org/manual/5.5/readme.html#changes), [table.create](https://www.lua.org/manual/5.5/manual.html#pdf-table.create), [utf8.offset](https://www.lua.org/manual/5.5/manual.html#pdf-utf8.offset), [incompatibilities](https://www.lua.org/manual/5.5/manual.html#8).

```lua
-- PUC Lua 5.5 only.
local reserve = table.create(100, 8)
assert(next(reserve) == nil and #reserve == 0)
local start_byte, end_byte = utf8.offset('\195\164x', 1)
assert(start_byte == 1 and end_byte == 2)
```

Do not transfer Luau's similarly named `table.create` contract to PUC Lua. Similar names across runtimes need separate documentation and tests.

## Embedding and GC changes

The 5.5 migration includes native API changes that require review even when Lua application source parses unchanged:

| Area | Check |
|---|---|
| State creation | `lua_newstate` has an explicit seed argument; inspect `luaL_makeseed` and host entropy policy |
| Library opening | `luaL_openselectedlibs` is available; choose exposed libraries intentionally |
| External strings | Lifetime and deallocation ownership are part of the embedding contract |
| GC tuning | Parameters use the new `param` / `LUA_GCPARAM` mechanism; old parameter triples cannot be carried over blindly |
| Call results | Explicit requested-result count has a documented maximum; use the supported multiple-result path when appropriate |
| Dumping | Writer callback/stack behavior changed; test custom bytecode-cache writers |
| Legacy APIs | `lua_resetthread` is a compatibility macro; `lua_setcstacklimit` is no longer declared in the public header |
| Varargs formatting | `lua_pushvfstring` reports failure by returning NULL and leaving an error message; `lua_pushfstring` still raises errors |
| Explicit GC steps | `LUA_GCSTEP` changes from an int argument measured in Kbytes to a size_t argument measured in bytes; port the variadic call type and units |
| Coroutine self-close | `coroutine.close()` defaults to the running coroutine; `lua_closethread(L, L)` does not return and requires a resume context |

Sources: [API incompatibilities](https://www.lua.org/manual/5.5/manual.html#8.3), [new APIs](https://www.lua.org/manual/5.5/readme.html#changes), [lua_newstate](https://www.lua.org/manual/5.5/manual.html#lua_newstate).

Review these differences even if old C code compiles: variadic calls cannot type-check a stale GC argument, and a formatting wrapper expecting a long jump can accidentally continue after the new NULL result. Do not use the non-returning self-close path across native frames whose cleanup requires ordinary return. Sources: [lua_pushvfstring](https://www.lua.org/manual/5.5/manual.html#lua_pushvfstring), [5.4 lua_gc](https://www.lua.org/manual/5.4/manual.html#lua_gc), [5.5 lua_gc](https://www.lua.org/manual/5.5/manual.html#lua_gc), [lua_closethread](https://www.lua.org/manual/5.5/manual.html#lua_closethread).

5.5 changes GC scheduling and array storage. These are reasons to measure the real workload, not a universal throughput or latency guarantee. Capture allocation rate, live heap, pause distribution, and host-boundary costs before tuning. Retain the ability to return to the baseline settings. [GC parameters](https://www.lua.org/manual/5.5/manual.html#2.5), [collector source](https://www.lua.org/source/5.5/lgc.c.html).

## Patch-specific defects

Check the official [known-bug list](https://www.lua.org/bugs.html#5.5.1) before freezing a runtime. At this review date, 5.5.1 has reported defects involving GC parameter arithmetic, numeric-loop/negative-zero edge cases, self-closing coroutines, and emergency collection while resizing weak tables. Some have linked upstream fixes; a fix on the upstream branch is not proof that an installed release or vendor build contains it.

In particular, do not adopt self-close inside finalizers or error cleanup solely because 5.5 documents the feature. Verify the precise affected path and patched source. Record a patch commit/checksum in addition to the release number when carrying a fix. Check older releases too: several reports list an earlier introduction version.

## Migration acceptance

1. Parse supported modules with the new runtime, including generated source.
2. Rebuild and run all native extensions against the same headers/configuration.
3. Check global-declaration scopes, loop assignments, and error assumptions.
4. Check wrappers around all functions whose return cardinality matters.
5. Validate file and wire formats independently of incidental print formatting.
6. Exercise coroutine failures, close paths, and host callback lifetimes.
7. Compare bounded workload measurements with the previous runtime.
8. Verify packaged/deployed behavior and cached-bytecode invalidation.

Report source compatibility, native rebuild success, and host deployment success separately. A failed host integration is not evidence that the language feature itself is unavailable; a successful CLI probe is not evidence that an engine plugin supports 5.5.
