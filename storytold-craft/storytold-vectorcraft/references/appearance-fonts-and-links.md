# Appearance, text and linked assets

**Read when:** preserving vector editability or exporting illustrations with external dependencies.

Record whether text must remain editable, whether effects must stay live, and whether linked raster assets must be embedded or delivered alongside the document. These requirements determine the output format and allowable operations; a visually correct flattened export may fail the task.

Inspect fonts and import warnings through `info` and the live document. A missing family can change line breaks, glyph widths and object bounds. Outlining text is an explicit fallback with costs, not a substitute for quietly missing fonts. Do not distribute font binaries from the execution environment.

Linked SVG images, relink/update operations, style libraries, profiles and font-search folders participate in the filesystem policy. A missing link under confinement may be an authorization refusal rather than an absent file. Inspect the actual cause before changing roots or rewriting paths. Do not replace a missing production asset with a preview just to obtain a successful render.

Live appearance and hidden layers can survive in some exports through format-specific representation; that does not establish identical support in every consumer. Keep an editable native master and a rendered reference. When using raster tracing, check both topology and visual output: a close-looking trace can contain excessive nodes, disconnected paths or holes that break downstream CAD/cutting workflows. Resolve trace/effect commands from the actual registry rather than importing parameters from Illustrator or another Craft app.

An asset handoff should name source files, profile/font requirements, artboard selection, preserved semantics, intentional flattening/outlining, and any omitted constructs. This is an operator acceptance policy derived from the import/export risks, not an assertion of format parity.

## Evidence

- [vector-cli](https://github.com/storytold/vectorcraft/blob/main/apps/vectorcraft-cli/src/main.rs)
- [vector-mcp](https://github.com/storytold/vectorcraft/blob/main/docs/mcp.md)
- [vectorcraft-readme](https://github.com/storytold/vectorcraft/blob/main/README.md)
