# Building and porting UnLua for an exact Unreal revision

Use this only for the UnLua route. The inspected upstream baseline is `4a534502bbf2c5e51b456d9142acfa631e53350c`; no UE 5.8 build was executed here.

## Establish a reproducible input

Record the original repository, full source SHA, submodules/vendor files, Lua version/configuration, local patch commits and target matrix. Keep an engine-version port separate from a runtime upgrade or gameplay refactor so failures remain attributable.

A Git checkout is not sufficient evidence that all bundled runtime libraries match its source. In the inspected implementation, [`Lua.Build.cs`](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/ThirdParty/Lua/Lua.Build.cs) chooses the Lua source directory and library paths, can invoke CMake when outputs are absent, and selects `lua-5.4.3` by default. Inspect `DefaultUnLuaEditor.ini` and the actual library artifacts before interpreting `_VERSION`.

The baseline descriptor has Runtime `UnLua`, Editor `UnLuaEditor`, and Program `UnLuaDefaultParamCollector` modules with different loading phases/platform lists. Build the project's real targets; a successful Runtime compilation alone cannot certify the Editor or a commandlet. Source: [UnLua.uplugin](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/UnLua.uplugin).

## Classify the first real failure

| Failure layer | Inspect first | Avoid |
|---|---|---|
| C# build rules | Exact UBT declarations and preprocessor guards in `*.Build.cs` | Editing C++ to repair a C# rules error |
| C/C++ compile | The changed declaration in the installed engine and the calling plugin symbol | Copying casts from issue comments without ownership analysis |
| Link | Platform, architecture, CRT, exported C symbols, source/header/runtime match | Adding random libraries until the link passes |
| Module startup | DLL staging, plugin dependencies, load phase, build identity | Treating "could not load module" as proof of bad Lua syntax |
| UObject/Blueprint runtime | Binding, reflection caches, reinstancing, GC roots and delegate lifetimes | Declaring success after the editor merely opens |
| Packaged startup | Runtime module inclusion, Lua source manifest, loader path, assets | Using editor filesystem visibility as a packaging test |

[Epic's external-library guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/integrating-third-party-libraries-into-unreal-engine) describes linking, dynamic-library loading and staging. Match the actual failure to one of these boundaries.

## Known build-rules evidence

[Issue 754](https://github.com/Tencent/UnLua/issues/754) reports UE 5.6 failures involving deprecated warning settings and a removed `WindowsCompiler.VisualStudio2019` enum member. At the inspected `develop` SHA, the third-party rules already contain version-conditioned warning settings and guard the VS2019 branch. Therefore reproduce against the selected SHA before reapplying an old fix. Existing guards are evidence of an attempted compatibility adjustment, not evidence that all 5.8 rules compile.

Capture the earliest error with file and symbol, including errors that precede the final generic "module missing" message. Build once with the editor closed when checking a native source port; a live editor reload is a different experiment.

## The reflection-list problem

The 5.8 API reference declares [`UField::Next`](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/CoreUObject/UField?application_version=5.8) as `TObjectPtr<UField>`. The inspected [`ULuaOverridesClass::AddToOwner` and `RemoveFromOwner`](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/UnLua/Private/LuaOverridesClass.cpp) traverse `Children`/`Next` using pointer-to-pointer operations. For newer-engine branches they first copy `Class->Children.Get()` into a local raw pointer. [Issue 763](https://github.com/Tencent/UnLua/issues/763) reports the resulting raw-pointer-versus-`TObjectPtr` assignment failure and proposes a C-style cast.

**Do not apply that cast as a verified fix.** It suppresses a type mismatch without establishing the required assignment semantics. Epic documents that `TObjectPtr` participates in GC barriers; access to its storage as a raw `UField**` needs justification beyond identical-looking layouts. Source: [Object Pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine).

Derive the port against the actual headers:

1. Inspect the declared types and accessibility of the owner head and each link.
2. Determine whether insertion/removal is supported through a current engine helper or must update the documented field links directly.
3. Update the actual owner head when the list is empty; writing to a local `.Get()` copy cannot change that head.
4. For nonempty lists, retain predecessor/current nodes or use a type-correct link abstraction. Assign through the real typed fields.
5. Preserve nodes following the removed node unless the engine/plugin invariant proves that node must be the tail.
6. Preserve duplicate-insertion handling, root/unroot behavior and function-map invalidation.

These are algorithmic requirements inferred from the inspected list operations, **not a supplied 5.8 patch**. Verify local header contracts before authoring code.

Test empty, one-node, head, middle and tail cases; repeated activation/deactivation; repeated Blueprint compilation; hot reload; class destruction; and GC while bindings exist. A compile-only cast fix fails this acceptance standard.

## Finish the port without obscuring scope

Build Development Editor first, then the actual Game/Client/Server targets required by the project, and finally the intended Shipping configuration. Keep a log for each command and target. Epic's [dedicated-server procedure](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-dedicated-servers-in-unreal-engine) assumes a source engine build and a multiplayer C++ project; confirm the user's installed/source build supplies the required targets.

Report the resulting support statement narrowly: exact engine/toolchain/platform, source SHA plus patches, builds passed, runtime cases passed and remaining gaps. If broad reflection porting exceeds the project's need, implement the small game API described in `custom-embedding.md` instead of carrying unreviewed internal-engine mutations.
