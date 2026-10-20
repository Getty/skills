# React Flow layout, subflows, geometry, and grouping

**Read when:** adding automatic layout, nested groups, routing, or coordinate transformations.

## Choose layout from graph semantics

Use a directed layout approach for hierarchical workflows, a tree approach for genuine trees, and a force layout only when free-form relationship structure justifies its motion/cost. Dagre, ELK, and d3-family algorithms are external layout options, not built-in substitutes for a domain model. Verify installed bindings, licensing, edge routing, port constraints, and compound-graph support before choosing one.

Convert domain nodes and measured dimensions into the layout engine's input. Convert its result back in one controlled transaction. Record the graph revision used to calculate a layout; discard an asynchronous result if the graph changed or a newer request superseded it. Avoid a loop where each measurement triggers a layout that triggers another measurement indefinitely.

## Subflow contract

In the reviewed v12 generation, parent relationships use `parentId`; child coordinates are relative to the parent, and parents should precede their children in the nodes array. Distinguish declared dimensions from measured dimensions according to v12 semantics. Grouping changes coordinate frames, not merely the color of a surrounding rectangle.

Define reparenting as a domain operation preserving the desired absolute visual position. Convert between screen, flow, and parent-local coordinates exactly once at each boundary. Decide containment, clipping, z-order, selection behavior, and whether deleting a group deletes or releases children. Handle edges that cross group boundaries deliberately.

## Acceptance

Layout disconnected components, cycles where allowed, very long labels, dynamic node sizes, and deeply nested groups. Reparent while zoomed and scrolled; test group resize and viewport fit after measurement completes. Verify deterministic layout where repeatability matters, and preserve user-placed nodes unless an explicit command requests re-layout. Store user intent separately from transient engine coordinates when later edits should not destroy manual placement.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R53: React Flow layouting](https://reactflow.dev/learn/layouting/layouting)
- [R61: React Flow subflows](https://reactflow.dev/learn/layouting/sub-flows)
- [R58: React Flow v12 migration](https://reactflow.dev/learn/troubleshooting/migrate-to-v12)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
