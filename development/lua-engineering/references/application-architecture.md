# Application architecture

## Contents

- Establish host and lifetime
- Organize modules and capabilities
- Specify data and errors
- Control configuration and lifecycle
- Observe and evolve interfaces

This reference gives design recommendations based on the selected runtime's semantics. Check the [5.4 manual](https://www.lua.org/manual/5.4/manual.html) or [5.5 manual](https://www.lua.org/manual/5.5/manual.html) for language guarantees.

## Establish host and lifetime

Identify who creates the VM, loads modules, invokes entry points and destroys state. A CLI, HTTP worker, game world, editor tool and device controller have different restart and cancellation requirements. The embedding program defines the available functions and entry points. [Source: Lua as a hosted library](https://www.lua.org/manual/5.5/manual.html#1).

| Concern | Decision |
|---|---|
| Runtime | Implementation, exact release/commit, numeric build, syntax |
| Isolation | Process, VM, world, request or module instance |
| State owner | Component allowed to mutate each collection |
| Scheduling | Callback, explicit update, event loop or CLI call |
| Host boundary | Files, network, clock, randomness, native handles |
| Failure | Status, raised error, retry, cancellation or shutdown |
| Persistence | Schema, migration and transaction boundary |
| Delivery | Source modules, archive or version-bound bytecode |

Do not turn every row into an abstraction. A small conversion tool may need only a module and explicit input/output paths.

## Organize modules and capabilities

Prefer modules returning an explicit public value. require caches modules in package.loaded; requiring a name again does not create a new application instance. A module can return a constructor for instance-local state. [Source: require](https://www.lua.org/manual/5.5/manual.html#pdf-require).

~~~lua
-- Original example, PUC 5.1+ common subset.
local M = {}
function M.new(deps)
    assert(type(deps) == "table")
    assert(type(deps.now) == "function")
    local count = 0
    local api = {}
    function api.record()
        count = count + 1
        return { count = count, observed_at = deps.now() }
    end
    function api.snapshot()
        return { count = count }
    end
    return api
end
return M
~~~

This example copies snapshot data and keeps count private. It does not supply persistence, synchronization or a sandbox. The constructor allows independent instances while module code remains cached.

Group by stable domain responsibilities: inventory, catalog, rules, adapters. Avoid a universal Utils table that hides the dependency graph. Use simple functions and records before deep inheritance. Introduce interfaces at boundaries that change, require restricted access or benefit from controlled tests.

Pass clock, random source, storage, logging and network adapters explicitly where needed. If access control matters, expose a narrow operation instead of an unrestricted host object. Reachability still determines capabilities; see sandboxing-and-capabilities.md.

## Specify data and errors

For public functions, document accepted values/units; borrowed, copied or mutated tables; missing versus false/zero/empty fields; result count; error representation; yield/callback behavior; and guarantees after failure.

Use a consistent error convention per layer. A parser may return value, error; an invariant may raise; a native boundary may translate a caught error into a structured status. Error values need not be strings. [Source: error handling](https://www.lua.org/manual/5.5/manual.html#2.3).

Recommended mutation rule: validate and compute before publishing changes. A pcall is an error boundary, not a transaction rollback. When an operation crosses external systems, use their real transaction or compensation mechanisms. The bundled assets/rules.lua demonstrates a small validate-before-write operation.

Use field names or schemas to record units: duration_seconds, tick_index, bytes, radians. Keep CPU time, wall time and simulation time distinct. See numbers-time-and-randomness.md.

## Control configuration and lifecycle

Lua configuration is executable code. For trusted configuration this is useful; use an inert data parser when execution is inappropriate. Validate required fields, enums, ranges and unsupported keys before side effects.

Preserve explicit false when filling defaults:

~~~lua
local enabled = config.enabled
if enabled == nil then enabled = true end
~~~

The expression config.enabled or true erases false because nil and false are Lua's false values. [Source: values/types](https://www.lua.org/manual/5.5/manual.html#2.1).

Normalize configuration once. Prefer distinct definitions and mutable instances: catalog data, live inventory and transient host handles have different ownership. Tables are reference values; assigning the same definition table to several instances shares it. [Source: values/types](https://www.lua.org/manual/5.5/manual.html#2.1).

Use lifecycle stages where needed: construct, initialize, start, stop admission, drain/cancel, release. Define cleanup after partial initialization and repeated stop calls. Unsubscribe callbacks and timers before destroying their target. Keep retries bounded and visible.

## Observe and evolve interfaces

Give logs stable fields: operation, subsystem, request/world/session ID, duration and error category. Avoid dumping arbitrary payloads or credentials. Keep logging injectable; rate-limit repetitive failures where they obscure the first cause.

Version public script APIs independently of save schemas. Preserve exported names that consumers rely on; document unsupported internals. Prefer additive evolution or migration adapters when scripts are already deployed.

Treat hot reload as a state transition: quiesce work, validate replacement code, migrate candidate state, replace dispatch targets, rebind callbacks and resume. Clearing package.loaded does not remove old closures held elsewhere. [Source: require caching](https://www.lua.org/manual/5.5/manual.html#pdf-require); the staged transition is design guidance.

Review whether a second instance leaks mutable state, failed commands partially mutate, callbacks outlive the host, tests can control time/randomness and the target parser accepts every file. Prioritize concrete risks; remove abstractions that hide straightforward state changes.
