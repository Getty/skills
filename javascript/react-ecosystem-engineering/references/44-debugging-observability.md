# Debugging and observability playbooks

**Read when:** investigating broken rendering, repeated requests, crashes, or slow interactions.

## Reproduction first

Capture exact action sequence, expected/actual result, route, identity/tenant, data fixture, browser/runtime, dependency lock revision, build mode, and error stack. Remove private data from logs. Reduce the reproduction along one dimension at a time: application shell, data fetching, store, custom component, styling, and external library.

For invalid hook calls, inspect duplicate React copies, renderer compatibility, and hook placement. For effect loops, map writes to dependencies and distinguish synchronization from derivation. For repeated fetching, inspect query keys, mount/focus behavior, retries, and cache lifetime before blaming the network library. For hydration, compare initial server/client inputs and markup.

## Instrumentation

Use React/browser profiling tools to separate render work from layout and external latency. Add structured domain operation IDs rather than dumping full payloads. Track useful product signals: failed saves, stale-conflict rate, startup cost, interaction latency, resource leaks, and recovery success. Preserve privacy and define retention/access for telemetry.

For graph editors, log document revision, operation type, selected IDs, and validation code; avoid storing user-authored node content by default. For Electron, correlate renderer actions with main-process operation IDs without exposing sensitive main errors to the renderer.

## Fix validation

State the falsifiable hypothesis and the evidence that supports it. Add a minimal regression test, apply the smallest coherent correction, and retest the original scenario plus adjacent failure paths. Do not mask the symptom with extra remounting, disabled Strict Mode, swallowed errors, or relaxed security. Deliver observed root cause separately from suspected contributing factors and list the tests that could not be executed.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R01: React reference](https://react.dev/reference/react)
- [R11: hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot)
- [R18: TanStack Query defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)
- [R55: React Flow performance](https://reactflow.dev/learn/advanced-use/performance)
- [R71: Playwright](https://playwright.dev/docs/intro)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
