# MCP sessions and drawing inspection

**Read when:** operating CADCraft through an agent or a live desktop.

`cadcraft-cli mcp` starts a headless engine. `mcp --connect 127.0.0.1:7979` bridges to a desktop started with `--control 7979`. Do not assume port 7979 identifies CADCraft: VectorCraft, DesignCraft and GridCraft use the same documented default in their own setups. Allocate distinct ports and verify the application/session identity before mutation.

The reviewed public surface includes `command_line`, `execute`, `inspect_drawing`, `query_entities` and `render`. Connected mode adds window-specific observation/input such as `screenshot` and `ui_click`. Use drawing/entity inspection to identify targets, not screenshots alone.

The engine's model contains entities, layers, blocks, styles, constraints and spaces. A visible line can be part of a block or a paper-space viewport representation rather than a directly editable model-space entity. Query the relevant IDs/types and active space before selecting an edit.

Command discovery provides the actual accepted operation names and parameters. AutoCAD-like command aliases and interactive behavior do not establish a complete AutoCAD API clone. Do not assume an unsupported 3D/entity operation exists because a similar application supports it.

No universal suite authentication or root-confinement configuration is established for this surface by the reviewed CAD sources. Keep the listener loopback-only and use appropriate process/account isolation. Do not claim that PhotoCraft's token or WordCraft's root flags apply to CADCraft without verifying its installed options.

A transport timeout after a mutating command is an uncertain outcome: inspect entity state, history and saved paths before retrying. Prefer a saved working copy before destructive geometry or import-normalization operations.

## Evidence

- [cad-readme-detail](https://github.com/storytold/cadcraft/blob/main/README.md)
- [cad-cli](https://github.com/storytold/cadcraft/blob/main/apps/cadcraft-cli/src/main.rs)
