# Deployment, native modules, and reproducible runtime builds

Use when code works in a development shell but fails in a packaged application, when shipping native extensions, or when changing the Lua runtime embedded in a product.

## Contents

- [Define the deployment unit](#define-the-deployment-unit)
- [Choose source or bytecode intentionally](#choose-source-or-bytecode-intentionally)
- [Resolve modules predictably](#resolve-modules-predictably)
- [Match native modules to the host](#match-native-modules-to-the-host)
- [Static embedding](#static-embedding)
- [Build and release workflow](#build-and-release-workflow)
- [Diagnose packaging failures](#diagnose-packaging-failures)
- [Sources](#sources)

## Define the deployment unit

Record a manifest that can reproduce the executable behavior:

| Component | Record |
|---|---|
| Lua runtime | Implementation, version/commit, source checksum, local patches |
| Build | OS/architecture, compiler, configuration, static/shared linkage, numeric options |
| Host integration | API version, exposed libraries, loader roots, lifecycle behavior |
| Script package | Source revision, module manifest, data/schema version |
| Native modules | Their Lua headers/ABI, architecture, external libraries, build options |
| Tools | Compiler/transpiler, dependency lock, bytecode producer if used |

PUC distinguishes versions from patch releases; releases within a version are documented as ABI compatible, while a move between versions requires examining incompatibilities. Custom numeric/build configurations and vendor patches still belong in your compatibility decision. [Lua version policy](https://www.lua.org/versions.html).

## Choose source or bytecode intentionally

| Representation | Useful property | Required check |
|---|---|---|
| Plain source files | Inspectable, editable, straightforward source provenance | Packaging, load roots, update integrity |
| Source inside an archive/resource | One deployment unit with a custom loader | Error chunk names, module resolution, extraction-free loading if needed |
| PUC bytecode | Precompiled build artifact | Exact producer/consumer compatibility and trusted provenance |
| LuaJIT bytecode | LuaJIT-specific packaging options | Its branch/build-mode compatibility requirements |
| Luau compiler output | Input expected by Luau VM | Matching compiler/VM and trusted compiler output |

Do not describe bytecode as portable across Lua implementations or as protection for embedded secrets. Keep credentials outside shipped code. Preserve enough build provenance and debug information to investigate deployed errors.

PUC's binary loader checks format details, but its default verification hook does not establish arbitrary-bytecode safety. Load text only when accepting untrusted producers and handle execution separately. [PUC binary loader](https://www.lua.org/source/5.5/lundump.c.html); [LuaJIT bytecode options](https://luajit.org/running.html#opt_b); [Luau bytecode trust model](https://luau.org/sandbox/).

## Resolve modules predictably

Standard PUC module loading uses package state, searchers, Lua search paths, and native-library search paths. A host may replace this behavior entirely. Check effective values inside the deployed host rather than assuming the developer shell's paths apply. [Loader implementation](https://www.lua.org/source/5.5/loadlib.c.html); [package library](https://www.lua.org/manual/5.4/manual.html#6.3).

Recommended deployment policy:

- Use a stable module namespace independent of the launch working directory.
- Establish trusted application roots explicitly.
- Define case sensitivity and exact filename case consistently.
- Keep writable save/cache directories distinct from executable module roots.
- Decide whether environment variables may alter module search paths.
- Keep production module versions fixed for a session; define update/restart behavior.

When replacing `require`, reproduce the semantics the application needs: caching, repeated loads, errors, circular dependencies, module identity, and any additional loader result. A convenient file-read-and-execute helper is not automatically a compatible module system.

For hot updates, stage a complete versioned package, verify it, then switch at a defined lifecycle boundary. Do not overwrite half of an active dependency graph while requests continue. Migrate data deliberately if the new rules expect another schema.

## Match native modules to the host

A binary extension must match the host's runtime ABI and platform. Common PUC loaders look for exported `luaopen_...` entry points; dotted module names are transformed for the symbol lookup. Linking successfully is not proof that the correct module was found at runtime. [`findloader`, `lookforfunc`, `loadfunc`](https://www.lua.org/source/5.5/loadlib.c.html).

Before shipping an extension, verify:

1. Headers and linked runtime belong to the intended build.
2. Architecture and calling conventions match the host process.
3. Required entry points are exported with appropriate linkage.
4. Transitive native libraries are present and discovered through controlled paths.
5. Debug/release and C-runtime choices are compatible for any cross-boundary allocation.
6. The extension does not load another incompatible copy of Lua and exchange state pointers with it.
7. Ownership and error behavior obey the host's binding contract.

Use C linkage for Lua entry points compiled as C++ and the platform's required export settings. Avoid copying a shared library from a different machine merely because its filename matches. Test on the actual shipping target.

LuaJIT documents 5.1 API/ABI compatibility for ordinary C modules; that is not a promise that a PUC 5.4/5.5 module will load or that an arbitrary FFI declaration is correct. [LuaJIT compatibility](https://luajit.org/extensions.html).

Treat native-library retirement separately from script hot reload. A cached module entry is only one reference: C closures, userdata finalizers, callbacks, suspended tasks, and FFI function pointers can still enter the old library. Include release callbacks for 5.5 external-string buffers in that lifetime audit. Keep the library loaded until those users are retired and relevant cleanup has completed. PUC's standard loader retains dynamic-library handles in registry state and releases them through its own cleanup; removing `package.loaded[name]` is not an unload protocol. [PUC 5.5 loader handle ownership: `addtoclib`, `freelib`](https://www.lua.org/source/5.5/loadlib.c.html); [LuaJIT FFI library lifetime](https://luajit.org/ext_ffi_semantics.html).

For a host-managed unload, stop new dispatch, disconnect producers, resolve pending tasks, release old Lua references and native resources, and prove that no remaining function or finalizer points into the library before releasing its handle. If that condition cannot be established, keep the library loaded or replace the containing worker process. Validate cancellation and generation checks at the host boundary so late completions cannot enter retired code. These are lifecycle recommendations; neither unloading nor process replacement rolls back external effects already committed.

## Static embedding

Static linking can simplify distribution when the target should not load arbitrary dynamic modules. Register approved C modules through the documented package API or an explicit host loader. For **PUC 5.2+**, this opens a module and caches it without creating a global:

```c
/* Inside an appropriate protected initialization boundary. */
luaL_requiref(L, "host.ops", luaopen_host_ops, 0);
lua_pop(L, 1);
```

This example opens the module immediately. A lazy preload entry is a different choice. Preserve the actual module's error/lifetime requirements in either case. [`luaL_requiref`](https://www.lua.org/source/5.5/lauxlib.c.html#luaL_requiref).

For mobile, consoles, browser/WASM, or restricted embedded targets, verify the selected toolchain's support for native module loading, executable code generation, threads, filesystem access, and exception behavior. Do not infer target support from the desktop Lua syntax test. Compile and exercise the required path on that target before committing to a runtime-specific dependency.

## Build and release workflow

Prefer a reproducible project-local build over replacing a machine-wide Lua installation. PUC's distribution documents build targets, local installation, and `make test`; that test prints the interpreter version and is not an application regression suite. [PUC build instructions](https://www.lua.org/manual/5.5/readme.html#installation).

Recommended release sequence:

1. Resolve immutable source revisions and verify downloaded archives against their published checksums.
2. Build runtime and native extensions in the intended target configuration.
3. Run semantic and binding tests with that exact runtime.
4. Package scripts, resources, native dependencies, and required notices.
5. Run from a clean location/account without developer module paths.
6. Exercise startup, required module loads, error reporting, save/load, and shutdown.
7. Record the shipped manifest and retain symbols/source mapping appropriate to the product.

LuaRocks can describe platform and external dependencies, but external toolchain/library state must still be reproduced. [Rockspec format](https://github.com/luarocks/luarocks/blob/main/docs/rockspec_format.md).

## Diagnose packaging failures

| Symptom | Inspect first |
|---|---|
| `module ... not found` | Actual loader search paths/messages, package contents, module case |
| Native library present but unloadable | Loader error, transitive dependency, architecture, exported entry symbol |
| Syntax works locally, fails in product | Embedded runtime identity and source/transpiler target |
| Bad binary chunk | Bytecode producer, VM version/build, corruption/truncation |
| Works only from project directory | Relative path assumptions and current working directory |
| Works after developer setup | Undeclared global package or environment dependency |
| Crash on first native call | Header/runtime ABI, declaration, calling convention, ownership |
| Update corrupts active sessions | Mixed module versions, state schema, stale closures/callbacks |

Gather runtime identity and effective module search state before modifying paths. Preserve the original loader error instead of replacing it with a generic “Lua failed” message.

## Sources

Checked 2026-11-22:

- [Lua version policy](https://www.lua.org/versions.html), [source/checksums](https://www.lua.org/download.html), [5.5 build instructions](https://www.lua.org/manual/5.5/readme.html#installation).
- [PUC package API](https://www.lua.org/manual/5.4/manual.html#6.3), [5.5.1 module loader](https://www.lua.org/source/5.5/loadlib.c.html), [binary loader](https://www.lua.org/source/5.5/lundump.c.html), [auxiliary module loading](https://www.lua.org/source/5.5/lauxlib.c.html#luaL_requiref).
- [LuaJIT compatibility](https://luajit.org/extensions.html), [LuaJIT bytecode](https://luajit.org/running.html), [LuaJIT FFI lifetime](https://luajit.org/ext_ffi_semantics.html), [Luau sandbox/bytecode](https://luau.org/sandbox/).
- [LuaRocks rockspec](https://github.com/luarocks/luarocks/blob/main/docs/rockspec_format.md).
