# Import modes, metadata and source-file preservation

**Read when:** importing a shoot, moving originals, creating albums or handing off RAW edits.

Select import mode deliberately. Add-mode retains source paths. Copy-mode produces managed originals under the selected destination, normally the library's `Originals/`. Move-mode removes source files and associated XMP sidecars only after copying and cataloging succeeds. Duplicates and failures can retain their sources. Inspect the returned moved/kept lists; a partially completed move is not equivalent to a wholly completed move.

Undoing a move import does not restore originals to their old location. Preserve a manifest of source path, destination, hash and sidecars before authorizing a large move. Treat deletion authorization separately from catalog-edit authorization. For agent workflows the default recommendation is add/copy on a small subset first, then inspect and scale up.

Organizing by date, month or a folder template changes destination paths. Capture dates can be absent, causing import dates to be used. Renaming templates come from the engine's token catalog, discoverable through `photo.renameTokens`; do not infer a template language from another photo application. Use explicit duplicate/conflict policies and record the actual resulting names.

A library selection is a volatile cursor, not a durable list of business targets. Query and record IDs for the bounded operation, then inspect membership before applying a preset or exporting. Do not accidentally change every selected photo when the instruction names one.

For handoffs, `format:"original"` copies original media plus an XMP representation of edits; DNG output is another explicit path for RAW sources. Neither automatically means a different RAW processor interprets every develop feature identically. Deliver the original, sidecar/settings and a rendered reference when cross-application appearance matters.

## Evidence

- [light-mcp](https://github.com/storytold/lightcraft/blob/701f78ea2e586d4748705f10fdf5c4181dc1fd49/docs/mcp.md)
- [light-cli](https://github.com/storytold/lightcraft/blob/main/apps/lightcraft-cli/src/main.rs)
