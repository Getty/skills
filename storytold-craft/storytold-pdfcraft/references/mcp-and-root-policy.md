# MCP schemas, compact discovery and filesystem authority

**Read when:** starting PdfCraft automation or interpreting a validation refusal.

`pdfcraft-cli mcp --root DIR` is opt-in stdio MCP: it does not open a network port, and closes when stdin closes. The Cargo `mcp` feature controls availability; a build without it explicitly rejects the subcommand. Do not infer MCP availability from the presence of the rest of the CLI.

`--compact` retains a small core plus common command tools and `tool_search`/`tool_call`. Search by category/query or request one tool's complete input schema. An unlisted specialist tool can still be reachable through the documented compact-mode dispatch; absence from the compact list is not proof of absent engine capability.

Task tools use snake_case names, with registry IDs linked separately through `ToolDef.command`. Most task-tool schemas reject unknown fields. The common `command_run {id,params}` wrapper has a different nested-parameter contract: unmapped commands fail, and unknown nested keys can be ignored with a warnings array. Prefer direct typed tools for high-consequence edits and always inspect warnings.

## Root behavior

With a root set, every tool read/write and image-output path must resolve inside it. Relative paths are root-relative. Escaping links and parent paths are refused; external Windows share/device paths are rejected without probing them. The root must be an existing directory. Without a configured root, do not claim automatic filesystem confinement.

The desktop UI uses a separate control-descriptor file containing loopback connection information and credentials. `pdfcraft --control FILE` is not the numeric-port syntax of most sibling apps. Keep that descriptor private; use `pdfcraft-cli ui --control FILE METHOD...` only for necessary live UI work. This UI channel is not a headless MCP bridge selected by an invented `--connect` flag.

## Completion is synchronous

The reviewed exports complete synchronously. Progress tokens/cancellation notifications do not create background-job semantics. If a client times out, inspect output and document state before retrying. `command_batch` retains earlier successful edits after later errors; only specific tools that explicitly guarantee atomic edits should be treated as atomic.

## Evidence

- [pdf-automation](https://github.com/storytold/pdfcraft/blob/7163ba3dee8becfff6871c9a65d0d8314314742b/crates/automation/README.md)
- [pdf-cli](https://github.com/storytold/pdfcraft/blob/7163ba3dee8becfff6871c9a65d0d8314314742b/apps/pdfcraft-cli/src/main.rs)
- [pdfcraft-readme](https://github.com/storytold/pdfcraft/blob/main/README.md)
