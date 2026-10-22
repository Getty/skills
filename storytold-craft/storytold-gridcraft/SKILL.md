---
name: storytold-gridcraft
description: "Use when editing a spreadsheet or validating its calculation with GridCraft — gridcraft-cli or its MCP server, cells, formulas, calculation oracles, XLSX, XLSB or ODS round-trips, or a GridCraft run that fails."
---

# GridCraft: AI operation

Inspect and edit spreadsheets, evaluate formulas, validate calculation oracles and measure workbook round-trip fidelity using GridCraft.

## Operating loop

1. Identify `gridcraft-cli` and its version/build or binary hash; choose headless versus live mode explicitly.
2. Read the relevant reference below, inspect the current command/tool catalog and acquire current IDs. Never guess a sibling app's flags or schema.
3. Use direct CLI for bounded scripted work; persistent MCP for stateful discovery/editing; UI control only for verified UI-dependent behavior.
4. Preserve originals, authorize writes and expensive/network effects, execute small steps and inspect actual results/warnings.
5. Read back affected state, inspect the output, save/reopen when needed and report the checks actually performed. Inspect uncertain state before retrying.

## Non-negotiable product distinctions

- XLSB and ODS import may turn formulas into cached values and omit formatting.
- check exit zero is not comprehensive formula coverage: inspect noOracle, volatile and checked counts.
- Preserve formulas separately from displayed values and data types.
- CLI run stops on the first failing step; do not assume transaction rollback.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| inspecting spreadsheets, running edits or evaluating a formula without a GUI | [CLI workbook operations and command-script grammar](references/cli.md) |
| reading/writing cells or building an agent-facing workbook adapter | [MCP helpers, bounded ranges and formula-valued strings](references/mcp-and-data-types.md) |
| checking calculation correctness or interpreting gridcraft-cli check results | [Formula validation and independent cached-value oracles](references/formulas-and-calculation-oracles.md) |
| opening XLS/XLSB/ODS files or exporting a workbook for another application | [Format directionality and workbook round-trip losses](references/format-import-and-roundtrip.md) |
| performing real spreadsheet changes rather than isolated formula tests | [Safe table edits, formatting and workbook acceptance](references/workbook-editing-and-verification.md) |
| setting up an agent, running the supplied helpers, or deciding what has actually been verified | [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Local helpers

`capture_capabilities.py` records catalogs; `run_example.py` runs the authored smoke recipe. Both are in `scripts/`, plan-only until `--execute`, and are not sandboxes. Read the runtime reference first.

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
