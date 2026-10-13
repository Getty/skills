# Static versus live presentation behavior

**Read when:** using media/transitions or exporting PowerPoint/PDF deliverables.

A static slide render validates one visual state. It does not validate animation order, timings, transitions, media playback, hyperlinks or presenter behavior. Discover `transition.set`, `animation.set` and relevant media commands from the installed catalog and inspect the resulting slide structure.

Record external media dependencies and supported playback paths. Do not treat a linked video thumbnail as proof that the video was embedded or is available on another machine. When a presentation must work offline, test that handoff condition explicitly in an authorized environment.

PPTX export and native save serve different purposes. Preserve a `.deckcraft` master and reopen the actual `.pptx` delivery to compare slide count/order, layouts, shapes, text, charts/tables, animations and media references as applicable. An importer accepting a package does not imply full round-trip parity.

PDF exports can use slide pages, notes pages or handout layouts. Choose the layout explicitly; a handout page count differs from slide count. Raster conversion can cover only the first slide, so use all-slide rendering for an audit. Exporting to PDF also changes interactivity and editability; disclose that as a delivery property rather than presenting it as equivalent to a live deck.

If only static validation was possible, label that scope. Do not claim playback success, accessibility compliance or PowerPoint-perfect fidelity from a set of PNG previews.

## Evidence

- [deck-mcp](https://github.com/storytold/deckcraft/blob/main/docs/mcp.md)
- [deck-control](https://github.com/storytold/deckcraft/blob/main/docs/control-protocol.md)
- [deck-cli](https://github.com/storytold/deckcraft/blob/main/apps/deckcraft-cli/src/main.rs)
- [deckcraft-readme](https://github.com/storytold/deckcraft/blob/main/README.md)
