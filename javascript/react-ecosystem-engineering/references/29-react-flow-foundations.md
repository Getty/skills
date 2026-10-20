# React Flow foundations and controlled graph architecture

**Read when:** creating a node editor, workflow designer, topology view, or diagram UI.

## Baseline

For the v12 generation, use `@xyflow/react`; `reactflow` belongs to the preceding package generation. Import the package stylesheet and give the canvas an explicitly sized ancestor. An empty-looking canvas is often a dimensions or CSS problem rather than missing graph data. Keep node/edge type maps at module scope or otherwise stable.

Model domain nodes/edges separately from renderer-specific transient state. Use stable node IDs, edge IDs, and handle IDs. Start controlled when the product must validate, persist, collaborate, or implement history. Assign one graph-state owner; local hook state and an external store must not independently overwrite one another.

A useful boundary is `domain command → validated document revision → React Flow projection`. React Flow handles interaction and rendering; it does not by itself define the application's execution semantics, authorization, durable persistence, or conflict policy. Start with the included pure graph model and adapt its deliberately simple numeric ports to the real domain.

## Wiring sequence

Render two static nodes and one edge first. Add controlled node/edge changes, connection creation with validation, selection, a node inspector, and an explicit save/load command. Add creation/deletion and history only after their invariants are tested. Give every custom node a typed `Node<Data, Type>` shape and preserve the union in callbacks.

Keep Canvas tools intentional: Background, Controls, MiniMap, Panel, NodeToolbar, NodeResizer, and edge controls are optional product features, not a default checklist. Use `screenToFlowPosition` for palette/context-menu creation coordinates; do not subtract a wrapper offset again when the selected API already handles conversion.

## Acceptance

Load a nested route directly, resize the host, show the canvas after being hidden, change zoom, and create a node from an external palette. Verify stable IDs across save/load and no accidental node recreation during unrelated UI updates. The example covers a small editor shell; it is not a workflow engine or a production persistence service.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R50: React Flow learning index](https://reactflow.dev/learn)
- [R54: React Flow TypeScript](https://reactflow.dev/learn/advanced-use/typescript)
- [R58: React Flow v12 migration](https://reactflow.dev/learn/troubleshooting/migrate-to-v12)
- [R60: React Flow external state](https://reactflow.dev/learn/advanced-use/state-management)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
