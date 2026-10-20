# Drag-and-drop, sorting, and accessible alternatives

**Read when:** building sortable lists, Kanban boards, nested drops, or palette-to-canvas interactions.

## API generation gate

The current dnd kit documentation includes a newer React integration distinct from the older `@dnd-kit/core`/`@dnd-kit/sortable` generation. Inspect installed package names and matching docs before generating sensors, providers, collision logic, or sortable hooks. React DnD and Pragmatic drag and drop are alternatives in the catalog; their integration details require a separate review.

## Separate gesture from command

A drag preview is transient. The committed domain operation should be something like `moveCard(cardId, destinationColumnId, beforeCardId)`, validated independently of pointer coordinates. Define allowed sources/targets, cross-container rules, duplicate handling, cancellation, and persistence. Keep IDs stable across filtered/virtualized views and do not use visible positions as permanent order identifiers.

Specify pointer, touch, keyboard, nested-scroll, and assistive-technology behavior. Provide menu/buttons or another non-drag way to perform essential moves. Avoid overriding text selection or input controls inside draggable elements. A drag overlay must not duplicate accessible interactive content in an unusable way.

## Canvas integration

React Flow has its own node dragging and coordinate system. For a palette drop, convert the screen position once through the flow instance, then create a domain node through a validated command. Do not nest unrelated node drag managers unless their event ownership is explicitly tested. Track which scroll/container coordinate system produced a drop.

## Acceptance

Cancel with Escape, move by keyboard, drag across scroll containers, drop outside allowed targets, reorder while remote updates arrive, and remove the item mid-drag. Test undo as a single semantic operation rather than hundreds of pointer samples. Verify server rejection restores a coherent order without overwriting another user's accepted move.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R48: dnd kit](https://dndkit.com/)
- [R49: dnd kit React quickstart](https://dndkit.com/react/quickstart/)
- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
