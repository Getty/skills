# MCP identity, spread geometry and UTF-8 byte offsets

**Read when:** placing frames or editing text through a stateful agent.

`designcraft-cli mcp` starts an in-process headless engine with an empty Letter document; use `--sample` deliberately. `--connect PORT` or HOST:PORT targets a desktop started with `--control`. Reconnecting does not automatically resend a failed command because it may already have completed. Inspect first.

MCP `execute` takes `{command,params}`. `batch` accepts command entries or script text and stops on failure, reporting `failedIndex`. Result references such as `$N.path` are part of this engine's script/batch facility, not a universal MCP feature. Retain earlier result IDs and check partial state rather than assuming rollback.

## Geometry

Coordinates are points (1/72 inch), y downward, in spread space. A right-hand page on a facing spread begins after the left page's width, not at the spread origin. `inspect_document` reports page bounds. `render_page` and `export_png` page indexes are zero-based. Screen input uses a separate coordinate space derived from `ui_inspect.canvasRect` and display scale.

Never send screenshot pixels directly as page points. Map screen to canvas to spread/page using current zoom and origins, or bypass the UI with a frame command whose exact rectangle schema has been inspected.

## Text positions

Story positions use UTF-8 bytes: selection anchor/focus, replace-range endpoints, search-match ranges, caret positions, reported story length and overset location. They are not Unicode character counts or UTF-16 code units. For `Aéは`, the character boundaries in UTF-8 are 0, 1, 3 and 6. An interior-byte position can snap backward to a character start, hiding a caller's offset error.

Compute offsets from the exact current story text, not a normalized or translated copy. Check that each endpoint is a byte boundary and that the story has not changed since discovery. After replacement, reacquire offsets for later edits; old positions after the replacement are stale.

## Evidence

- [design-mcp](https://github.com/storytold/designcraft/blob/main/docs/mcp.md)
