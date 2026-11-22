# Sandboxing and capability design

Use when executing downloaded rules, user scripts, game mods, tenant code, or other code that should have less authority than the host. Apply the controls appropriate to the actual trust model; ordinary trusted application code does not need a custom sandbox by default.

## Contents

- [State the trust boundary](#state-the-trust-boundary)
- [Expose capabilities deliberately](#expose-capabilities-deliberately)
- [Load source and build environments](#load-source-and-build-environments)
- [Contain CPU and memory](#contain-cpu-and-memory)
- [Keep hosts from becoming escape routes](#keep-hosts-from-becoming-escape-routes)
- [Luau and LuaJIT differences](#luau-and-luajit-differences)
- [Validation and sources](#validation-and-sources)

## State the trust boundary

Separate these requirements before implementing anything:

| Requirement | Typical mechanism to evaluate |
|---|---|
| Prevent accidental globals between trusted scripts | Explicit modules and environments |
| Give scripts only selected application operations | Capability-based host API |
| Isolate unrelated script state | Separate environments or independent VMs, according to threat model |
| Bound work and memory consumption | Runtime accounting plus host deadlines, native-call budgets, and appropriate process limits |
| Contain a compromised native extension or VM | Separate process/OS boundary with restricted privileges |

An environment table controls name resolution. It is not by itself a CPU limit, native-memory limit, filesystem jail, or proof of isolation. “No `os` global” is a narrow observation; it does not describe every route reachable from exposed objects.

Write down who supplies code, which native functions it may reach, what data it may observe, and what damage a failed containment boundary could cause. Use that threat model to decide whether a VM-level boundary is sufficient or an external worker is needed.

When the requirement includes containment of a VM/native compromise, use a restricted worker process and a narrow capability broker in the trusted host. This is an architecture recommendation: the broker must validate operation schemas, tenant ownership, handle generations, payload sizes, and quotas for every request. Run parsing and compilation inside the restricted worker too; enforce deadlines and resource limits outside it. Restrict inherited credentials, file descriptors, filesystem access, and network authority. Merely launching a child process with the parent's privileges and secrets does not supply this boundary. LuaJIT explicitly recommends process-level containment for hostile code. [Upstream security position](https://luajit.org/faq.html).

## Expose capabilities deliberately

Prefer a small set of domain operations over arbitrary reflection or host objects. A capability should identify its authority, validate its input, bound its work, and define revocation.

| Prefer | Review before exposing |
|---|---|
| `read_config("approved_name")` | Generic filesystem objects and unrestricted paths |
| `emit_command(validated_command)` | Arbitrary shell execution |
| `lookup_entity(id)` with validity checks | Native pointers or unrestricted object traversal |
| Read-only snapshots or copied records | Mutable shared singleton tables |
| A fixed approved module map | Host filesystem/native-library searchers |
| Limited logging API | Unlimited output or sensitive process diagnostics |

Validate inputs at the capability boundary even when LuaLS reports correct types. Validate outputs before a privileged subsystem acts on them. Avoid returning a powerful parent object as an incidental field of a narrow result.

The full standard libraries contain facilities such as file access, processes, native library loading, and debugging. Open only the libraries the host contract needs; PUC 5.5 adds `luaL_openselectedlibs`, while earlier versions can open selected libraries explicitly. An opened library's indirect behavior still requires review. [Library loading](https://www.lua.org/manual/5.5/manual.html#6.1); [loader implementation](https://www.lua.org/source/5.5/loadlib.c.html).

## Load source and build environments

PUC Lua can reject binary input using text mode. Its manual explicitly warns that malicious binary chunks can crash the interpreter; bytecode is not a safe interchange format for hostile producers. [Loading chunks](https://www.lua.org/manual/5.5/manual.html#pdf-load); [binary loader, `luai_verifycode`](https://www.lua.org/source/5.5/lundump.c.html).

The following **PUC 5.2+ demonstration only separates globals**. It does not bound execution or implement a complete hostile-code sandbox:

```lua
local function run_formula(source, input)
    local env = {
        input = input,
        math = { min = math.min, max = math.max, floor = math.floor },
    }
    local chunk, err = load(source, "=formula", "t", env)
    if not chunk then
        return false, err
    end
    return pcall(chunk)
end
```

For a real boundary, inspect every referenced value, including `input`: a table with host userdata, callable metatables, closures capturing privileged data, or shared mutable descendants can carry authority. Copy and validate the allowed data graph instead of assuming the top-level table is harmless.

Do not fall back to `_G` through an environment metatable. Do not hand out `debug`, generic `load`, unrestricted `require`, native-module loading, or the host's package tables without a justified contract. Protect built-in and custom shared tables from mutation; a proxy with `__newindex` alone does not make an existing table deeply immutable.

Module loading needs its own policy: canonical module IDs, allowlisted dependency graph, size limits, fixed search roots, caching scoped to the relevant tenant/session, and a defined update process. Trusted and untrusted modules should not share mutable caches accidentally.

## Contain CPU and memory

PUC instruction hooks can observe execution at selected events/counts. They are a scheduling/accounting tool, not a hard limit on time spent inside every native call. A script can also catch ordinary errors; an error raised by a hook must not be treated as a universally uncatchable kill operation. Review the host's actual termination path. [`lua_sethook`, `luaG_traceexec`](https://www.lua.org/source/5.5/ldebug.c.html); [protected errors](https://www.lua.org/manual/5.4/manual.html#2.3).

Recommended resource design:

1. Limit source size and parse/compile work as well as execution.
2. Budget a job or session, not only one callback; repeated small calls also consume resources.
3. Use monotonic host deadlines and cancellation checked at runtime safepoints.
4. Give expensive host functions their own input limits, timeouts, and cancellation.
5. Account for Lua heap and native resources separately.
6. Choose an external worker/process limit when reliable interruption cannot be guaranteed in process.

A custom Lua allocator can account for allocations passing through it, provided it correctly handles growth, shrinkage, failure, and frees. Allocations in foreign libraries or host objects may bypass that allocator. A useful quota model includes outstanding requests, log bytes, object counts, and returned data size, not only VM bytes. [`lua_newstate` and allocator use](https://www.lua.org/source/5.5/lstate.c.html#lua_newstate).

## Keep hosts from becoming escape routes

For each exposed function, examine:

- Can it read or mutate another session's data?
- Can it call an arbitrary method, evaluate source, load a module, or manufacture a capability?
- Can a crafted table trigger unanticipated metamethod calls?
- Can a native callback reenter script while a privileged invariant is temporarily broken?
- Can stale handles access recycled resources?
- Can an error message reveal secrets or invoke another script function?

Use schemas and opaque handles where appropriate. Revoke capabilities when a session ends, and reject queued work carrying an old session generation. Keep host validation independent of client-side or script-side validation.

## Luau and LuaJIT differences

**Luau** removes or restricts several standard Lua facilities and provides host APIs to freeze shared tables and isolate thread globals. Its embedding setup requires cooperation: use the documented `luaL_sandbox`, `luaL_sandboxthread`, readonly table support, allocator accounting, and interrupt callback as appropriate. It imposes no default memory quota. Its VM expects compiler-produced bytecode; validate provenance before loading bytecode. [Luau sandbox design](https://luau.org/sandbox/); [Luau C API sandbox/callback sections](https://luau.org/api/).

**LuaJIT** provides an FFI that calls native functions and accesses C data. Treat FFI availability as native-code authority, not as an innocuous convenience library. Removing its global name is insufficient if a script can recover it through a module loader or an exposed closure. Disabling JIT compilation does not turn FFI calls into a safe sandbox. [FFI capabilities](https://luajit.org/ext_ffi.html); [LuaJIT VM controls](https://luajit.org/ext_c_api.html).

LuaJIT's FAQ states that parsing, loading, or running untrusted source or bytecode is not considered safe and that bugs involving it are not considered security-relevant for LuaJIT itself. It also warns that compiled code ignores debug hooks: a tight compiled loop may never return to the interpreter to run an interrupt hook. Do not use a PUC-style instruction-hook budget as the sole termination mechanism for JIT-enabled hostile code. Evaluate a restricted worker with externally enforced limits, including limits on expensive native calls. [Official FAQ: interruption and sandboxing](https://luajit.org/faq.html).

For every runtime, keep the exact patched build and capabilities in the security argument. Do not translate a project's general “sandboxed” description into a guarantee about your host API.

## Validation and sources

Run adversarial cases only in an appropriately contained test environment: infinite Lua loop, enormous allocation, deeply nested input, output flooding, repeated failed calls, mutated shared library table, crafted metatable, unauthorized module path, stale handle, callback after cancellation, and expensive native operation. Verify both resource limits and absence of unauthorized side effects.

Primary sources checked 2026-11-22:

- [PUC load/environment API](https://www.lua.org/manual/5.5/manual.html#pdf-load), [5.4 errors](https://www.lua.org/manual/5.4/manual.html#2.3).
- [5.5.1 binary loader](https://www.lua.org/source/5.5/lundump.c.html), [debug hooks](https://www.lua.org/source/5.5/ldebug.c.html), [state allocator](https://www.lua.org/source/5.5/lstate.c.html), [module loader](https://www.lua.org/source/5.5/loadlib.c.html).
- [Luau sandboxing](https://luau.org/sandbox/), [Luau C API](https://luau.org/api/).
- [LuaJIT FFI](https://luajit.org/ext_ffi.html), [LuaJIT C API controls](https://luajit.org/ext_c_api.html), [LuaJIT FAQ: hooks and untrusted code](https://luajit.org/faq.html).
