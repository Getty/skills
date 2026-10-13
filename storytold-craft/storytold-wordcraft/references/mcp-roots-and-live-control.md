# Headless MCP, authorship and live control keys

**Read when:** opening an agent session or choosing a confinement boundary.

`wordcraft-cli mcp` is headless. `mcp --connect 127.0.0.1:7981` uses a desktop started with `wordcraft --control 7981`. The bridge reads the control key from `WORDCRAFT_CONTROL_KEY` or the application's key file and sends it only to loopback addresses. Protect the key file and do not put a real key into a shared configuration example.

Headless startup accepts `--author NAME`; alternatively call `file.setAuthor`. Name the agent's role so reviewers can distinguish its revisions/comments from other authors. Authorship labels are review metadata, not authentication or proof of identity.

## Optional path confinement

Headless MCP supports separate existing read/write roots. With confinement active, an omitted corresponding root grants no such file authority. Relative paths are resolved against the working directory before checks. Roots constrain document opens, templates, images, mail-merge inputs, comparisons and many save/export operations.

The root flags cannot be combined with `--connect`. The reviewed desktop does not provide equivalent root flags, so a live bridge is not a scoped substitute. Without the root flags do not describe the headless server as automatically sandboxed. Root checks do not prevent all non-filesystem effects: the local Zotero integration uses sockets, and in-memory document reads/edits remain possible.

## Tools and verification

Use `list_commands` with `query`, `execute {command,params}`, `inspect_document`, `get_text` and `render_page`. `type_text` can split lines into paragraphs when explicitly requested. `select_text` selects a chosen occurrence; inspect the occurrence and surrounding content before a revision. Open/save helper tools do not share the PhotoCraft `doc_*` names.

A connected window adds screenshot/click/key/UI inspection. Prefer semantic text and style commands; UI automation is justified for interaction-specific state, not as a workaround for a rejected filesystem operation.

## Evidence

- [word-mcp](https://github.com/storytold/wordcraft/blob/main/docs/mcp.md)
- [word-cli](https://github.com/storytold/wordcraft/blob/main/apps/wordcraft-cli/src/main.rs)
