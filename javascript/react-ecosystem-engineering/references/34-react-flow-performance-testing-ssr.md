# React Flow performance, testing, SSR, and diagnostics

**Read when:** scaling a canvas, embedding it in SSR, or debugging measurement/interaction problems.

## Diagnose in order

Check package generation and duplicate React installations, stylesheet import, parent dimensions, stable node/edge type maps, valid IDs/handles, and measured geometry before changing rendering strategy. Reduce the reproduction to two nodes and one edge, then reintroduce custom nodes, layout, store integration, and overlays one at a time.

Profile a representative graph, including heavy node content. Narrow store subscriptions, keep callbacks/type maps stable where required, and avoid every node reading the entire nodes/edges collection. Collapse details, defer expensive inspectors, and virtualize ancillary lists. Visibility optimizations can have tradeoffs; measure rather than assuming an option always improves performance.

## SSR requirements

React Flow has documented SSR/SSG support, but a server cannot infer browser layout measurements. Follow the installed version's explicit dimensions and handle-geometry requirements. Decide whether the product needs a server-rendered diagram, a static preview, or an intentionally client-only editor. Test the initial output and hydration separately. Do not claim either “React Flow can never SSR” or “it works identically without geometry inputs.”

## Test pyramid

Pure unit tests cover document validation, commands, migrations, and history. DOM component tests cover inspectors and accessible controls. Browser tests cover real dimensions, pointer/keyboard interaction, panning, zoom, handles, resize, drag/drop, and layout. JSDOM geometry mocks are limited scaffolding, not evidence of real connection hit testing.

Build fixtures for tiny, disconnected, nested, large, malformed, and maximum-supported graphs. Measure load time, interaction latency, memory after repeated document switching, and save/import round-trips. Test failed async layout and stale results. The bundle's offline graph tests execute without React; its TSX/browser examples require installation and are explicitly marked unexecuted in the validation report.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R55: React Flow performance](https://reactflow.dev/learn/advanced-use/performance)
- [R56: React Flow SSR and SSG](https://reactflow.dev/learn/advanced-use/ssr-ssg-configuration)
- [R57: React Flow testing](https://reactflow.dev/learn/advanced-use/testing)
- [R58: React Flow v12 migration](https://reactflow.dev/learn/troubleshooting/migrate-to-v12)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
