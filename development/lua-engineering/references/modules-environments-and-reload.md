# Modules, environments, dependency boundaries, and reload

Scope: PUC Lua with version gates. Reviewed 2026-11-22. Reload procedures here are application design recommendations; Lua does not supply a universal live-update protocol.

## Contents

- [A module contract](#a-module-contract)
- [Loader and cache behavior](#loader-and-cache-behavior)
- [Environments](#environments)
- [Separate definitions from instances](#separate-definitions-from-instances)
- [Designing reload](#designing-reload)
- [Diagnosing loading failures](#diagnosing-loading-failures)

## A module contract

Prefer modules that return one explicit value, usually a table of functions, constructors, or definitions. Keep loading side effects small and declared. Legacy `module(...)` changes environment behavior and is not a portable modern module pattern. [5.1 module library](https://www.lua.org/manual/5.1/manual.html#5.3), [5.2 library changes](https://www.lua.org/manual/5.2/manual.html#8.2).

```lua
-- A complete module; PUC Lua 5.1–5.5.
local M = {}
function M.cost(unit_price, count)
    assert(type(count) == 'number' and count >= 0 and count % 1 == 0)
    return unit_price * count
end
return M
```

Treat imports as dependencies. A domain module can accept storage, clock, random generator, and logger through a constructor or argument. That makes host behavior explicit and permits small tests without a game engine, service, or filesystem.

## Loader and cache behavior

`require` consults the loaded-module table and configured searchers/loaders. `package.path` concerns Lua files; `package.cpath` concerns native libraries. Dots in module names are interpreted by the standard search paths; a project may replace these mechanisms. [5.4 package library](https://www.lua.org/manual/5.4/manual.html#6.3), [loader implementation `ll_require`, `findloader`, `searchpath`](https://www.lua.org/source/5.5/loadlib.c.html#ll_require).

| Situation | Consequence | Application rule |
|---|---|---|
| Loaded value is truthy | Cached value is returned | Avoid re-running initialization unintentionally |
| Module returns false | It does not establish the usual truthy cache hit | Return a table/object for normal reusable modules |
| Loader returns nil and no loaded value is set | Standard require records true | An accidental missing return can produce a boolean API |
| Cache entry is cleared | Future require can reload | Existing references remain references to the old objects |
| Dependency cycle | Partly initialized dependencies or recursion can occur | Make initialization order explicit; do not assume a universal cycle resolver |

PUC 5.4+ `require` can also return loader data on an actual load; a cached result does not supply the same result list. Capture the module into one local before forwarding results to another API. [require contract](https://www.lua.org/manual/5.4/manual.html#pdf-require).

Namespace modules consistently: `project.storage` is more informative than a globally ambiguous `util`. Avoid modifying search paths from arbitrary feature modules. Configure allowed roots at the host/bootstrap boundary and record the resolved source in diagnostics.

## Environments

In PUC 5.2+, a free name resolves through lexical `_ENV`; `_G` is an ordinary binding referring to the conventional global table. Changing `_G` is not a substitute for changing a chunk's lexical environment. In 5.1, function environments and `setfenv` use a different mechanism. [5.2 environments](https://www.lua.org/manual/5.2/manual.html#2.2), [5.1 environments](https://www.lua.org/manual/5.1/manual.html#2.9).

For trusted expression evaluation under a deliberately small environment on PUC 5.2+:

```lua
local environment = { limit = 7 }
local chunk, message = load('return limit * 2', '@rule', 't', environment)
assert(chunk, message)
assert(chunk() == 14)
```

The `'t'` mode admits text, not arbitrary binary chunks. The environment controls the free names reachable directly from that chunk. It does not revoke capabilities captured inside supplied functions, restrict all resource consumption, or secure exposed native operations. A callable object or library can carry more authority than its name suggests. [load contract](https://www.lua.org/manual/5.4/manual.html#pdf-load), [loader implementation](https://www.lua.org/source/5.5/lbaselib.c.html#luaB_load).

Do not assume the first upvalue of an arbitrary dumped function represents `_ENV`; the special guarantee applies to loaded main chunks, while dumped functions may have other upvalue arrangements. Do not use bytecode as a general closure-state serializer. [load and upvalues](https://www.lua.org/manual/5.4/manual.html#pdf-load).

## Separate definitions from instances

Use three concepts when multiple sessions or worlds can coexist:

1. **Module code:** functions and constructors.
2. **Definitions:** recipes, schemas, configuration, immutable-by-contract metadata.
3. **Instance state:** queues, entities, timers, user state, resource handles.

Avoid storing session state in an implicitly shared module unless a process-wide singleton is intentional. The cache belongs to the interpreter state; coroutines within that state do not provide isolated module caches. [Threads and states](https://www.lua.org/manual/5.4/manual.html#2.6), [package.loaded](https://www.lua.org/manual/5.4/manual.html#pdf-package.loaded).

```lua
local M = {}
function M.new(clock)
    local instance = { ticks = 0 }
    function instance:step()
        self.ticks = self.ticks + 1
        return clock(), self.ticks
    end
    return instance
end
return M
```

Factories provide a clear reset boundary. Keep snapshots as explicit data when they must survive module replacement or application restarts.

## Designing reload

Clearing `package.loaded[name]` is only cache invalidation. It does not replace old callbacks, close old resources, migrate instance layouts, or update every previously captured function. Design reload as a controlled state transition:

1. **Stage:** Parse and load candidate code in an appropriate staging context. Require a versioned API description and declared dependencies.
2. **Validate:** Check mandatory exports and run bounded pure checks without modifying active state.
3. **Prepare:** Pause relevant dispatch, record affected registrations, and identify state migrations.
4. **Migrate:** Transform a copy or otherwise recoverable form of state. Validate the resulting invariants.
5. **Commit:** Switch the active module reference and update intended callbacks at a defined boundary.
6. **Retire:** Unsubscribe old events and cancel/close resources that belong to the retired implementation.
7. **Recover:** If preparation fails, retain the old implementation. Define recovery for failures after external side effects separately.

A stable dispatch object can look up the current implementation on each call, avoiding captured stale function references. This is a tradeoff: extra indirection buys replacement control. Updating methods in place is another option, but must handle removed exports and mixed generations of state.

Do not advertise arbitrary in-flight coroutine migration. A suspended coroutine retains its frames and local state; choose to drain, cancel, or version long-running tasks explicitly. [Coroutine execution model](https://www.lua.org/manual/5.4/manual.html#2.6).

## Diagnosing loading failures

Capture: exact runtime; requested module name; configured Lua/native paths; current working directory; resolved source; loader error chain; architecture and native dependency details. Check case-sensitive filenames on the deployed filesystem, packaged resource inclusion, and host-custom searchers. Separate “module not found,” parser error, runtime initialization error, and native loader/ABI failure before changing code.
