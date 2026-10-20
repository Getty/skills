# React Compiler and evidence-led performance work

**Read when:** UI is slow, memoization proliferates, or enabling the compiler.

## Measure the bottleneck

Capture a representative interaction with a production-like dataset and build. Separate input delay, JavaScript execution, React commit work, layout/paint, network wait, and backend latency. Record hardware, browser, warm/cold cache, dataset size, and percentile targets. A faster local demo with fewer nodes is not a valid before/after comparison.

React Compiler 1.0 is stable, but enabling it remains a toolchain and library-compatibility change. Check compiler/lint integration for the installed framework. Roll it out with diagnostics and tests; do not assume every component is compiled. Correctness must not depend on a memoization optimization. Keep component rendering and hooks consistent with React's rules.

## Optimization order

Remove duplicated work and broad subscriptions; isolate rapidly changing state; avoid effects that create additional update chains; virtualize genuinely large collections; reduce payloads and expensive dependency loading; offload heavy pure computation. Add targeted memoization only with a clear unstable identity or expensive calculation and measured improvement. Compiler adoption does not excuse passing giant mutable objects or subscribing every node to the full graph.

Set independent budgets for initial transfer, startup execution, interaction latency, and retained memory. Lazy-load editors, maps, rich charts, and 3D features at meaningful route or feature boundaries. Preserve a loading/error state for failed chunks after deployment.

## Acceptance

Repeat the same scenario before and after, including worst-case content and low-end hardware. Check behavior under Strict Mode and browser back/forward navigation. Look for stale values introduced by an incomplete dependency array or unsafe custom comparator. Keep regression thresholds in CI where measurement variance permits; otherwise archive comparable traces and document the manual gate.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R03: React Compiler 1.0](https://react.dev/blog/2025/10/07/react-compiler-1)
- [R01: React reference](https://react.dev/reference/react)
- [R55: React Flow performance](https://reactflow.dev/learn/advanced-use/performance)
- [R74: Vite](https://vite.dev/guide/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
