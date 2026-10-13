# GridCraft skill

Inspect and edit spreadsheets, evaluate formulas, validate calculation oracles and measure workbook round-trip fidelity using GridCraft.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [CLI workbook operations and command-script grammar](references/cli.md) — inspecting spreadsheets, running edits or evaluating a formula without a GUI.
- [MCP helpers, bounded ranges and formula-valued strings](references/mcp-and-data-types.md) — reading/writing cells or building an agent-facing workbook adapter.
- [Formula validation and independent cached-value oracles](references/formulas-and-calculation-oracles.md) — checking calculation correctness or interpreting gridcraft-cli check results.
- [Format directionality and workbook round-trip losses](references/format-import-and-roundtrip.md) — opening XLS/XLSB/ODS files or exporting a workbook for another application.
- [Safe table edits, formatting and workbook acceptance](references/workbook-editing-and-verification.md) — performing real spreadsheet changes rather than isolated formula tests.
- [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) — setting up an agent, running the supplied helpers, or deciding what has actually been verified.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
