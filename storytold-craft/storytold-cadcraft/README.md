# CADCraft skill

Create and verify drawings with CADCraft using geometry commands, structured inspection, layouts and DXF/DWG interchange.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [CLI execution and stateful CAD prompts](references/cli-and-command-prompts.md) — creating drawings or deciding between textual command input and structured commands.
- [MCP sessions and drawing inspection](references/mcp-and-inspection.md) — operating CADCraft through an agent or a live desktop.
- [Geometry precision, units and constraint-aware edits](references/geometry-units-and-constraints.md) — creating dimensionally meaningful drawings rather than visual approximations.
- [Model-space previews versus paper-space publication](references/layouts-fonts-and-plotting.md) — exporting drawings, dimensions or layout sheets.
- [DXF/DWG round-trip risk and delivery checks](references/file-loss-and-verification.md) — opening external CAD files or saving a supposedly compatible drawing.
- [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) — setting up an agent, running the supplied helpers, or deciding what has actually been verified.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
