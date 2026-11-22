---
name: lua-engineering
description: Design, implement, embed, debug, test, profile and deploy Lua applications and scripting APIs. Use for PUC Lua 5.1 through 5.5, LuaJIT and Luau distinctions; language semantics, tables and metatables, modules and hot reload, coroutines and errors, C/C++ embedding and native modules, garbage collection and performance, LuaRocks and tooling, sandboxing, persistence, networking, portable libraries, and simulation or event-driven game rules. Keep Unreal-specific integration in unreal-lua-engineering.
---

# Lua Engineering

Build against the actual runtime and host contract. Use this skill as a routed engineering knowledge base; load only the references required by the task. Keep a small script small. Do not impose an application framework, sandbox, coroutine scheduler or native extension when the task does not need one.

## Establish the runtime contract

1. Inspect the repository, host, build configuration and existing conventions.
2. Identify implementation (PUC Lua, LuaJIT, Luau or host fork), exact version/build, platform, numeric configuration, enabled libraries and native dependencies.
3. Distinguish CLI, embedded trusted rules, untrusted plugins, event-loop application and engine-hosted scripts. A host may remove standard functions or replace their behavior.
4. Record ownership of mutable state, scheduling/thread access, error propagation, persistent data, resource lifetime and deployment format where relevant.
5. Prefer the project's runtime. For a new unconstrained application, evaluate the current PUC release and required library/tool support. Do not silently migrate an embedded runtime.
6. Inspect or run a bounded probe for missing decisive details. State assumptions and continue with useful work before asking for information.

Evidence snapshot: 2026-11-22. Lua 5.5 is current in this snapshot; Lua 5.4 remains an important deployed embedding target. Refresh patch levels, bug reports and tool syntax support before dependency selection. Read [versions](references/versions-and-portability.md) and [source policy](references/sources-and-evidence.md).

## Route to the relevant material

| Task or failure | Reference |
|---|---|
| Choose a runtime, support several versions or migrate | [Versions and portability](references/versions-and-portability.md) |
| Check truthiness, scope, multiple returns or iteration | [Language semantics](references/language-semantics.md) |
| Represent arrays, maps, sparse values, IDs or graphs | [Tables and data models](references/tables-and-data-models.md) |
| Implement methods, inheritance, proxies or weak tables | [Metatables and object models](references/metatables-and-object-models.md) |
| Load modules, control environments or replace code | [Modules, environments and reload](references/modules-environments-and-reload.md) |
| Handle errors, cleanup, cancellation and coroutines | [Errors, resources and coroutines](references/errors-resources-and-coroutines.md) |
| Parse text, UTF-8, patterns or binary protocols | [Strings, patterns and binary data](references/strings-patterns-and-binary-data.md) |
| Adopt global declarations, named varargs or 5.5 APIs | [Lua 5.5 changes](references/lua55-changes.md) |
| Organize modules, interfaces, configuration and lifecycle | [Application architecture](references/application-architecture.md) |
| Save/load state, exchange JSON or migrate schemas | [Persistence and data exchange](references/persistence-and-data-exchange.md) |
| Handle time, randomness and numerical accuracy | [Numbers, time and randomness](references/numbers-time-and-randomness.md) |
| Use files, sockets, HTTP or host-specific APIs | [I/O, networking and hosts](references/io-networking-and-hosts.md) |
| Embed Lua and maintain stack/registry contracts | [Embedding and the C API](references/embedding-c-api.md) |
| Manage native handles, callbacks, threads and teardown | [Native lifetime and async](references/native-lifetime-and-async.md) |
| Expose capabilities to untrusted code | [Sandboxing and capabilities](references/sandboxing-and-capabilities.md) |
| Measure allocations, GC, boundary cost and throughput | [Performance and GC](references/performance-and-gc.md) |
| Use LuaJIT, FFI, Luau typing or codegen | [LuaJIT and Luau](references/luajit-and-luau.md) |
| Configure LuaLS, linting, formatting, packages and types | [Tooling and dependencies](references/tooling-and-dependencies.md) |
| Debug a failure or build a meaningful test matrix | [Testing and debugging](references/testing-and-debugging.md) |
| Build native modules or deploy across platforms | [Deployment and native modules](references/deployment-and-native-modules.md) |
| Implement simulation, rules, commands or replay | [Simulation and event systems](references/simulation-and-event-systems.md) |
| Find manuals, source, errata and validation provenance | [Sources and evidence](references/sources-and-evidence.md) |

## Preserve correctness conditions

- Keep syntax, library behavior and C ABI specific to the runtime. LuaJIT is not PUC Lua 5.4; Luau is a distinct dialect/runtime.
- Treat only nil and false as false. Preserve legitimate false or zero when applying defaults.
- Define dense sequence, sparse map or record semantics. Do not use table length as arbitrary key count or assign semantic order to unspecified traversal.
- Preserve argument/result counts when nil matters. Check expansion in tail positions.
- Separate module state from session/world/request state. Require caching, callbacks and captured closures affect reload.
- Make mutation ownership explicit. Coroutines do not provide parallel VM access, an OS scheduler or nonblocking I/O.
- Protect native boundaries, maintain stack balance, retain registry references deliberately and release them before VM destruction. Avoid unsafe longjmp across C++ object lifetimes.
- Serialize data through a defined schema. Source code, bytecode, closures and native addresses are not a portable persistence model.
- For hostile scripts, audit reachable capabilities, loaders, native libraries, budgets and isolation. An environment table alone is not a complete security boundary.
- Profile the real workload. Do not infer latency, memory or entity capacity from a language name or unrelated microbenchmark.

Read the matching references for version-specific evidence and exceptions. Apply only mechanisms relevant to the task.

## Implement and verify

1. Define or reproduce the observable requirement with explicit host assumptions.
2. Choose the smallest data model and lifecycle that satisfies it.
3. Implement a pure core or small module boundary where useful; inject the capabilities actually required.
4. Define error, empty/nil, invalid-input and resource-release behavior.
5. Check with the target parser/runtime. Tooling that rejects new syntax is not proof of a language error.
6. Verify success and meaningful failure/boundary cases. Test multiple runtimes only when portability is a requirement.
7. Profile relevant costs and optimize measured limiting work.
8. Report changes, actual runtime/toolchain, results and unresolved limits.

For conceptual requests, give the design and examples. For implementation requests, continue through working code and verification. A standalone Lua test does not certify an engine or native integration.

## Use the bundled diagnostics

Run from this skill directory with an explicit interpreter:

~~~sh
/path/to/lua scripts/runtime_probe.lua
/path/to/lua scripts/semantic_checks.lua
python3 scripts/run_lua_checks.py --lua /path/to/lua
~~~

Repeat --lua to compare supported PUC/LuaJIT executables. The Python runner uses argument arrays and a bounded timeout; it installs nothing, downloads nothing and executes no project files. Probes execute bundled trusted diagnostic chunks. Results are observations, not a complete conformance or sandbox certificate. Luau/restricted hosts need their own launch adapters.

- [Runtime contract](assets/runtime-contract.json): optional decision record.
- [Rules example](assets/rules.lua): explicit state and no mutation on rejected input; tested by semantic_checks.lua.
- [Minimal C host](assets/minimal_host.c): PUC 5.4/5.5 embedding example for trusted scripts, deliberately exposing standard libraries. Read the embedding reference for build and limits.

## Keep host boundaries clear

Lua can implement substantial domain logic. Place bulk operations, engine lifecycle, OS services and authority checks at an appropriate host boundary. Preserve the option to optimize selected systems without scattering host details through every rule.

For Unreal, use unreal-lua-engineering for engine versions, UObjects, worlds, replication, packaging and build evidence. Do not make this general Lua skill depend on a game engine, package manager or editor.
