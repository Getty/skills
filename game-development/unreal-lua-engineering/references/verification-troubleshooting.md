# Verification gates and targeted troubleshooting

Use this to turn a source-grounded route into a precise compatibility statement. Record each result as passed, failed or not run, with engine/toolchain/plugin/runtime identity and raw evidence. The skill's UE build/runtime gates are initially **not run**.

## Minimal integration acceptance

| Gate | Exercise | Required evidence |
|---|---|---|
| Inputs | Inspect engine build, target, Lua source/header/library, plugin SHA/patches | Reproducible version tuple; no unidentified binary |
| Native build | Compile and link the actual Editor target | Build command, exit status and relevant logs |
| Normal execution | Initialize one game world and call one rule | Correct result and identifiable VM/world |
| Error containment | Syntax error, wrong module result, runtime error, wrong return type | Useful diagnostic; no UE crash; defined readiness/result |
| Stack discipline | Repeated successful and failing calls | Constant host stack shape and no accumulated roots |
| World lifetime | Repeated PIE start/stop and map changes | New state where required; no stale callbacks or cross-world values |
| Packaging | Cook/stage/run a Development game | Script found through the selected loader in the actual distribution |
| Final target | Required Shipping/Client/Server builds | Independent result for each target actually needed |

Use meaningful checks at the integration boundaries; do not multiply arithmetic tests after the remaining risk has moved to packaging or object lifetime.

## Supplied scaffold probes

Begin with `main.lua` unchanged: `Evaluate(3)` must return 6. Check a negative and fractional input. Reject NaN/infinity at the native entry. These are correctness probes, not benchmarks.

To test errors without adding standard libraries, replace the chunk for one test at a time and restart the world:

| Script variation | Expected outcome |
|---|---|
| Missing `end` | Initialization fails with compilation error |
| `return 42` | Initialization rejects the module contract |
| `return function(x) return '6' end` | Evaluation rejects string coercion |
| `return function(x) return x, x end` | Evaluation rejects extra results |
| `return function(x) return end` | Evaluation rejects missing result |
| `return function(x) return x + {} end` | Protected runtime error; host remains alive |
| `return function(x) return 1 / 0 end` | Non-finite result rejected |

For failure-then-success in the **same** VM, use:

```lua
return function(value)
    if value < 0 then
        return value + {}
    end
    return value * 2
end
```

Call negative then positive inputs repeatedly. The second call must still succeed; inspect stack invariants in a debug build. The example does not call `error`, `assert` or `print`, because the scaffold intentionally opens no standard libraries.

For world isolation, temporarily use a closure-local counter:

```lua
local count = 0
return function(_)
    count = count + 1
    return count
end
```

The first call in each new world must return 1. Exercise multiple PIE worlds in one process; sequential counts across worlds expose shared state. Stop and restart PIE and repeat. Restore the original script after probes.

## Broader plugin lifecycle tests

For UnLua or any UObject bridge, create/bind/destroy actors; end play with pending timers; remove delegate listeners; force collection; travel maps; and recompile a bound Blueprint in the editor. Verify that deleted objects are rejected, manual roots are released and callback dispatch does not enter an old VM.

When porting the reflection override list, add focused tests for empty/head/middle/tail insertion/removal, repeated enable/disable and other fields following the override node. Tie each test to the changed symbol. See [UnLua `LuaOverridesClass.cpp`](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/UnLua/Private/LuaOverridesClass.cpp) and [UE 5.8 UField declaration](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/CoreUObject/UField?application_version=5.8).

## Network tests when networking is in scope

Use standalone, listen server, dedicated server, single-process PIE and separate processes. Include a command that succeeds, one rejected for insufficient resources, late join, reconnect and disconnect during pending work. Assert a single authoritative mutation and adequate client reconstruction. A Client/Server file split without this exercise is organization evidence only.

Epic's [PIE options](https://dev.epicgames.com/documentation/en-us/unreal-engine/play-in-editor-multiplayer-options-in-unreal-engine) support multiple worlds and network emulation. Its [dedicated-server setup](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-dedicated-servers-in-unreal-engine) separates build, cook and run. Preserve those distinctions in test reports.

## Troubleshooting by symptom

| Symptom | First discriminating check | Likely boundary |
|---|---|---|
| Generic missing/incompatible module | Find the earliest UBT compile/link failure | Native build, not necessarily plugin startup |
| `Lua.dll` missing | Inspect selected integration's linkage and staged dependency | Dynamic-library deployment; the supplied scaffold uses static linkage |
| Works in editor, missing script in package | Compare staged manifest, loader and resolved path | UFS/NonUFS mismatch or missing staging |
| Old script keeps running | Log module source origin/hash and cache generation | Shadowing loader root, cached closure, or no reload feature |
| Server has UI errors | Log world net mode and local-player availability | Role bootstrap or server module dependency |
| PIE clients share inventory | Log VM identity, world and game-instance identity | Wrong environment locator/global mutable state |
| Crash after travel or actor destruction | Trace callback generation, owner world and wrapper validity | Cross-runtime lifetime |
| Crash after Blueprint recompilation | Inspect override restoration and reflection caches | Reinstancing/port regression |
| Frame spikes after many jobs finish | Separate dispatch, Lua, GC, batch native work and replication | Scheduling/allocation rather than an assumed language limit |

The inspected UnLua loader searches persistent-download paths before project paths; source provenance is therefore a concrete diagnostic, not an optional cosmetic log. Source: [`FLuaEnv::LoadFromFileSystem`](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/UnLua/Private/LuaEnv.cpp).

## Completion statement

Report what actually ran: "Development Editor compiled on [engine/toolchain] and the packaged scalar-rule scenario passed" is useful. "Works with UE5" hides the required evidence. Include unrun platform/Server/Shipping/lifecycle gates without implying they failed. If blocked, name the first unresolved symbol, missing dependency or unavailable engine target and the concrete next action that would settle it.
