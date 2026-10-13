# WordCraft skill

Write, revise and review structured documents with WordCraft, preserving style, tracked changes and export intent.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [Document CLI commands and explicit review output](references/cli.md) — reading, revising or converting documents from shell jobs.
- [Headless MCP, authorship and live control keys](references/mcp-roots-and-live-control.md) — opening an agent session or choosing a confinement boundary.
- [Selection scope, style inheritance and silent property omissions](references/selection-styles-and-typography.md) — applying formatting or changing document structure without unintended global edits.
- [Reliable tracked changes and review handoffs](references/tracked-changes-and-review.md) — copyediting, commenting or producing a reviewable revision.
- [Structured content, citations and mail-merge boundaries](references/tables-sections-fields-and-merge.md) — editing a long document, managing repeated outputs or integrating references.
- [Editable-versus-rendered delivery checks](references/format-fidelity-and-verification.md) — exporting documents or deciding whether a conversion preserved the required semantics.
- [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) — setting up an agent, running the supplied helpers, or deciding what has actually been verified.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
