# Sources and evidence

Evidence snapshot: **2026-11-22**. No Unreal installation was available for compiling or running the included scaffold. Keep exact source findings, reported failures, documented APIs and executed tests separate.

## Pinned integration evidence

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| [UnLua develop source at 4a534502bbf2c5e51b456d9142acfa631e53350c](https://github.com/Tencent/UnLua/tree/4a534502bbf2c5e51b456d9142acfa631e53350c) | An immutable inspected source baseline | UE 5.8 compilation or runtime success |
| [UnLua README](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/README_EN.md) | Reflected binding features and broad engine claim | Exact patch/toolchain support |
| [UnLua issue 754](https://github.com/Tencent/UnLua/issues/754) | Reported 5.6 build failure and contributor statement about develop merge | A 5.8 certification |
| [UnLua issue 763](https://github.com/Tencent/UnLua/issues/763) | Reported reflection compatibility problem and proposed changes | Safety of a raw pointer reinterpretation |
| [LuaMachine issue 84](https://github.com/rdeioris/LuaMachine/issues/84) | Reported 5.8 Linux/Clang errors and suspected loader logic issue | Failure of every platform or an approved fix |
| [sluaunreal](https://github.com/Tencent/sluaunreal) | Its own RPC/property declaration and binding approach | Interchangeability with UnLua |
| [LuaMachine](https://github.com/rdeioris/LuaMachine) | Controlled API and loading model | An unchanged 5.8 build |

Inspect current branches before project adoption, then pin the revision actually tested. Never identify a plugin solely by the VersionName in its descriptor: different source revisions can retain the same display version. See the build/porting reference for exact source files and symbols.

## Epic authorities

| Source | Scope |
|---|---|
| [UWorldSubsystem, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UWorldSubsystem?application_version=5.8) | World lifetime, creation and callbacks |
| [UField, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/CoreUObject/UField?application_version=5.8) | Field-link type/API review |
| [Third-party libraries](https://dev.epicgames.com/documentation/en-us/unreal-engine/integrating-third-party-libraries-into-unreal-engine) | External modules, libraries and runtime staging |
| [Plugin architecture](https://dev.epicgames.com/documentation/en-us/unreal-engine/plugins-in-unreal-engine) | Descriptors and module placement |
| [Build configuration](https://dev.epicgames.com/documentation/en-us/unreal-engine/build-configuration-for-unreal-engine) | Target/toolchain configuration |
| [Object pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine) | UObject pointer ownership and tracking |
| [Networking overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine) | Standalone/listen/dedicated/client roles |
| [RPCs](https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-procedure-calls-in-unreal-engine) | Owning-connection and execution rules |
| [Property replication](https://dev.epicgames.com/documentation/en-us/unreal-engine/replicate-actor-properties-in-unreal-engine) | Explicit synchronized state |
| [PIE multiplayer](https://dev.epicgames.com/documentation/en-us/unreal-engine/play-in-editor-multiplayer-options-in-unreal-engine) | Multiple worlds/process arrangements |
| [Animation Blueprints](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprints-in-unreal-engine) | Skeletal animation control |

Unversioned Epic pages may show a newer engine heading. For version-sensitive C++ changes, prefer the selected version's API and the installed header/source. A documentation signature is useful evidence, but UHT/UBT and the actual compiler remain necessary.

## Lua and native-build authorities

- [Lua release archives/checksums](https://www.lua.org/ftp/): obtain the exact pinned dependency.
- [Lua 5.4 manual](https://www.lua.org/manual/5.4/manual.html): scaffold C API, stack, loading and errors.
- [Lua 5.4 source](https://www.lua.org/source/5.4/): verify implementation behavior for the selected patch source.
- [Lua compatibility policy](https://www.lua.org/versions.html): do not swap Lua versions without ABI/API review.
- [CMake MSVC_RUNTIME_LIBRARY](https://cmake.org/cmake/help/latest/prop_tgt/MSVC_RUNTIME_LIBRARY.html): explicit CRT selection in the build recipe.
- [AngelScript installation](https://angelscript.hazelight.se/getting-started/installation/): separate engine-source/build requirement when comparing scripting alternatives.

The bundled scaffold pins PUC Lua 5.4.9 for its own narrow API. That is independent of the Lua revision bundled by a selected UnLua checkout. Do not share or replace one library merely because both expose lua_State.

## Verification scope

The descriptor/layout and inspector received structural and CLI checks, including invalid evidence records, missing paths and synthetic engine/project metadata. The pure role-selection fixture was executed against standalone PUC Lua 5.1.5, 5.4.9 and 5.5.1. The general lua-engineering skill contains separately verified language and C-host examples.

An independent host-boundary exercise compiled the unchanged `LuaRulesSubsystem.cpp` against deliberately fake UE API definitions and the real PUC Lua 5.4.9 static library, using GCC 14.2, C++20, strict warnings, AddressSanitizer and UndefinedBehaviorSanitizer. It checked finite input/results, strict result shape, repeated failure/success stack balance, independent simulated instances, manually invoked teardown and off-thread rejection. The run passed with leak detection disabled because LeakSanitizer could not run under the executor's tracing environment. The Lua library itself was not sanitizer-instrumented.

That exercise tests the Lua-facing C++ control flow under test doubles. It does **not** test UHT/UBT, actual Unreal headers, engine lifecycle dispatch, UFS/Pak staging, Win64/MSVC ABI, packaged operation, server behavior or performance. All genuine Unreal gates remain not_run in the bundled template.

Use acceptance-contract.md and the evidence template to record actual target results. Promote a route to project-supported only after the required gates pass. Preserve not_run for missing environments rather than converting source plausibility into a claim of success.
