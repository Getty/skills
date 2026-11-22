# Runtime selection, versions, and portability

Reviewed against primary sources on 2026-11-22. Treat release facts as a dated snapshot; inspect the actual host before choosing syntax, libraries, native modules, or bytecode.

## Contents

- [Identify the runtime contract](#identify-the-runtime-contract)
- [Version boundaries](#version-boundaries)
- [Selection and migration workflow](#selection-and-migration-workflow)
- [Portable boundaries](#portable-boundaries)
- [Evidence and acceptance](#evidence-and-acceptance)

## Identify the runtime contract

Before changing code, record all of these:

| Property | Evidence to collect | Decision it controls |
|---|---|---|
| Implementation | `_VERSION`, host documentation, `jit.version` when present, embedded source/headers | PUC Lua, LuaJIT, and Luau require different contracts |
| Exact release | Interpreter `-v`, build manifest, vendored source version | Bug fixes, available C functions, known defects |
| Language version | Parser/compiler used by the actual host | Whether newer syntax can even be loaded |
| Numeric configuration | `math.type`, integer bounds, native configuration | IDs, overflow, serialization, wire formats |
| Platform and ABI | Architecture, compiler/runtime, linkage, host plugin version | Native extension compatibility |
| Libraries and loaders | `package.path`, `package.cpath`, available globals, host loading rules | Dependency resolution and capabilities |
| Execution model | CLI, embedded single state, separate states, event loop | State lifetime, scheduling, cancellation |
| Support policy | Upstream release policy plus host commitments | Whether an old runtime is an intentional dependency |

Do not install a new system interpreter and assume an application embedding its own Lua will use it. A syntax checker, editor language server, and application must target the same language contract. This is a workflow recommendation derived from Lua's embedding model and incompatibility rules. [Embedding model](https://www.lua.org/manual/5.5/manual.html#1), [version policy](https://www.lua.org/versions.html).

## Version boundaries

The official version page identifies **5.5.1** as current, released 2026-08-03, and **5.4.9** as the final 5.4 release, released 2026-08-25. Recheck the [official chronology](https://www.lua.org/versions.html) when making a new deployment decision. “Lua 5” is not a compatibility specification.

| PUC Lua target | Distinctive boundary for application code | Check before migration |
|---|---|---|
| 5.1 | Function environments with `getfenv`/`setfenv`; global `unpack`; legacy `module` | Libraries often assume 5.1-specific globals and C APIs |
| 5.2 | Lexical `_ENV`; `table.pack`/`table.unpack`; `package.searchers`; `goto`; `bit32` | Environment manipulation, module loaders, yield boundaries |
| 5.3 | Integer/float distinction, `//`, bitwise operators, UTF-8 library, binary packing | Numeric coercion, large IDs, bit-operation replacements |
| 5.4 | `<const>` and `<close>`, `coroutine.close`, generational GC | Cleanup/cancellation, finalizer behavior, C API changes |
| 5.5 | Global declarations, named vararg tables, read-only loop variables, `table.create`, changed GC controls | Parser compatibility, additional return values, embedding rebuild |

Sources: [5.1 manual](https://www.lua.org/manual/5.1/manual.html), [5.2 changes](https://www.lua.org/manual/5.2/manual.html#8), [5.3 changes](https://www.lua.org/manual/5.3/manual.html#8), [5.4 changes](https://www.lua.org/manual/5.4/manual.html#8), [5.5 changes](https://www.lua.org/manual/5.5/manual.html#8).

**LuaJIT and Luau are independent implementation choices.** Do not treat their version numbers as PUC Lua compatibility levels, or copy `table.create`, FFI, typing, or JIT assumptions between them. Consult their own [LuaJIT compatibility documentation](https://luajit.org/extensions.html) and [Luau compatibility documentation](https://luau.org/compatibility). Their detailed operating constraints belong in the runtime-specific references.

## Selection and migration workflow

1. **Start from the deployment host.** For an existing game, editor, appliance, or server module, its supported runtime controls the choice.
2. **List required capabilities.** Include native libraries, CPU architectures, static/dynamic linking, host scheduler, sandbox boundary, editor tooling, and support horizon.
3. **Choose one declared baseline.** A standalone application with full control may choose a recent PUC release; a plugin may deliberately retain an older version. Record the reason.
4. **Inventory incompatibilities before edits.** Search for removed names, environment manipulation, bytecode loaders, integer-sensitive code, GC tuning, and native extension entry points.
5. **Compile every supported source file with every supported parser.** Runtime `if` statements cannot hide unsupported syntax from a parser. Put version-specific source in separately loaded modules.
6. **Execute behavioral probes.** Include nil-bearing returns, failed coroutines, large numbers, binary formats, module loading, iteration assumptions, and cleanup.
7. **Rebuild native artifacts.** Re-run host integration and packaged deployment tests. A successful CLI run does not establish embedded compatibility.

Use a narrow compatibility module rather than distributing version checks throughout the application:

```lua
-- Parses on PUC Lua 5.1–5.5.
local M = {}
M.unpack = table.unpack or unpack
M.pack = table.pack or function(...)
    return { n = select('#', ...), ... }
end
return M
```

A compatibility module can normalize a missing library function. It cannot make a 5.1 parser understand `<close>` or make a double-only numeric model preserve arbitrary 64-bit integer IDs. [5.1 syntax](https://www.lua.org/manual/5.1/manual.html#2), [5.4 declarations](https://www.lua.org/manual/5.4/manual.html#3.3.7).

## Portable boundaries

- Use source distribution as the default across different Lua versions. Precompiled chunks are version-specific; native modules require the appropriate ABI. Keep release/build metadata beside cached bytecode. [Official compatibility policy](https://www.lua.org/versions.html).
- Use strings for external identifiers when an endpoint cannot guarantee the required integer range. Define finite-number, integer, and range checks at serialization boundaries.
- Specify encoding, locale assumptions, time zone, binary endianness, and filesystem path behavior independently of Lua syntax.
- Treat optional compatibility compiler flags as migration aids. Test without them before claiming support for a new baseline. [5.5 incompatibilities](https://www.lua.org/manual/5.5/manual.html#8).
- Keep runtime-sensitive integration modules separate from pure domain modules so alternate hosts can reuse the latter with a controlled adapter.

## Evidence and acceptance

A compatibility claim should name implementation, exact release, platform, host, tested features, and omissions. “5.1–5.5 compatible” requires execution on that matrix, not merely avoidance of obvious new syntax. Record parse-only checks separately from behavioral tests, and desktop CLI tests separately from embedded tests.

The build sources and checksums are published in the [official download archive](https://www.lua.org/ftp/). Release dates and archive timestamps are different fields; preserve their meaning in manifests.
