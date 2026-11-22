# Sources and evidence

Evidence snapshot: **2026-11-22**. Use the version-specific manual as the semantic authority, upstream source for implementation details, and the actual target runtime for host behavior. The references contain original explanations and examples; they do not replace the manuals or vendor complete third-party packages.

## Source hierarchy

1. Exact selected runtime's reference manual, release notes and bug list.
2. Matching release/commit source and headers; inspect build flags as well.
3. Library author's documentation, rockspec/build files and source tests.
4. Actual execution logs from the target host/toolchain.
5. Issue reports as reported observations, with their environment and unresolved status preserved.

Keep recommendations, documented semantics, implementation observations and measured results distinct. A current web page can describe a later patch than the binary being debugged. A successful example is evidence for its tested contract, not a general compatibility guarantee.

## Language and runtime authorities

| Source | Use |
|---|---|
| [Official versions](https://www.lua.org/versions.html) | Release history and compatibility policy |
| [Official download checksums](https://www.lua.org/ftp/) | Exact source archive provenance |
| [Known bugs](https://www.lua.org/bugs.html) | Patch-specific defects and fixes |
| [Lua 5.1 manual](https://www.lua.org/manual/5.1/manual.html) | Legacy/5.1 semantics |
| [Lua 5.2 manual](https://www.lua.org/manual/5.2/manual.html) | Environments and 5.2 transition |
| [Lua 5.3 manual](https://www.lua.org/manual/5.3/manual.html) | Integers, bitwise syntax, UTF-8 and packing |
| [Lua 5.4 manual](https://www.lua.org/manual/5.4/manual.html) | Closing variables, coroutines, GC and API |
| [Lua 5.5 manual](https://www.lua.org/manual/5.5/manual.html) | Current version-specific semantics |
| [Lua 5.5 changes](https://www.lua.org/manual/5.5/readme.html#changes) | Migration entry point |
| [Lua source browser](https://www.lua.org/source/) | Versioned implementation inspection |
| [Lua license](https://www.lua.org/license.html) | Redistribution and attribution obligations |
| [Programming in Lua editions](https://www.lua.org/pil/) | Book version context; online first edition targets 5.0 |
| [LuaJIT status](https://luajit.org/status.html) | Branch and runtime status |
| [LuaJIT extensions](https://luajit.org/extensions.html) | Differences from PUC Lua |
| [LuaJIT FFI semantics](https://luajit.org/ext_ffi_semantics.html) | Native types, pointers and callbacks |
| [Luau syntax](https://luau.org/syntax) | Dialect-specific syntax |
| [Luau compatibility](https://luau.org/compatibility) | Deliberate differences from Lua |
| [Luau sandboxing](https://luau.org/sandbox) | Host isolation and omitted facilities |

## Tools and libraries

| Source | Use |
|---|---|
| [Lua Language Server](https://github.com/LuaLS/lua-language-server) | Runtime configuration, definitions and annotations |
| [Luacheck](https://github.com/lunarmodules/luacheck) | Linting and supported language versions |
| [StyLua](https://github.com/JohnnyMorganz/StyLua) | Formatter syntax modes |
| [LuaRocks](https://github.com/luarocks/luarocks/wiki) | Trees, rockspecs, builds and dependency handling |
| [Teal](https://github.com/teal-language/tl) | Optional typed language/toolchain |
| [Busted](https://github.com/lunarmodules/busted) | Existing Lua test framework |
| [LuaUnit](https://github.com/bluebird75/luaunit) | xUnit-style tests and reports |
| [LuaSocket](https://lunarmodules.github.io/luasocket/) | Transport and protocol modules |
| [LuaSocket TCP](https://lunarmodules.github.io/luasocket/tcp.html) | Partial I/O and timeout contracts |
| [LuaFileSystem](https://lunarmodules.github.io/luafilesystem/manual.html) | Directory and attribute operations |
| [luv](https://github.com/luvit/luv) | libuv integration and lifecycle |
| [OpenResty Lua module](https://github.com/openresty/lua-nginx-module) | Host phase/yield/API contracts |
| [Lua CJSON author manual](https://www.kyne.au/~mark/software/lua-cjson-manual.html) | Format-policy examples; historical version scope |

Use these as candidates and authorities for their own interfaces, not as mandatory dependencies. Refresh support matrices before adopting new Lua syntax or native modules. A project using another established library should normally keep it unless the task supplies a reason to change.

## Bundled validation baseline

The original diagnostics and rules fixture were executed on Linux against checksum-verified official PUC Lua **5.1.5**, **5.4.9** and **5.5.1**, built with the generic target. Each runtime passed 36 semantic/rule checks. The language reference examples received 67 version-appropriate executions across those interpreters.

The minimal C host compiled against the matching 5.4.9 and 5.5.1 headers/static libraries with GCC C99, warnings enabled and warnings treated as errors. Success, syntax error, runtime error, non-string error, unsupported yield, binary-input rejection, missing-file handling and usage paths were exercised for both builds.

An independent application exercise used the skill to implement an instance-owned event dispatcher. The same 12 behavioral cases passed on 5.1.5 and 5.4.9, covering nil/false-bearing tuples, listener ordering and cancellation, changes during dispatch, callback/reporter errors and reentrant drain rejection. This checked whether the guidance could support a new implementation; the exercise is not an additional bundled framework.

These checks do **not** certify LuaJIT, Luau, Windows/MSVC, custom numeric configurations, native module loading, restricted hosts, thread behavior or Unreal integration. Run the relevant host and packaging checks when those requirements apply. See testing-and-debugging.md for commands and interpretation.

## Refresh procedure

Before changing runtime versions, check official releases/errata, tool parser support, all native ABI consumers, bytecode assets and the actual host version. Preserve the old runtime contract, run the smallest representative compatibility cases, then record the new tested matrix. Never reinterpret an untested platform as supported simply because a source file compiled elsewhere.
