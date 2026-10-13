# Threaded stories, styles and overset detection

**Read when:** flowing long text through pages or changing typography.

Treat a story as logical text and a frame as one layout container through which the story flows. A text frame's visible lines are not necessarily the entire story. `inspect_document` provides stories, frames and overset status; `get_story` exposes text, frame linkage, paragraphs, lines and the overset position.

Before replacing story text, determine whether the task authorizes replacing the whole story or only a range. `set_story_text` replaces the story, with newlines creating paragraphs. A global replacement can discard carefully scoped edits elsewhere; use an inspected range operation when required.

For publication work, define reusable character/paragraph styles instead of applying unrelated local formatting to every frame. After changing fonts, size, leading, margins or columns, reflow and inspect overset again. A visually tidy first page does not prove the final pages retained all text. Font fallback or missing glyphs can change line breaks and therefore pagination.

Keep a content checksum or text comparison across layout changes. Validate headings, tables/captions and final paragraphs as well as total character/byte count. An unchanged length alone cannot prove unchanged content. Track which frame owns each part of a story and which page/parent spread provides repeating elements.

If text is overset, do not silently shrink all type until it fits. Decide whether to add pages/frames, revise spacing/column geometry or request editorial shortening according to the brief. Preserve readable typography and report any content intentionally removed.

Use a bounded render to inspect each page, then detail crops around small type, crossings, wrapped images and frame edges. Pair that visual check with explicit story/overset inspection before saving the final layout.

## Evidence

- [design-mcp](https://github.com/storytold/designcraft/blob/main/docs/mcp.md)
- [designcraft-readme](https://github.com/storytold/designcraft/blob/main/README.md)
