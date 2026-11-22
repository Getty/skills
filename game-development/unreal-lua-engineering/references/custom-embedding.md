# Narrow Lua embedding: an actionable UE 5.8 route

## Contents

- Scope and evidence
- What the scaffold implements
- Build the pinned Lua dependency
- Integrate and exercise the plugin
- Build and package explicit Client and Server targets
- Extend the host without changing its guarantees accidentally
- Sources

## Scope and evidence

This route combines Unreal's documented external-library mechanism, a world subsystem and Lua's public C API. It avoids broad reflection overrides and direct mutation of Unreal's internal field lists. That smaller integration surface is the reason to choose it for a rules-oriented simulation; it is not an assertion that an engine build has already passed.

**UE 5.8 compilation and execution of the supplied scaffold were not performed.** Treat the code as a complete implementation candidate to compile and exercise on the exact engine/toolchain. Its initial platform is **Windows x64, release dynamic CRT (`/MD`), PUC Lua 5.4.9**. Other operating systems, Windows ARM64, different CRT modes, native Lua extensions and other Lua implementations need their own builds and tests.

Copy `assets/minimal-plugin/LuaRules` into the project's `Plugins/LuaRules` directory. Keep the plugin name unless all corresponding module names, API macros and lookup strings are updated together.

## What the scaffold implements

| Part | Concrete behavior |
|---|---|
| `LuaEmbedded.Build.cs` | An External module requiring an explicitly supplied header tree and static library; fails clearly when they are absent |
| `CMakeLists.txt` | Requires a Visual Studio generator targeting x64; builds Lua's library sources as C; excludes the interpreter/compiler entry points; selects `/MD` |
| `LuaRules.Build.cs` | Runtime dependencies on Core, CoreUObject, Engine, Projects and the private Lua library; stages `main.lua` as UFS |
| `ULuaRulesSubsystem` | One `lua_State` per Game/PIE world; editor/preview worlds are excluded |
| Startup | Allocates the VM in `Initialize`; reads and executes the rule chunk at `OnWorldBeginPlay` |
| Script contract | A text chunk returning one function accepting a finite number and producing a finite number |
| Execution | Game-thread-only `Evaluate`, protected execution, strict numeric return check and stack restoration |
| Shutdown | Stops evaluation at world end play; clears the state pointer and closes Lua in `Deinitialize` |

The example `main.lua` returns a function that doubles its argument. It needs no standard library. The host intentionally opens **none**: `require`, `print`, `math`, `io`, `os`, `debug` and even the ordinary base-library helpers are absent. This does not make it a security sandbox: trusted code can still loop forever or consume memory, and no CPU/memory quota or process boundary is provided.

There is no Tick, native callback, UObject wrapper, replication, save serialization or hot reload in this scaffold. Add these as explicit features after the minimal boundary passes its tests.

## Build the pinned Lua dependency

Use the official archive `https://www.lua.org/ftp/lua-5.4.9.tar.gz`, SHA-256:

```text
2335b6c582a52654f94612bf10d2f4672805d05329aa6568b1d8cd9e5c6fb8e6
```

The archive and checksum were listed by the [official download area](https://www.lua.org/ftp/) at research time. Extract it beside the CMake file so `Source/ThirdParty/LuaEmbedded/lua-5.4.9/src/lua.h` exists. Keep the upstream license with redistributed Lua source/binaries and the appropriate product notices. The skill does not bundle Lua's source or a prebuilt library.

Run from the project directory in PowerShell; these commands are a recipe to execute in the target development environment, not an execution log:

```powershell
$luaPlugin = (Resolve-Path '.\Plugins\LuaRules').Path
$luaThirdParty = Join-Path $luaPlugin 'Source\ThirdParty\LuaEmbedded'
$luaArchive = Join-Path $luaThirdParty 'lua-5.4.9.tar.gz'
Invoke-WebRequest 'https://www.lua.org/ftp/lua-5.4.9.tar.gz' -OutFile $luaArchive
$luaExpected = '2335b6c582a52654f94612bf10d2f4672805d05329aa6568b1d8cd9e5c6fb8e6'
if ((Get-FileHash $luaArchive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $luaExpected) {
    throw 'Lua source checksum mismatch'
}
tar -xzf $luaArchive -C $luaThirdParty
if ($LASTEXITCODE -ne 0) { throw 'Lua extraction failed' }

# Select the same toolset version that the actual Unreal build uses.
# This generator is an example for an environment using Visual Studio 2022.
cmake -S $luaThirdParty -B (Join-Path $luaThirdParty 'build-win64') `
    -G 'Visual Studio 17 2022' -A x64
if ($LASTEXITCODE -ne 0) { throw 'Lua CMake configuration failed' }
cmake --build (Join-Path $luaThirdParty 'build-win64') --config Release
if ($LASTEXITCODE -ne 0) { throw 'Lua library build failed' }
```

Do not treat the example generator as a statement that every UE 5.8 installation uses that compiler. Record the compiler/toolset and Windows SDK selected by UBT; select the corresponding CMake toolset, including an explicit version when several are installed. The expected output is `lib/Win64/x64/LuaEmbedded.lib` under the third-party module. This supplied recipe deliberately rejects Ninja/NMake and other non-Visual-Studio generators: pointer width alone cannot distinguish x64 from ARM64. Add a real compiler target-architecture check and revalidate before extending the generator support. Do not rename a Linux `.a` or an ARM64 library into this x64 output path.

The supplied build rules reject static CRT and the target's debug-CRT option. Epic documents that Unreal normally uses release CRT even for many debug configurations; match the actual target rather than deriving CRT solely from its display name. A static **Lua library** and a static **C runtime** are separate choices.

## Integrate and exercise the plugin

Enable `LuaRules` in the C++ project's plugin list. Generate project files with the selected engine, then build the actual Editor target with that installation's `Engine/Build/BatchFiles/Build.bat`. Preserve the full output and first compiler/linker error if it fails. The scaffold supplies no engine binaries and requires normal UHT/UBT compilation.

In a test actor's BeginPlay, obtain `ULuaRulesSubsystem` from its world and call `Evaluate(3.0, Output, Error)`. After successful initialization, expect `true`, output `6.0` and an empty error. The subsystem's world-begin-play hook is documented to run before actor BeginPlay, but keep the explicit `IsReady`/error result and verify the actual lifecycle in the target engine.

Test the same operation from a packaged Development build. The runtime locates the plugin content directory through `IPluginManager`, reads the staged script via Unreal's file API, and converts text with a named `FTCHARToUTF8` object. It does not use raw `fopen` to read a packed script. The dependency is statically linked, so this scaffold itself does not require a separate `Lua.dll`.

## Build and package explicit Client and Server targets

**Unexecuted reference sequence:** none of the Windows commands, Unreal targets, cooking steps or runtime scenarios below were run while creating this skill. `RulesProbe`, the `D:` paths and `/Game/Maps/LuaRulesSmoke` are an adaptable example, not files or targets supplied by the scaffold. Replace them with the actual project, engine, target, map and archive paths. Preserve each command, exit code and complete log.

### Prepare the project and target files

Use a **source build of the selected UE 5.8 revision** and a C++ project for this sequence. Epic's dedicated-server tutorial requires a source engine and a C++ multiplayer project; a successful launcher Editor build does not establish that Client/Server targets are available. Record `Engine/Build/Build.version`, the source revision and the compiler/toolset/Windows SDK actually chosen by UBT. Start with a healthy C++ project and the engine's own matching target settings. [Source: dedicated-server setup](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-dedicated-servers-in-unreal-engine?application_version=5.8).

1. Copy and enable `Plugins/LuaRules`, then build the pinned x64 `/MD` Lua dependency above. Add `"LuaRules"` to the game's private module dependencies if a game `.cpp` includes `LuaRulesSubsystem.h`.
2. Keep the generated Editor and Game targets. Create the Client and Server targets by copying the project's Game `.Target.cs`, renaming its class and constructor, and changing `Type`. Preserve the actual engine's `DefaultBuildSettings`, `IncludeOrderVersion` and game-module settings; do not guess versioned enum values from another engine installation.

| Example target file under `Source/` | Class and constructor | `Type` | Game module |
|---|---|---|---|
| `RulesProbeEditor.Target.cs` | `RulesProbeEditorTarget` | `TargetType.Editor` | `RulesProbe` |
| `RulesProbeClient.Target.cs` | `RulesProbeClientTarget` | `TargetType.Client` | `RulesProbe` |
| `RulesProbeServer.Target.cs` | `RulesProbeServerTarget` | `TargetType.Server` | `RulesProbe` |

For example, the copied Client constructor must be `public RulesProbeClientTarget(TargetInfo Target) : base(Target)`, set `Type = TargetType.Client`, and retain `ExtraModuleNames.Add("RulesProbe")`. Use the corresponding Server names and `TargetType.Server` for its copy. Regenerate project files with this source engine. Target class/file matching and Client/Server separation are UBT requirements. [Source: target reference](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-build-tool-target-reference?application_version=5.8).

3. Create the smoke-test map, add it to the cook selection, and set suitable game/server default maps. Place a non-editor-only test actor whose `BeginPlay` obtains `GetWorld()->GetSubsystem<ULuaRulesSubsystem>()`, checks `IsReady()`, and calls `Evaluate(3.0, Output, Error)`. Emit an explicit pass/fail record with world, net mode, subsystem identity, output and error; success requires `true`, `6.0` and an empty error. Keep the probe in a context that runs on clients too: a GameMode-only probe would exercise only the server. Avoid relying solely on `check` or a debug console for a final Shipping result.

### Compile all three actual targets

Close the Editor before rebuilding native modules. The following PowerShell helper preserves logs and stops at the first failed native command. All paths and target names remain example values to replace:

```powershell
$luaProbeEngine = (Resolve-Path 'D:\UE_5.8_Source' -ErrorAction Stop).Path
$luaProbeProject = (Resolve-Path 'D:\Projects\RulesProbe\RulesProbe.uproject' -ErrorAction Stop).Path
$luaProbeArtifacts = 'D:\LuaRulesArtifacts'
$luaProbeLogDir = Join-Path $luaProbeArtifacts 'Logs'
New-Item -ItemType Directory -Force -Path $luaProbeLogDir -ErrorAction Stop | Out-Null
$luaProbeBuild = Join-Path $luaProbeEngine 'Engine\Build\BatchFiles\Build.bat'
$luaProbeUat = Join-Path $luaProbeEngine 'Engine\Build\BatchFiles\RunUAT.bat'

function Invoke-LuaProbeRecorded {
    param([string]$Executable, [string[]]$ToolArguments, [string]$LogPath)
    if (-not (Test-Path -LiteralPath $Executable -PathType Leaf)) {
        throw "Executable not found: $Executable"
    }
    & $Executable @ToolArguments 2>&1 | Tee-Object -FilePath $LogPath -ErrorAction Stop
    $nativeExitCode = $LASTEXITCODE
    if ($nativeExitCode -ne 0) {
        throw "Command failed with exit code $nativeExitCode; see $LogPath"
    }
}

foreach ($luaProbeTarget in @('RulesProbeEditor', 'RulesProbeClient', 'RulesProbeServer')) {
    Invoke-LuaProbeRecorded -Executable $luaProbeBuild -ToolArguments @(
        $luaProbeTarget, 'Win64', 'Development', $luaProbeProject, '-WaitMutex'
    ) -LogPath (Join-Path $luaProbeLogDir "$luaProbeTarget-build.log")
}
```

Verify that the logs identify the requested target, x64 architecture and intended toolchain. Distinguish a failed UHT/C++ compile, link failure and plugin-load failure; stop at the earliest relevant error. A target's output binary alone can be stale, so preserve the command result as well.

### Cook, stage and archive independently

Use the exact engine's `RunUAT.bat BuildCookRun -Help` and Project Launcher profiles to confirm the effective options. Epic recommends generating a command through a Custom Launch Profile and retaining the `BuildCookRun` arguments from its output log. Select the **actual Client or Server build target**, Development, x64, cook by the book, the smoke-test map, and separate package/archive destinations. A launch mode named Dedicated Server is not proof that `RulesProbeServer` was compiled. [Source: build operations and generated command lines](https://dev.epicgames.com/documentation/unreal-engine/build-operations-cooking-packaging-deploying-and-running-projects-in-unreal-engine?application_version=5.8).

These are candidate command arrays for that profile, to reconcile with the installed engine's help/output before executing. They intentionally build and stage both distributions independently:

```powershell
$luaProbeCommon = @(
    'BuildCookRun', "-project=$luaProbeProject", '-noP4', '-platform=Win64',
    '-build', '-cook', '-stage', '-package', '-pak', '-archive', '-prereqs',
    '-utf8output', '-map=/Game/Maps/LuaRulesSmoke'
)
$luaProbeClientArguments = $luaProbeCommon + @(
    '-client', '-target=RulesProbeClient', '-clientconfig=Development',
    '-clientarchitecture=x64', "-archivedirectory=$luaProbeArtifacts\Client"
)
Invoke-LuaProbeRecorded -Executable $luaProbeUat -ToolArguments $luaProbeClientArguments `
    -LogPath (Join-Path $luaProbeLogDir 'client-package.log')

$luaProbeServerArguments = $luaProbeCommon + @(
    '-server', '-noclient', '-target=RulesProbeServer', '-serverconfig=Development',
    '-serverplatform=Win64', '-serverarchitecture=x64',
    "-archivedirectory=$luaProbeArtifacts\Server"
)
Invoke-LuaProbeRecorded -Executable $luaProbeUat -ToolArguments $luaProbeServerArguments `
    -LogPath (Join-Path $luaProbeLogDir 'server-package.log')
```

Check the staged UFS manifests and actual packaged contents for `Plugins/LuaRules/Content/LuaRules/main.lua` in **both** distributions; use the package tools appropriate to the selected Pak/IoStore configuration. Record the script hash used in each build. The scalar script is deliberately staged in both targets. A future server-only script needs its own staging rule; choosing not to execute it on clients does not remove its bytes from their package.

### Run the archived builds and record acceptance

Copy the archives to a clean test directory or Windows machine with the required engine/VC runtime prerequisites and no project-source fallback. Resolve the actual archived executable locations; the following paths are examples and can vary with the engine and archive layout. Run the server in one PowerShell window and clients in separate windows:

```powershell
# Server window: replace this with the executable from the actual server archive.
$luaProbeServerExe = 'D:\LuaRulesArtifacts\Server\WindowsServer\RulesProbeServer.exe'
& $luaProbeServerExe '/Game/Maps/LuaRulesSmoke' '-port=7777' '-log' '-unattended' `
    '-abslog=D:\LuaRulesArtifacts\Logs\server-run.log'

# Client window: use the executable from the actual client archive.
$luaProbeClientExe = 'D:\LuaRulesArtifacts\Client\WindowsClient\RulesProbeClient.exe'
& $luaProbeClientExe '127.0.0.1:7777' '-log' '-windowed' '-ResX=800' '-ResY=600' `
    '-abslog=D:\LuaRulesArtifacts\Logs\client-1-run.log'
# Start a second process with client-2-run.log when checking multiple clients.
```

Require the server log to show a dedicated-server world, each connected client to show its client world, and the smoke probe to pass in each. Merely starting the processes does not prove a connection or a successful rule evaluation. The scalar evaluator implements no replication: this connection test observes host/target compatibility, not authoritative gameplay synchronization.

Run the [error and isolation probes](verification-troubleshooting.md) in the real engine: failure followed by success in the same VM, multiple PIE worlds in one process, repeated PIE stop/start, and map travel. Verify that each new counter-fixture world begins at 1 and that old worlds stop accepting evaluation. Re-cook/re-stage changed packaged fixtures; the scaffold has no script hot reload. Restore `main.lua` after probes. Repeat the package/runtime slice for Shipping when Shipping is the delivery configuration.

Keep a separate evidence record for each exact target/configuration. Fill `target.name`, `target.type`, compiler/version, toolset, Windows SDK and CRT fields; mark dedicated-server and remote-client gates required for this Client/Server deliverable. Keep unrelated fields/gates explicit, using a reason for `not_applicable`. Standalone Lua checks, metadata inspection and C++ builds against Unreal test doubles do not pass any genuine Unreal compilation, lifecycle or packaging gate.

## Extend the host without changing its guarantees accidentally

The private stack has exactly one retained function at slot 1 after initialization. Each evaluation pushes a copy, supplies one numeric argument, calls under `lua_pcall`, validates the result and restores the stack to one. No registry allocation is needed for this one-function proof. Move to a registry-managed module/function abstraction when several entry points are required; preserve protected error handling around allocations and registration.

The error formatter checks the error object's actual type before converting it. It does not invoke Lua `tostring` or arbitrary metamethods while reporting another failure. Conversion buffers remain owned by named C++ objects while their bytes are used.

Future C callbacks, library opening, table construction and registry operations introduce additional places that can raise Lua errors or allocate. Keep nonlocal Lua error propagation inside a protected C-compatible boundary; do not let it skip C++ destructors. Define an allocator/error policy before advertising recoverable resource exhaustion.

For real gameplay, replace the scalar contract with a versioned input snapshot and validated output commands. Begin with stable IDs and copied values. Add a custom module searcher using the same UFS loader, per-world authority context, cancellation and generation checks. Keep UE object operations on their permitted thread. Choose a separate untrusted-code design if mods or downloaded scripts must be isolated.

## Sources

- [Epic external libraries and UFS staging](https://dev.epicgames.com/documentation/en-us/unreal-engine/integrating-third-party-libraries-into-unreal-engine).
- [UWorldSubsystem 5.8 API and lifecycle hooks](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UWorldSubsystem?application_version=5.8); [supported world-type override](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UWorldSubsystem/DoesSupportWorldType?lang=en-US).
- [Module descriptor fields, including platform architecture lists](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Projects/FModuleDescriptor?application_version=5.8).
- [Unreal build target CRT options](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-build-tool-target-reference).
- [Lua 5.4 build source list](https://www.lua.org/manual/5.4/readme.html); [Lua C API](https://www.lua.org/manual/5.4/manual.html#4), especially load, protected calls, stack and errors.
- [Unreal character conversion lifetime](https://dev.epicgames.com/documentation/unreal-engine/character-encoding-in-unreal-engine?lang=en-US).
- [CMake `MSVC_RUNTIME_LIBRARY`](https://cmake.org/cmake/help/latest/prop_tgt/MSVC_RUNTIME_LIBRARY.html), including `MultiThreadedDLL` selection of `/MD`; [Visual Studio target platform](https://cmake.org/cmake/help/latest/variable/CMAKE_VS_PLATFORM_NAME.html).
