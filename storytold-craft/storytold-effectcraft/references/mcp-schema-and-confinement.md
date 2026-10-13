# MCP schemas, scoped access and bridge limitations

**Read when:** registering an EffectCraft agent or dealing with a denied operation.

`mcp` starts headless; `--bridge 9877` drives a desktop started with `--control 9877`. Explicit `--gpu` in headless mode attempts a GPU compositor and fails with a reason if no usable adapter is available. Inspect `get_project.renderer`/`render.backend` for actual backend information.

Use `list_commands` with `schemas:true` or `describe_command` to obtain the command schema. `execute_command` accepts `command` or `id` plus `params`; unknown command parameters are rejected in the reviewed implementation. The common `command_run` wrapper instead uses `{id,params}`. Keep those envelopes separate.

## Root flags change more than paths

MCP accepts repeatable `--automation-read-root` and `--automation-write-root`. When confined, reads are allowed under read or write roots; writes require a write root. File parameters must be absolute, inside the appropriate root, with links resolved and no `..`. With no confinement flags the previous unconfined behavior remains; do not describe it as PhotoCraft's deny-by-default policy.

The gate examines engine commands and other absolute paths in parameters, as well as implicit targets such as a project's current save path and render-queue outputs. Scoped mode refuses scripts, Execute File, revealing files, batch result references that carry file paths, and various UI-driving bridge tools. This is an intentional capability boundary: changing from a direct file command to JavaScript or a UI click is not an acceptable way around it.

## Error layers

An unknown outer MCP argument is a JSON-RPC invalid-params error. A tool/engine failure appears as `isError:true`. A response with a positive failed-step/item count is a failure even when some results succeeded. Record per-step or per-queue-item evidence.

Use bounded `render_preview` for observation without file output. Whole-window screenshots, live UI elements and pointer interaction require bridge mode and may be denied while scoped. Choose the least-authority surface that actually supports the operation rather than automatically granting unrestricted desktop control.

## Evidence

- [effect-mcp](https://github.com/storytold/effectcraft/blob/main/docs/mcp.md)
- [effect-agents](https://github.com/storytold/effectcraft/blob/main/docs/agents.md)
- [effect-cli](https://github.com/storytold/effectcraft/blob/main/apps/effectcraft-cli/src/main.rs)
