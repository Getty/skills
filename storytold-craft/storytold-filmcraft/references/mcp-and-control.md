# MCP, desktop bridging and error layers

**Read when:** configuring an agent session, discovering tools, or distinguishing protocol failures from command failures.

Headless MCP starts with `filmcraft-cli mcp`; add `--project FILE.fcproj` or `--demo` deliberately. Otherwise the project is empty. The desktop listener uses `filmcraft --control 9876`, and the MCP bridge uses `mcp --bridge 127.0.0.1:9876`. `--data-dir` selects user-preset storage, not a sandbox.

The reviewed MCP parser does not provide `--automation-read-root` or equivalent confinement flags. It can access files allowed to the OS account. Do not copy a PhotoCraft or WordCraft launch configuration and assume the same security boundary. Use a restricted OS user/container/VM with explicitly mounted inputs and outputs where isolation is needed; loopback networking alone is not file isolation.

## Inspect the exact tool layer

Common tools are `command_list`, `command_run`, `command_batch`, `doc_inspect` and `render_preview`. Film-specific inspection exposes bins/media items through `project_inspect` and tracks/clips/effects through `sequence_inspect`. `media_import` takes absolute paths and optional bin/image-sequence information. `render_frame` takes seconds and does not move the playhead or selection.

Tool envelopes reject unknown keys with JSON-RPC `-32602`; nested engine parameters retain their command-specific handling. An accepted tools/call request can still return `isError:true`. Malformed JSON, an unknown method, a tool error and a partly failed batch are distinct observations.

## UI only when relevant

Bridge tools include `ui_elements`, `ui_click`, `ui_drag`, `ui_key`, `ui_type`, `ui_screenshot` and `ui_control`. Prefer stable IDs discovered from the current layout; cached element rectangles can become stale after a workspace change. `render_frame` in bridge mode captures the Program monitor, whereas a whole-window screenshot includes editor chrome.

Raw control messages use `{id,method,params}` and `{id,ok,result|error}`, not an MCP JSON-RPC envelope. A successful TCP connection is not proof that the intended project is open. Inspect the live session before mutation, especially after reconnection.

## Evidence

- [film-agents](https://github.com/storytold/filmcraft/blob/main/docs/agents.md)
- [film-cli](https://github.com/storytold/filmcraft/blob/main/apps/filmcraft-cli/src/main.rs)
