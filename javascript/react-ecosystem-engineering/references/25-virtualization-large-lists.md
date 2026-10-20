# Virtualization, infinite lists, and scroll correctness

**Read when:** rendering thousands of rows/items/nodes or diagnosing scrolling cost.

## Select the abstraction

TanStack Virtual is headless; React Virtuoso supplies higher-level list-oriented behavior. Choose based on item measurement, chat/reverse loading, grouping, grids, sticky content, and scroll restoration. Do not assume a DOM list virtualizer can replace a graph renderer's own visibility and coordinate handling.

Establish the data-loading boundary separately from the rendering window. Virtualization reduces mounted presentation; it does not reduce the total dataset, network response, filter cost, or retained state by itself. Bound both loaded data and rendered elements where necessary.

## Measurement contract

Use stable item keys and accurate estimates. Account for variable heights, font loading, images, expanded content, borders, and zoom. Preserve the visible anchor when inserting earlier messages or replacing optimistic items. Never assign component state by visible index when recycling a row can associate it with another entity.

Define overscan through measurement, not a magic constant. More overscan can reduce flashing but increases render/layout work. For keyboard navigation, ensure the active item exists when focus moves, and expose position/size semantics only when they are accurate. Search, browser find, printing, and copy/export may need non-virtualized alternatives.

## Acceptance

Jump to an item far away, append and prepend data, change item height after an image loads, delete the focused item, restore scroll after navigation, and resize the container. Test low-end hardware and fast wheel/touch scrolling with production styling. Profile layout thrashing and listener cleanup after repeated mount/unmount. Record both interaction latency and memory use; a smooth small demonstration is not evidence for the target dataset.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R42: TanStack Virtual](https://tanstack.com/virtual/latest)
- [R43: React Virtuoso](https://virtuoso.dev/)
- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)
- [R55: React Flow performance](https://reactflow.dev/learn/advanced-use/performance)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
