---
name: unreal-lua-engineering
description: Select, implement, port, verify and debug Lua gameplay integration in Unreal Engine, especially UE 5.8. Use for UnLua, sluaunreal, LuaMachine, explicit Lua C-API plugins, exact engine/plugin compatibility, UObjects and reflection, world-scoped Lua states, client/server/shared scripts, authority and RPCs, animation/simulation boundaries, hot reload, packaging, dedicated servers, native lifetime and reproducible build evidence. Do not claim a generic UE5 compatibility label proves UE5.8 support.
---

# Unreal Lua Engineering

Choose a concrete integration route, record exact versions, and build the smallest meaningful proof before expanding gameplay. Keep general Lua semantics in lua-engineering; this skill covers the Unreal host and its deployment/lifecycle contracts.

**Evidence snapshot: 2026-11-22. No UE 5.8 binary was built or run while creating this skill.** The included source scaffold and porting procedures are actionable, source-grounded starting points. They require the selected Unreal toolchain and the acceptance checks below. A standalone Lua/C test is not an Unreal compatibility certificate.

## Start with the project contract

1. Inspect the actual project, engine Build.version, target files, plugins, script roots, build logs and team instructions.
2. Record exact UE version/changelist/source revision, binary versus source engine, platform/architecture, compiler/CRT, target/configuration, plugin commit and bundled Lua build.
3. Establish whether scripts need broad reflected UE access, a small explicit domain API, designer/mod APIs, server-only rules, local presentation or all of these.
4. Preserve an existing functioning integration unless changing it solves the task. Avoid replacing a plugin based only on release labels or popularity.
5. Select a route below. Mark unknown facts and continue with inspectable source/configuration work; ask for an engine checkout or build output only when it blocks the next proof.

Read [route selection](references/compatibility-route-selection.md) and [evidence policy](references/sources-and-evidence.md). Use [the acceptance contract](references/acceptance-contract.md) to define the minimum relevant proof, not an unnecessary platform matrix.

## Select a route deliberately

| Need | Candidate route | Acceptance condition |
|---|---|---|
| Broad access to reflected classes, properties, functions and events | Pinned UnLua source plus necessary UE-version adaptation | Exact build, representative bindings, lifecycle, packaged scripts and required network modes pass |
| Existing slua/LuaMachine project or their specific API model | Retain and inspect that plugin's exact source/build | Verify its own bindings, runtime, packaging and target matrix; do not transfer UnLua assumptions |
| Narrow rules API, limited dependence on UE reflection internals | Private Lua static library with a runtime module and world subsystem | C ABI/toolchain match, per-world ownership, protected calls, staged files and target build pass |
| Entire gameplay layer in a typed UE-oriented language | Consider AngelScript only if its engine-source/build requirements are acceptable | Treat as a separate engine integration decision, not a Lua drop-in |

For UnLua, distinguish documented capability from verified version support. The researched develop revision is a source baseline, not an endorsed UE 5.8 release. Do not patch reflection internals by suppressing warnings or reinterpreting smart-pointer storage as raw pointer links.

For the explicit embedding route, begin with the bundled finite-number evaluator. Grow the API only after its build and lifecycle work. It does not expose UObjects, automatically replicate state or implement a scheduler.

## Route to implementation details

| Work | Reference |
|---|---|
| Compare integration models and actual compatibility evidence | [Compatibility and route selection](references/compatibility-route-selection.md) |
| Pin/build UnLua, triage UE 5.8 changes and port reflection safely | [UnLua build and porting](references/unlua-build-porting.md) |
| Manage UObjects, delegates, GC and stale native references | [Binding and lifetime](references/binding-lifetime.md) |
| Scope state to worlds and implement client/server/shared roles | [Worlds and networking](references/worlds-networking.md) |
| Stage scripts, use Unreal filesystem access and design reload | [Packaging and reload](references/packaging-reload.md) |
| Combine rules, many entities, navigation and skeleton animation | [Simulation and animation](references/simulation-animation.md) |
| Build the explicit C-API subsystem route | [Custom embedding](references/custom-embedding.md) |
| Reproduce failures and verify native/runtime/packaged behavior | [Verification and troubleshooting](references/verification-troubleshooting.md) |
| Record pass/fail/not-run evidence without overclaiming | [Acceptance contract](references/acceptance-contract.md) |
| Consult exact sources and refresh the snapshot | [Sources and evidence](references/sources-and-evidence.md) |

## Preserve engine and network invariants

- Scope mutable Lua state to a world/session contract. Multiple PIE worlds may exist in one process; a process-global simulation table is not a per-world design.
- Distinguish actor authority, network mode, ownership and local-player presentation. Standalone and listen-server worlds can require both simulation and local presentation.
- Treat server/client/shared folders as loader organization. Shared source does not synchronize variables or remove server-only scripts from a client package.
- Keep authoritative mutation behind validated commands. Configure RPC ownership and explicit replication/serialization; arbitrary Lua tables are not automatically replicated.
- Respect the selected binding's UObject/GC ownership rules. Use stable domain IDs for saved relationships; validate transient handles at use and after async completion.
- Access UE objects and one Lua state on the supported owning thread. Coroutines are not permission to call UObject APIs from workers.
- Unregister delegates/timers, invalidate generations and stop admissions before destroying world state or unloading a module.
- Protect Lua execution/error boundaries. Do not allow Lua longjmp or C++ exceptions to cross unprepared frames; maintain stack and reference ownership contracts.
- Keep animations and movement in their appropriate UE systems. Lua may choose actions and parameters; per-frame native-to-script traffic must be measured.
- Distinguish successful Editor loading, packaged runtime operation and dedicated-server operation. Each observes a different contract.

## Implement incrementally

1. Build the native/plugin dependency for the exact engine toolchain.
2. Load one trusted Lua file through the intended packaged path.
3. Invoke one function and verify return, error and repeated-call behavior.
4. Prove state separation across the required worlds and teardown/restart cycles.
5. Expose one representative game command/read model; define ownership and validation.
6. Add actual RPC/replication only when multiplayer is required, and test the remote-client path.
7. Package and run without development source-directory fallbacks.
8. Measure a representative workload before adding per-entity scripting, caches or native batch APIs.

Preserve the user's existing implementation milestones. For a new terrain prototype, prove terrain first, then movement/animation, then one Lua-controlled rule. Do not introduce a large framework to demonstrate one production building.

## Use the included artifacts

- [Minimal LuaRules plugin](assets/minimal-plugin/LuaRules/LuaRules.uplugin): complete source scaffold for a Win64 x64 runtime module, private pinned PUC Lua 5.4.9 static library, UWorldSubsystem and one pure numeric rule. Read custom-embedding.md before copying. The third-party source archive and compiled library are intentionally not vendored.
- [Role selection example](assets/role_bootstrap.lua): pure Lua decisions for server authority and local presentation; no networking transport or loader is hidden in it.
- [Build evidence template](assets/build-evidence-template.json): optional exact-target record with honest not-run defaults.
- [Project inspector](scripts/inspect_unreal_lua.py): Python 3.9+ read-only metadata/source observations from paths explicitly provided by the caller. It never runs UBT, patches a plugin or establishes compatibility.
- [Role checks](scripts/check_roles.lua): exercise the role-selection example using a standalone Lua interpreter; these are not network integration tests.

~~~sh
python3 scripts/inspect_unreal_lua.py --plugin /path/to/Plugins/LuaRules --engine /path/to/UE_5.8 --project /path/to/Game.uproject
python3 scripts/inspect_unreal_lua.py --evidence /path/to/build-evidence.json
lua scripts/check_roles.lua
~~~

Use argument arrays or correctly quoted shell arguments for build paths. Preserve actual build logs and return codes. Never claim the plugin is working because metadata matches, an inspection script returns success, or a README names UE 5.8.
