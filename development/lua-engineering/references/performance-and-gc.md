# Performance, allocation, and garbage collection

Use for throughput, frame time, memory growth, startup time, or Lua/native integration bottlenecks. Treat optimization claims as hypotheses until measured on the actual runtime and workload.

## Contents

- [Define the measured outcome](#define-the-measured-outcome)
- [Find where the time goes](#find-where-the-time-goes)
- [Optimize data and boundaries](#optimize-data-and-boundaries)
- [Investigate allocation and retention](#investigate-allocation-and-retention)
- [Tune GC by runtime](#tune-gc-by-runtime)
- [Use appropriate profilers](#use-appropriate-profilers)
- [Report a defensible result](#report-a-defensible-result)
- [Sources](#sources)

## Define the measured outcome

Write a workload statement: runtime/build, target hardware, input sizes, expected output, warm/cold state, concurrency model, and the practical latency or memory requirement. A scripting benchmark that never crosses the production host boundary does not measure that boundary.

Measure the dimension that matters:

| Workload | Useful measurements |
|---|---|
| Interactive/game loop | Median and tail frame/tick time, worst pause, work backlog |
| Batch transformation | Items/second, total CPU time, peak memory, result equivalence |
| Service | Throughput at target concurrency, tail request latency, queue length |
| Embedded controller | Worst bounded work interval, allocation behavior, restart cost |
| Script startup | Compile/load time, initialization calls, first-use latency |

Keep startup/JIT warm-up separate from steady-state when both matter. Ensure the benchmark consumes/checks its result. Use representative distributions and include the largest expected input, not only a convenient average.

## Find where the time goes

Use this decomposition as an investigation model, not a predictive benchmark:

```text
total cost = algorithm work
           + scheduling/dispatch
           + native boundary and conversion
           + allocation and collection
           + I/O or waits
```

Count callbacks and native calls per operation. Measure how much data is copied or boxed at each boundary. Sample the host as well as the Lua stack so that time in a C function is not misclassified as a slow Lua caller.

Before editing hot code, answer: Is the expensive path called too often? Does it scan too much data? Does it allocate transient structures? Does it spend most of its time in a host operation? Would a different scheduling policy remove the work entirely?

## Optimize data and boundaries

Apply changes in this order unless a profile suggests otherwise:

1. Remove unnecessary work and replace unsuitable algorithms.
2. Restrict updates to changed or due items.
3. Batch native queries and updates with explicit result shapes.
4. Reuse immutable definitions and avoid rebuilding identical lookup tables.
5. Reduce allocation where it is measured to matter.
6. Consider runtime-specific idioms or native kernels last.

For collections, maintain a documented dense-sequence invariant or an explicit count. Sparse tables require another representation; their length cannot be used as an arbitrary element count. Bulk APIs should state whether their buffers are copied, borrowed, or retained, because reduced copying trades against lifetime complexity.

Do not automatically replace every `pairs` with a numeric loop, every function with an inline expression, or every table with FFI storage. Such changes may alter semantics and can increase maintenance costs. Likewise, localizing every library lookup is not a universal optimization across PUC, LuaJIT, and Luau. Luau, for example, documents specialized import and table-access optimizations that depend on its environment assumptions. [Luau performance design](https://luau.org/performance/).

If moving a kernel to native code, make one call do enough useful work to justify conversion and dispatch. Profile the complete batch path including marshaling and result consumption. Native code is also a new lifetime and failure boundary.

## Investigate allocation and retention

Distinguish **allocation rate** from **retained heap**. High temporary allocation can cause collection work without a leak. A stable live heap can coexist with increasing process memory due to allocator behavior or native resources.

For a memory investigation, capture snapshots at comparable lifecycle points: after initialization, after one workload, after repeated workloads, after documented release, and after a diagnostic collection. Track native allocations separately. `collectgarbage("count")` reports Lua-accounted memory, not every byte owned by the process. [GC interface](https://www.lua.org/manual/5.5/manual.html#pdf-collectgarbage).

Inspect likely roots: module caches, global registries, event subscriptions, pending coroutines, closure upvalues, native registry references, and unbounded result/history caches. A weak table is appropriate only when losing an entry is valid for the application; it does not substitute for releasing a required subscription or handle. [PUC GC reachability](https://www.lua.org/manual/5.4/manual.html#2.5); [5.5.1 collector traversal](https://www.lua.org/source/5.5/lgc.c.html).

Object pools are a measured tradeoff. They can reduce allocation while retaining more memory, keeping references alive accidentally, and complicating reinitialization. Test for stale fields and compare both tail latency and steady memory before retaining a pool.

## Tune GC by runtime

Never paste GC tuning numbers from another runtime or release. PUC documents that optimal GC settings are not portable across platforms/releases. Lua 5.4 and 5.5 support incremental and generational modes, but 5.5 changes tuning interfaces and major-collection behavior. [5.4 collector](https://www.lua.org/manual/5.4/manual.html#2.5); [5.5 changes](https://www.lua.org/manual/5.5/readme.html#changes).

| Runtime | Investigation rule |
|---|---|
| PUC 5.1–5.3 | Read that version's `collectgarbage` interface; do not assume 5.4 generational settings exist |
| PUC 5.4 | Mode/tuning parameters use the 5.4 interface; incremental step-size interpretation is version-specific |
| PUC 5.5 | `collectgarbage("param", name[, value])` queries/changes parameters; step work is not the old 5.4 tuning recipe |
| LuaJIT | Use its own collector/profile behavior; PUC 5.4/5.5 knobs do not describe it |
| Luau | Script GC controls are restricted; tune/measure through the selected host API |

For C hosts, port `lua_gc` varargs as well as settings: `LUA_GCSTEP` accepts an **int in Kbytes in 5.4**, but a **size_t in bytes in 5.5**. Passing the old literal type to the new variadic function can be incorrect even when compilation succeeds. Supply an explicit `size_t` and the intended byte amount in the 5.5 branch; keep the 5.4 conversion separate. The Lua-side `collectgarbage("step", n)` also changes from Kbytes to bytes. Separately, 5.4's incremental `stepsize` is logarithmic (2^n bytes), while 5.5's `stepsize` parameter is a byte count. These are distinct conversions. Sources: [5.4 C interface](https://www.lua.org/manual/5.4/manual.html#lua_gc), [5.5 C interface](https://www.lua.org/manual/5.5/manual.html#lua_gc), [5.4 incremental parameters](https://www.lua.org/manual/5.4/manual.html#2.5.1), [5.5 GC parameters](https://www.lua.org/manual/5.5/manual.html#2.5).

A 5.5-only diagnostic query:

```lua
assert(_VERSION == "Lua 5.5")
print("Lua KiB", collectgarbage("count"))
print("GC pause parameter", collectgarbage("param", "pause"))
print("GC step parameter", collectgarbage("param", "stepsize"))
```

Start with defaults, vary one setting, repeat representative runs, and keep the change only if the relevant outcome improves. Stopping GC can create a temporary benchmark improvement while deferring memory/collection cost; include the complete lifecycle when evaluating it. A manual full collection on every frame/request should be justified by measurements rather than habit.

## Use appropriate profilers

| Runtime | Primary route | Interpretation limit |
|---|---|---|
| PUC Lua | Host/native sampling plus application counters; debug hooks when suitable | Hook instrumentation can materially alter call-heavy execution |
| LuaJIT | `luajit -jp workload.lua`; investigate compilation with `-jv`/`-jdump` when relevant | Distinguish Lua, native, GC, compilation, and interpreted fallback work |
| Luau | Optimized interpreter with `--profile`; convert the resulting profile using the project's tools | Its documented sampler can attribute leaf C-function time to the calling Luau function |

Sources: [LuaJIT profiler](https://luajit.org/ext_profiler.html), [LuaJIT CLI](https://luajit.org/running.html), [Luau profiling](https://luau.org/guides/profile/).

Do not compare a debug host with an optimized host or a warmed JIT run with a cold interpreter startup and call that a language-speed comparison. Retain the harness and exact runtime identity with the result.

## Report a defensible result

For each retained optimization, report the original bottleneck, workload, before/after latency or throughput, memory impact, output-equivalence check, and any new portability/lifetime constraint. If no relevant gain remains after realistic integration overhead, remove unnecessary complexity.

Stop optimizing once the actual requirement is met unless another concrete risk remains. For simulations, input batching and work scheduling are often useful hypotheses; they are not substitutes for measuring the chosen entity model and host API.

## Sources

Checked 2026-11-22:

- [PUC 5.4 GC](https://www.lua.org/manual/5.4/manual.html#2.5), [PUC 5.5 GC API](https://www.lua.org/manual/5.5/manual.html#pdf-collectgarbage), [5.5 change summary](https://www.lua.org/manual/5.5/readme.html#changes).
- [PUC 5.5.1 collector implementation](https://www.lua.org/source/5.5/lgc.c.html).
- [LuaJIT profiler](https://luajit.org/ext_profiler.html) and [CLI controls](https://luajit.org/running.html).
- [Luau optimization design](https://luau.org/performance/), [profiling guide](https://luau.org/guides/profile/), [sandbox/GC exposure](https://luau.org/sandbox/).
