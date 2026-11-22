# Script loading, packaging, deployment and reload

Use this when files work in the editor but disappear after packaging, when adding `require`, or when changing scripts during a running session.

## Decide the source and loader together

| Delivery form | Required loader | Appropriate use |
|---|---|---|
| Files staged through Unreal's UFS | Unreal filesystem API, then compile the returned bytes/text | Project scripts that may be packed into an archive |
| Loose NonUFS files | Explicit allowed filesystem roots and ordinary/native I/O as designed | User-editable deployment files or approved mod directories |
| Plugin-defined script asset | That plugin's asset loader/cooker | Integrations such as LuaMachine's LuaCode |
| Bytecode | Exact compatible Lua implementation/build and a trusted build pipeline | Optional deployment format after source loading is proven |

Epic documents UFS versus NonUFS staging and `RuntimeDependencies.Add` in [Third-Party Libraries](https://dev.epicgames.com/documentation/en-us/unreal-engine/integrating-third-party-libraries-into-unreal-engine). Plain Lua filesystem operations do not acquire an Unreal archive reader merely because the host is Unreal. Load through the correct interface and then pass the script to Lua.

The supplied scaffold stages one plugin file as UFS and reads it through `FFileHelper::LoadFileToString`. It intentionally supplies no `require` implementation. To add modules, implement and test a loader/searcher against the same staged source manifest; do not open standard `package` and assume it discovers packed content.

## Define the module contract

Specify module-name grammar, name-to-path mapping, allowed roots, UTF-8/source policy, maximum size, manifest entry, version/hash and error behavior. Treat a module identity and a filesystem path as different inputs. Normalize once and reject traversal, absolute paths and ambiguous aliases if modules are constrained to a root.

A custom searcher should return the compiled loader and any supported loader data, or a useful failure message under the selected Lua version's `require` contract. Record the exact 5.1/5.4/Luau behavior; their loaders are not interchangeable. Source: [Lua 5.4 `package.searchers`](https://www.lua.org/manual/5.4/manual.html#pdf-package.searchers).

Prefer text-only loading for project-controlled source unless bytecode is intentionally supported. Lua's load mode distinguishes text and binary chunks; precompiled data is not a cross-runtime deployment format. Source: [Lua 5.4 `load`](https://www.lua.org/manual/5.4/manual.html#pdf-load).

## UnLua-specific inspected behavior

At the pinned revision, [`FLuaEnv::LoadFromFileSystem`](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/UnLua/Private/LuaEnv.cpp) converts dotted module names to path separators and iterates package patterns. It first searches the project's persistent-download location, then project paths, using Unreal file helpers. Custom loaders are also supported.

Therefore a stale downloaded override can shadow the file currently being edited. Include resolved origin, content version/hash and VM identity in diagnostic output. When debugging a mismatch, inspect every configured search root and cache entry instead of repeatedly rebuilding C++.

UnLua's [FAQ](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Docs/CN/FAQ.md) identifies inclusion of the Script directory in Additional Non-Asset Directories to Package. Verify effective staging even if the selected plugin version also modifies packaging defaults; the final staged manifest is the relevant result.

## Separate role selection from distribution

`server/`, `client/` and `shared/` are application conventions. Define a manifest for each target and load only the appropriate modules. A listen-server-capable Game build normally needs authoritative logic locally; a dedicated Client-only distribution may have a different set. Whether a file is present and whether it runs are separate properties.

List assets referenced by scripts in the cooking strategy. A path string in Lua is not proof that an asset will be cooked. Use the project's established asset-management or explicit inclusion mechanism and verify the packaged result. Epic separates build/cook/stage/package and provides asset rules for cooking: [Packaging](https://dev.epicgames.com/documentation/en-us/unreal-engine/packaging-your-project), [Asset Management](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-management-in-unreal-engine).

## Hot reload is a state transition

The inspected UnLua environment exposes `HotReload`, delegating to a Lua implementation. This establishes an available mechanism, not a guarantee that every application state can migrate safely. Source: [`LuaEnv.cpp::HotReload`](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/UnLua/Private/LuaEnv.cpp) and [HotReload.lua](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Content/Script/UnLua/HotReload.lua).

Use an application protocol:

1. Compile and validate candidate modules before changing live dispatch.
2. Check native API and state-schema compatibility.
3. Stop admission of new callbacks at a defined simulation boundary.
4. Preserve or migrate explicit data state; choose a policy for old closures, coroutines, listeners and cached function references.
5. Install the candidate dispatch and increment its generation.
6. Resume work; reject completions carrying the old generation where appropriate.
7. Retain a known-good version and a deliberate rollback/restart path.

Replacing `package.loaded[name]` alone cannot update every previously captured callable. Re-executing module initialization may duplicate delegates, timers or registrations. Make initialization and teardown paired and test repeated reloads. The minimal plugin has no reload feature: restart its world to load changed source.

Record reload testing separately from C++ Live Coding or native-module hot reload. A Lua-only rule change and a changed UObject layout require different handling and evidence.
