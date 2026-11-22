# Compatibility evidence and route selection

Research snapshot: **2026-11-22**. Read this before selecting a plugin or claiming UE 5.8 support.

## Evidence levels

| Level | What it establishes | What it does not establish |
|---|---|---|
| Documented API | A named official API, lifecycle, or build mechanism exists in the cited documentation. | The proposed integration compiles in the user's installation. |
| Inspected source | A specific immutable revision contains the described implementation. | Correct behavior on every engine/toolchain/platform. |
| Reported behavior | An issue author or maintainer reports a failure or fix. | Independent reproduction, complete coverage, or support commitment. |
| Local build verified | A recorded exact target compiled and linked locally. | Cooked runtime, teardown, networking, or production fitness. |
| Runtime verified | A recorded scenario passed on the exact build. | Scenarios and targets not exercised. |

**This skill's UE 5.8 compilation, editor execution, packaging, and multiplayer tests were not run.** It supplies a source-grounded implementation route, inspected upstream risks, and acceptance procedures. The minimal plugin is a proof scaffold awaiting those engine tests.

Unversioned Epic URLs may resolve to a newer documentation version; during research several displayed 5.9. Prefer the 5.8 selector where available and inspect the installed engine headers for exact signatures. A search result with a 5.8 heading is documentation evidence, not a local build result.

## Available routes

| Route | Documented or inspected capability | Choose it when | Cost to establish UE 5.8 suitability |
|---|---|---|---|
| Narrow C API embedding | Epic supports external library modules; `UWorldSubsystem` supplies world lifetime hooks; Lua provides an embedding C API. | Rules consume explicit values/IDs and a small game-specific API is desirable. | Build the library for the exact ABI; compile the host; test UFS loading, lifecycle and intended targets. |
| Tencent UnLua | Reflection access and Blueprint-event integration; runtime/editor modules; source includes per-game-instance environment location. | Scripts need broad Actor, UObject, UI and event access. | Audit and potentially port reflection internals in addition to building/testing. |
| Tencent sluaunreal | Project README includes Lua-defined RPCs and typed replication declarations. | Those Lua-side facilities fit an existing project or team. | Inspect exact source and dependencies; do not transfer UnLua compatibility conclusions. |
| LuaMachine | Developer-defined API; filesystem scripts or packaged LuaCode assets. | A constrained application API is preferred and existing plugin facilities reduce work. | Resolve exact platform failures and run world/packaging tests; UE5 branding is insufficient. |

Sources: [Epic external libraries](https://dev.epicgames.com/documentation/en-us/unreal-engine/integrating-third-party-libraries-into-unreal-engine), [UWorldSubsystem 5.8](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UWorldSubsystem?application_version=5.8), [UnLua README](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/README_EN.md), [slua README](https://github.com/Tencent/sluaunreal), [LuaMachine README](https://github.com/rdeioris/LuaMachine).

For a new simulation centered on recipes, jobs, needs and production, start with the narrow route unless broad UObject scripting is an explicit requirement. This is an architecture recommendation: it limits the engine surface that must be maintained. For an established UnLua game, evaluate a targeted port before replacing its scripting architecture.

## Inspected UnLua baseline

The upstream `develop` head retrieved through GitHub's branch API was **`4a534502bbf2c5e51b456d9142acfa631e53350c`**, dated 2026-04-02. Use this as an audit baseline, not as an approved UE 5.8 release. Re-resolve upstream before implementation; record the selected full SHA and patch series.

| Observation | Evidence | Consequence |
|---|---|---|
| Plugin descriptor still says 2.3.6 at this SHA. | [UnLua.uplugin](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/UnLua.uplugin) | VersionName cannot identify the actual source. |
| UE 5.6 work was reported merged to `develop`. | [Issue 754, maintainer/contributor discussion](https://github.com/Tencent/UnLua/issues/754) | There is a newer path than blindly selecting the old release tag; this does not establish 5.8. |
| A UE 5.7 pointer-type failure was reported and remains open in the retrieved issue. | [Issue 763](https://github.com/Tencent/UnLua/issues/763) | Audit reflection list manipulation before claiming 5.8 support. |
| The default selected runtime is `lua-5.4.3`. | [`Lua.Build.cs::GetLuaVersion`](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/ThirdParty/Lua/Lua.Build.cs) | A newer system Lua installation does not upgrade the embedded runtime. |
| Binding code includes Lua implementation headers and version branches. | [`LuaCore.cpp`](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/UnLua/Private/LuaCore.cpp) | Replacing Lua with 5.5, LuaJIT, or Luau is an integration port, not a filename change. |

LuaMachine has a specific [UE 5.8 Linux/Clang report, issue 84](https://github.com/rdeioris/LuaMachine/issues/84): unreachable statements and an additional-path search loop that the reporter believes terminates prematurely. Treat it as a reported configuration-specific failure. Review the search behavior before removing warnings; do not label every platform broken or disable warnings globally.

## Decision procedure

1. Record engine full version/changelist, build source, OS, architecture, compiler/toolset, SDK, target configuration and required deployment platforms.
2. State the needed boundary: pure rule evaluation, domain commands, broad reflection, Blueprint override, UI, RPC declarations, modding, or native extensions.
3. Select one integration and one Lua implementation. Inventory any other Lua runtimes already loaded by plugins.
4. For UnLua, audit the pinned implementation and local engine declarations before modifying source. For narrow embedding, compile the supplied scaffold without adding unrelated facilities.
5. Run the smallest end-to-end slice: initialize per world, evaluate a rule, surface an error, tear down, and load the same rule in a packaged build.
6. Add dedicated-server verification when required; a successful editor or standalone Game target does not establish a Server target.

Do not call an integration "supported on UE 5.8" until the output names the evidence level, exact version tuple and exercised scenarios. When a blocker remains, state its source/symbol and the test or access needed to settle it.
