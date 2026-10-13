# Targeted vector inspection and object-level edits

**Read when:** working on large documents or manipulating geometry and appearance without dumping the full model.

Begin with document summary, artboards and layers, then fetch only the relevant object subtree. `vectorcraft://document/json` can be very large; prefer `vectorcraft://object/{id}` or `run_command` with `document.node`. Summary mode supports depth and child-count limits, with `childCount` indicating a truncated listing. A truncated subtree is not evidence that the hidden remainder is empty.

A live object query can report geometry, bounds, paint and children. Preserve the distinction between object identity, stacking order, group membership and current selection. Use unique IDs obtained from the current session; names or ordinal positions alone are unsafe after reorder/group operations.

The registry is also available through `vectorcraft://commands` and individual `vectorcraft://command/{id}` resources. Effects and swatches have targeted resources. Retrieve the exact operation's parameter documentation and current enablement before constructing transformations or path operations.

## Edit reasoning

A vector object can have editable geometry plus strokes, fills, transforms and live effects. A bounding rectangle alone does not describe its path topology or visible stroke extent. Before a boolean operation or outlining, preserve a working copy and define which editability must survive. After the operation inspect object count, grouping, transforms and appearance, then render a bounded crop around the change.

Selection-sensitive commands require an explicit selection check. Never infer that a click selected the intended underlying object when overlapping or clipped objects share the same screen region. Prefer object-level commands when available; use live pointer input only when its interaction semantics are needed.

For repeated assets, capture the style/geometry intent and reconstruct targets from fresh IDs. Do not store session-local IDs in an ostensibly portable template. Validate one item before applying a mutation across a whole artboard set.

## Evidence

- [vector-mcp](https://github.com/storytold/vectorcraft/blob/main/docs/mcp.md)
- [vectorcraft-readme](https://github.com/storytold/vectorcraft/blob/main/README.md)
