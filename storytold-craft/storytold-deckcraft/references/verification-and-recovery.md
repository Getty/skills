# Presentation verification and safe recovery

**Read when:** finishing a deck or recovering after a partial sequence of edits.

Maintain a slide manifest containing logical slide identity/title, index, intended layout, important shapes and delivery inclusion. Recompute indexes after insert/delete/reorder rather than using stale ordinal targets. Separate stable content labels from session-local object IDs.

Save a checkpoint before a global theme/layout operation or a large slide-generation batch. If a batch fails, inspect the actual slide/object counts and the failed step before replaying. Duplicate slides or overlapping shapes can look plausible at a glance; do not assume failure left the deck unchanged.

Acceptance requires: the intended content/order; editable objects preserved where required; all-slide render review; correct exported page/slide count; readable small text/tables/charts; and explicit media/animation testing when those features matter. Review both a full-slide overview and detail regions.

For a handoff, provide the editable master, requested interchange/export files, external-asset manifest where needed, and unresolved compatibility limitations. Record whether the PPTX was reopened and whether animation/playback was actually tested. Source-reviewed feature support is not a substitute for those task-specific observations.

## Evidence

- [deck-cli](https://github.com/storytold/deckcraft/blob/main/apps/deckcraft-cli/src/main.rs)
- [deck-mcp](https://github.com/storytold/deckcraft/blob/main/docs/mcp.md)
- [deck-control](https://github.com/storytold/deckcraft/blob/main/docs/control-protocol.md)
