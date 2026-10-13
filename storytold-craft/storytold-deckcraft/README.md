# DeckCraft skill

Build, inspect and export presentations with DeckCraft while preserving editable shapes, slide structure and presentation intent.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [CLI deck construction and zero-based slide rendering](references/cli-and-slide-indexes.md) — creating an editable presentation or rendering all slides.
- [MCP tools, slide points and live UI control](references/mcp-and-coordinate-spaces.md) — building slides semantically or mapping pointer operations.
- [Editable shapes, layouts and text hierarchy](references/slide-structure-and-text.md) — turning an outline into a structured presentation.
- [Static versus live presentation behavior](references/media-animation-and-interchange.md) — using media/transitions or exporting PowerPoint/PDF deliverables.
- [Presentation verification and safe recovery](references/verification-and-recovery.md) — finishing a deck or recovering after a partial sequence of edits.
- [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) — setting up an agent, running the supplied helpers, or deciding what has actually been verified.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
