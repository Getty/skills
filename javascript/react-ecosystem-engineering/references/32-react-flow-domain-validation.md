# React Flow domain validation and execution boundaries

**Read when:** a diagram represents executable work, typed dataflow, rules, or infrastructure.

## Define the domain before the canvas

Write down allowed node types, required configuration, port types, edge direction, cardinality, self-loop policy, cycle policy, and required entry/exit points. A visually connected graph is not necessarily valid or executable. Validate both a candidate connection and the complete imported/persisted document. Repeat authoritative checks in the service that executes or stores privileged work.

A connection check should reject missing nodes/ports, unknown types, incompatible directions/types, duplicates, exceeded cardinality, and prohibited cycles. For DAGs, use a bounded traversal/topological check; reconnect validation must remove the old edge first. Distinguish an invalid draft, which may remain editable, from an executable graph, which must satisfy all required constraints.

## Execution model

Choose dataflow, control-flow, or a documented hybrid. Define evaluation ordering, cache keys, invalidation, retry, timeout, cancellation, concurrency limits, and failure propagation. The UI may display intermediate results but should not become an unbounded executor merely because node data can be updated. Expensive or privileged work belongs behind a validated execution interface, potentially in a worker, server, or Electron-owned process.

Treat code/expression nodes as an explicit trust boundary. Never use `eval` on imported node data in the browser or main process. A general hostile-code executor needs an isolation design beyond React Flow and beyond ordinary Node worker/process separation.

## Validation output and tests

Return structured issues with entity/port IDs, machine-readable codes, and a user-actionable explanation. Keep import validation bounded by input size, node/edge count, string lengths, and algorithmic complexity. Test unknown discriminants, malformed coordinates, duplicate IDs, dangling ports, cycles, disallowed fan-in, and reconnecting the same edge. The bundled pure graph module executes these checks offline and is intentionally narrower than a full workflow engine.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R59: React Flow computing flows](https://reactflow.dev/learn/advanced-use/computing-flows)
- [R50: React Flow learning index](https://reactflow.dev/learn)
- [R52: React Flow handles](https://reactflow.dev/learn/customization/handles)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
