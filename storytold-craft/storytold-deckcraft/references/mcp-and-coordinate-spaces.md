# MCP tools, slide points and live UI control

**Read when:** building slides semantically or mapping pointer operations.

`deckcraft-cli mcp` starts a headless engine. `--sample` loads a sample; `--connect 7990` attaches to a desktop started with `--control 7990`. Inspect the deck before mutation, especially when sharing a live session with a person.

MCP uses `list_commands`, `run_command {command,params}`, `batch`, presentation open/save/export helpers, document/slide inspection and render tools. Semantic helpers for shapes, text, pictures, tables and charts usually avoid fragile pointer input. `batch` stops on the first error; no universal external-side-effect rollback should be inferred.

Geometry is in slide points, 1/72 inch. The documented 16:9 example is 960×540 points; inspect actual slide dimensions instead of hardcoding that for every deck. Slide-space `ui.pointer` coordinates are not screen coordinates. Live `ui.click`/`ui.drag` use screen points, requiring current canvas/slide rectangles and scale.

Raw control messages use `{id,method,params}` and a success/error envelope. The MCP wrapper is a different protocol. `call_app` in connected mode can invoke control methods; do not invent a second unauthenticated public HTTP interface from the existence of a loopback control listener.

Whole-window screenshots verify editor state. `render_slide` or `ui.render` verifies slide content. Slide-show start/end and keyboard navigation affect a live presentation; obtain permission before taking over a presenter's active window. A successful headless render does not show that presenter mode, notes or playback interactions work.

## Evidence

- [deck-control](https://github.com/storytold/deckcraft/blob/main/docs/control-protocol.md)
- [deck-mcp](https://github.com/storytold/deckcraft/blob/main/docs/mcp.md)
