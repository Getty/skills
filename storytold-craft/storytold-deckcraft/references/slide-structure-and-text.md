# Editable shapes, layouts and text hierarchy

**Read when:** turning an outline into a structured presentation.

Start with presentation size, theme, slide count and a content outline. Choose appropriate layouts and placeholders instead of putting every element into independent anonymous rectangles. Inspect existing slide and shape IDs; do not persist IDs from the sample deck into a reopened or different deck.

The registry includes `slide.new`, shape insertion/connection/freeform/merge, formatting, theme, table and chart families. Retrieve each selected command's schema/parameter docs before constructing geometry. Rectangles, connectors, grouped objects and placeholder text have distinct semantics even when their previews look similar.

Preserve the user's intended text hierarchy and editability. A rendered screenshot of an entire slide is not an editable replacement for shapes, tables or charts. Use native text boxes/placeholders and inspect actual text after changes. Font fallback can alter line breaks and cause overflow; verify at the renderer used for the final export.

For repeated slides, create one representative layout and validate its margins, alignment, typography and reading order before replication. Binding fresh returned IDs avoids editing a previous slide accidentally. When changing a global theme or layout, re-render affected slides rather than assuming local positions remain suitable.

Check text fit, overlaps, clipping, contrast and chart/table legibility at ordinary viewing size. Also inspect notes and hidden slides if the delivery includes them. A successful file export cannot establish that the narrative order or displayed figures match the brief; perform explicit content comparison.

## Evidence

- [deck-mcp](https://github.com/storytold/deckcraft/blob/main/docs/mcp.md)
- [deck-control](https://github.com/storytold/deckcraft/blob/main/docs/control-protocol.md)
- [deckcraft-readme](https://github.com/storytold/deckcraft/blob/main/README.md)
