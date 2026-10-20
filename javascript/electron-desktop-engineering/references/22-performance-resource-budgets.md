# Startup, responsiveness, memory, and background resource budgets

**Read when:** the application starts slowly, main freezes, or background load grows.

## Establish budgets

Record cold/warm startup, time to useful interaction, main event-loop delay, renderer interaction latency, memory per window, background CPU, and disk/network work. Use representative data and low-end supported hardware. Distinguish Electron/runtime baseline cost from application work, but do not use baseline cost as an excuse for unbounded extra processes or polling.

## Investigate by owner

Main must not perform large synchronous reads, parsing, database queries, or CPU loops. Renderers should avoid unnecessary subscriptions, expensive hidden content, and continuous animations when idle. Native services/workers need concurrency, queue, output, and lifetime limits. Lazy loading should defer noncritical work without creating a long first-use freeze.

Measure startup stages: module loading, app readiness, window creation, asset loading, preload, renderer initialization, data recovery, and first useful view. Cache deliberately with invalidation and size limits. Preloading every optional editor, language server, and GPU scene increases startup and retained memory even when the user never opens them.

## Resource lifecycle

Track open windows, WebContents, listeners, timers, workers, child processes, database connections, object URLs, and native handles. Repeated workspace/window switching should reach a stable resource plateau. Hidden windows and background tasks need explicit inactivity policy; throttling flags are not a substitute for correct application ownership.

## Acceptance

Capture comparable traces before/after and test startup with large/corrupt state, many documents, offline services, and a busy system. Run a long-duration open/close/reconnect scenario and inspect memory/CPU. Verify cancellation and quitting stop owned work. Keep performance claims tied to exact hardware/runtime/artifact and avoid describing an isolated microbenchmark as whole-application improvement.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E18: Electron performance](https://www.electronjs.org/docs/latest/tutorial/performance)
- [E14: utilityProcess](https://www.electronjs.org/docs/latest/api/utility-process)
- [E37: Content tracing](https://www.electronjs.org/docs/latest/api/content-tracing)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
