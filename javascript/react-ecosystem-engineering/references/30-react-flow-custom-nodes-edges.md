# React Flow custom nodes, edges, handles, and inspectors

**Read when:** building domain-specific nodes, ports, edge controls, or embedded node editors.

## Node contract

Define a discriminated node union and use the corresponding `NodeProps<SpecificNode>` type. Keep serializable node data separate from callbacks, DOM references, credentials, and execution results. A node's visual component should issue commands by ID, not retain a stale snapshot and replace the whole graph. Subscribe an inspector to its selected entity rather than every drag update in the graph.

A port needs stable identity, direction, data type, cardinality, and connection policy. Render handles from those domain definitions. When handle count or placement changes, use the appropriate node-internals update mechanism after the DOM reflects the change. Preserve measurable handles: hiding them with `display: none` can make connection geometry unavailable. Check the current library guidance for invisible/disabled presentation.

## Interaction ownership

Inputs, buttons, scrollable panels, and resizers inside nodes must not unintentionally initiate node dragging or canvas panning. Apply the library's intended interaction classes/props such as `nodrag`, `nopan`, or `nowheel` only where needed, then test touch and keyboard behavior. Avoid making the entire node a button containing other buttons.

Custom edges should preserve a usable hit area, label placement, selection state, and accessible operations. Reuse path/base-edge helpers when they fit instead of reproducing coordinate mathematics. Edge labels rendered through portals need explicit pointer-event and stacking decisions. Reconnection is a domain edit: validate while excluding the original edge from duplicate/cycle checks.

## Acceptance

Add/remove ports, resize nodes, edit text while zoomed, reconnect an edge, and delete a selected node. Assert that incident edges are handled by an explicit policy and port references never dangle. Test keyboard selection, alternative connect commands, high-contrast states, and meaningful node/port names. Do not rely solely on color to distinguish valid and invalid targets.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R51: React Flow custom nodes](https://reactflow.dev/learn/customization/custom-nodes)
- [R52: React Flow handles](https://reactflow.dev/learn/customization/handles)
- [R54: React Flow TypeScript](https://reactflow.dev/learn/advanced-use/typescript)
- [R50: React Flow learning index](https://reactflow.dev/learn)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
