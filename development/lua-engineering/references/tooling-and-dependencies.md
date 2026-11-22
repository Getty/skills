# Tooling, type information, and dependencies

Use for creating or repairing a Lua development workflow. Configure tools for the runtime the application actually embeds; a developer's system `lua` is not necessarily that runtime.

## Contents

- [Pin the toolchain contract](#pin-the-toolchain-contract)
- [Language server and host definitions](#language-server-and-host-definitions)
- [Choose a typing workflow](#choose-a-typing-workflow)
- [Linting and formatting](#linting-and-formatting)
- [LuaRocks and dependency trees](#luarocks-and-dependency-trees)
- [Locking and reproducibility](#locking-and-reproducibility)
- [Dependency selection](#dependency-selection)
- [Sources](#sources)

## Pin the toolchain contract

Record runtime, parser target, language-server version, formatter/linter version, package-manager version, and any code-generation step. Run syntax validation with the exact supported runtime as a separate gate from editor diagnostics.

As checked 2026-11-22, tool support is uneven:

| Tool | Documented scope relevant here | Consequence |
|---|---|---|
| LuaLS | README lists PUC 5.1–5.5 and LuaJIT | Configure runtime and host libraries explicitly |
| Luacheck | README lists PUC syntax 5.1–5.4 and LuaJIT | Do not assume it understands new 5.5 constructs |
| StyLua | Documented syntax choices include Lua51/52/53/54, LuaJIT, Luau, CfxLua | Check actual release support before formatting 5.5-only source |

Sources: [LuaLS README](https://github.com/LuaLS/lua-language-server), [Luacheck README](https://github.com/lunarmodules/luacheck), [StyLua syntax selection](https://github.com/JohnnyMorganz/StyLua#configuring-runtime-syntax-selection).

A rejected valid construct may be a tool-parser gap. Confirm using a minimal file and the target interpreter before rewriting correct language code or weakening all diagnostics.

## Language server and host definitions

Use LuaLS runtime settings and library definitions to reflect the project. A project-local `.luarc.json` omits the `Lua.` prefix used by editor-level settings. Example for a **Lua 5.4 host**:

```json
{
  "runtime.version": "Lua 5.4",
  "workspace.library": ["types"],
  "diagnostics.globals": ["Host"]
}
```

This declares the global name but does not describe its members. Provide definition files for the actual host API instead of suppressing undefined-member/type diagnostics broadly. [LuaLS settings](https://luals.github.io/wiki/settings/); [definition files](https://luals.github.io/wiki/definition-files/).

For example, a definition file can describe a domain API without executing its implementation:

```lua
---@meta

---@class HostApi
local HostApi = {}

---@param entity_id integer
---@return boolean exists
function HostApi.entity_exists(entity_id) end

---@type HostApi
Host = {}
```

Keep generated or handwritten definitions synchronized with the native API version. Describe ownership, errors, units, optionality, and whether callbacks may yield in documentation comments. A type name such as `integer` alone cannot express every domain constraint.

Use LuaCATS annotations on public boundaries and ambiguous records rather than annotating every obvious local. Annotations are comments for the Lua runtime; they help tooling but do not enforce runtime validation. LuaCATS and older EmmyLua annotations are not fully cross-compatible in current LuaLS. [Annotations](https://luals.github.io/wiki/annotations/).

## Choose a typing workflow

| Goal | Route | Extra boundary to maintain |
|---|---|---|
| Keep ordinary `.lua` source | LuaLS/LuaCATS | Tool-specific static checks and truthful definitions |
| Adopt Luau | Luau language/analyzer/runtime | Host integration and Lua compatibility differences |
| Compile typed source to ordinary Lua | [Teal](https://github.com/teal-language/tl) | Compiler version, generated target, source-to-generated diagnostics |

Choose explicitly. Do not insert Luau type syntax into a PUC project or treat a Teal source file as directly executable Lua. If generated Lua is shipped, test that generated output on the target runtime and preserve traceability to its source. Do not rely on a static type checker to validate network payloads, saved files, or plugin input.

## Linting and formatting

Scope linter globals to the smallest known host surface. Prefer fixing an accidental global or unreachable branch to adding a project-wide suppression. For deliberate exceptions, use narrow suppression and a reason that a reviewer can verify.

Set formatter syntax explicitly. StyLua's default union can introduce ambiguity; the project documents conflicts such as PUC label syntax versus Luau type assertions. A **5.4** configuration could begin:

```toml
syntax = "Lua54"
column_width = 100
indent_type = "Spaces"
indent_width = 4
```

Use a check mode in CI before making broad formatting edits. Keep mechanical reformatting separate from behavior changes when that improves review. A formatter validates its own accepted grammar; it does not prove runtime or host compatibility. [StyLua configuration](https://github.com/JohnnyMorganz/StyLua#options).

## LuaRocks and dependency trees

LuaRocks packages modules and dependency information, including pure Lua and native modules. Prefer a project-specific tree with an explicit Lua version to avoid accidentally using globally installed modules. [LuaRocks usage](https://github.com/luarocks/luarocks/blob/main/docs/using_luarocks.md).

Example command shape for an existing local rockspec; replace its filename with the real project file:

```sh
luarocks --lua-version=5.4 --tree=lua_modules make project-1.0-1.rockspec
luarocks --lua-version=5.4 --tree=lua_modules list
luarocks --lua-version=5.4 --tree=lua_modules path
```

The printed paths must be integrated into the actual launcher/host. A successful installation does not mean an embedded runtime's `require` will search that tree. Check Lua paths, native paths, library linkage, and custom loaders from inside the host.

Rockspecs can separate runtime, build, and test dependencies and describe platform-specific external dependencies. Use accurate Lua constraints: declaring `lua >= 5.1` while using 5.4-only syntax misleads the resolver. [Rockspec format](https://github.com/luarocks/luarocks/blob/main/docs/rockspec_format.md).

## Locking and reproducibility

LuaRocks documents `build`/`make --pin` as the way to create `luarocks.lock` with exact transitive dependency versions. Repeating `--pin` regenerates the lock instead of preserving it. Its documented lock handling depends on the build/install workflow, including whether a binary rock embeds the lock. [Pinning documentation](https://github.com/luarocks/luarocks/blob/main/docs/pinning_versions_with_a_lock_file.md).

Recommended process:

1. Resolve dependencies in a controlled update step.
2. Review and retain the resulting lock plus exact runtime/toolchain identity.
3. Rebuild without repinning in a clean environment.
4. Verify the actual resolved package list and target runtime.
5. Retain native dependency/toolchain versions separately.

Do not describe a lock file as a complete build manifest. It does not, by itself, record every compiler option, operating-system package, vendor patch, external C library, or host API version. Prove the precise workflow used in deployment; do not assume arbitrary `luarocks install` commands consume the current directory's lock in the same way as `make`.

## Dependency selection

Choose a module based on the application's needed feature and inspect its primary repository/docs. Check supported runtimes, native dependencies, maintained branch, tests for the required feature, license, and packaging behavior. Reuse existing project choices when they satisfy the requirement; do not accumulate alternative JSON/network/test libraries without a reason.

For embedded hosts, a small reviewed dependency vendored or packaged with the application can be more predictable than resolving packages at runtime. If vendoring, preserve upstream provenance, license notices, local patches, and a repeatable update process.

Testing/debugging is covered separately. Toolchain checks should feed that workflow rather than replace execution under the real host.

## Sources

Checked 2026-11-22:

- [LuaLS](https://github.com/LuaLS/lua-language-server), [settings](https://luals.github.io/wiki/settings/), [annotations](https://luals.github.io/wiki/annotations/), [definition files](https://luals.github.io/wiki/definition-files/).
- [Luacheck](https://github.com/lunarmodules/luacheck), [StyLua](https://github.com/JohnnyMorganz/StyLua), [Teal](https://github.com/teal-language/tl).
- LuaRocks [usage](https://github.com/luarocks/luarocks/blob/main/docs/using_luarocks.md), [rockspec format](https://github.com/luarocks/luarocks/blob/main/docs/rockspec_format.md), [lock files](https://github.com/luarocks/luarocks/blob/main/docs/pinning_versions_with_a_lock_file.md).
