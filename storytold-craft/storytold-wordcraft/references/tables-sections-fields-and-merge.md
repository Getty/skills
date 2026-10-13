# Structured content, citations and mail-merge boundaries

**Read when:** editing a long document, managing repeated outputs or integrating references.

Use document structure to distinguish body text, headers/footers, tables, sections, fields and review annotations. A flattened text dump cannot fully represent those relationships. Before a bulk replacement, determine which structures are in scope and which must remain unchanged.

Table insertion and style operations should use discovered row/column/style parameters rather than tab-delimited text that merely looks aligned. Reinspect table structure and render page breaks after changing widths, fonts or content. Section/page geometry changes can affect headers, footers, numbering and pagination beyond the immediate selection; check representative boundary pages.

Citation fields, bibliography data and ordinary text are different representations. The local Zotero integration requires a running application and has its own commands and possible prompts. Preserve fields when the task requires refreshable references; do not replace them with visually equivalent plain text without accepting that loss.

Mail-merge input paths are covered by the configured read-root policy. Output paths are covered by write authority. Treat a merge as a multiplication of outputs: verify recipient count, unique names, collision behavior, data mapping and a small sample before creating the whole set. Never accidentally expose one recipient's data in another recipient's document.

Do not assume a familiar feature label means the same field-update, pagination or merge behavior as Microsoft Word. Use installed command descriptions, run a bounded sample and reopen the actual delivery. This reference sets verification requirements; exact feature-specific parameters must come from the live catalog rather than invented syntax.

## Evidence

- [word-cli](https://github.com/storytold/wordcraft/blob/main/apps/wordcraft-cli/src/main.rs)
- [word-mcp](https://github.com/storytold/wordcraft/blob/main/docs/mcp.md)
- [wordcraft-readme](https://github.com/storytold/wordcraft/blob/main/README.md)
