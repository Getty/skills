# MCP modes and exclusive library ownership

**Read when:** opening a persistent library, connecting to the desktop, or resuming after a restart.

`lightcraft-cli mcp` starts an in-process headless engine. `--library DIR` creates or opens persistent catalog storage; `--demo` supplies procedural sample photos. Passing source paths imports them into the headless session. A persistent catalog and an ephemeral imported session are not the same deployment.

A library uses an exclusive `catalog.lock`. If the desktop owns it, start/retain its control listener and use `mcp --connect 127.0.0.1:7980`. Do not delete the lock, clone an active mutable catalog or open a second headless writer to bypass the refusal. After a reconnect or desktop restart, inspect the library path, counts, active photo and selection before editing: connection recovery does not prove identity continuity.

The external library directory does not relocate preferences, logs or optional models. Copy/move imports normally use its `Originals/`; add imports refer to existing locations. Require the relevant external drive to be mounted before startup and distinguish unavailable media from a corrupt catalog.

## Keep the model's context small

Use `--compact` to omit the generated per-command tools while retaining helper tools. `list_commands` or the common `command_list` still discovers engine IDs. Generated tools use a `cmd_` prefix and convert dots to underscores, but their command parameters are prose-described/free-form rather than complete machine JSON Schemas. Do not manufacture a JSON Schema from a descriptive label and then claim upstream validation.

The core inspection loop is `doc_inspect` → `query_photos` → `get_develop`/`list_controls` → an explicit edit → `render_preview` → export. Pagination/filtering prevents a full-library dump. `select_photos` rejects unknown IDs without changing the selection. Other helpers accepting an `id` may first make that photo active; the read-only `render_preview` explicitly avoids changing selection or saving a file.

`command_batch` consists of separate edits and separate undo entries. The exporter may choose a new conflict-free filename on every call, making retries non-idempotent. Capture returned output paths rather than assuming the requested basename was used.

## Evidence

- [light-mcp](https://github.com/storytold/lightcraft/blob/701f78ea2e586d4748705f10fdf5c4181dc1fd49/docs/mcp.md)
