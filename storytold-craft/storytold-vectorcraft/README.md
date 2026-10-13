# VectorCraft skill

Create and transform vector documents, inspect objects, control live appearance and export artboards with VectorCraft.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [CLI grammar, artboard selection and loss-aware conversion](references/cli.md) — building vector processing scripts or converting an imported illustration.
- [Explicit MCP mode selection and filesystem policy](references/mcp-modes-and-roots.md) — starting VectorCraft safely or investigating file-access refusals.
- [Targeted vector inspection and object-level edits](references/object-queries-and-editing.md) — working on large documents or manipulating geometry and appearance without dumping the full model.
- [Appearance, text and linked assets](references/appearance-fonts-and-links.md) — preserving vector editability or exporting illustrations with external dependencies.
- [Multi-artboard export and round-trip checks](references/export-verification.md) — delivering PDF/SVG/raster outputs or validating a lossy import.
- [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) — setting up an agent, running the supplied helpers, or deciding what has actually been verified.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
