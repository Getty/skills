---
name: storytold-cadcraft
description: "Use this skill when the user requests CADCraft operations, CLI/MCP automation, output verification or troubleshooting. Create and verify drawings with CADCraft using geometry commands, structured inspection, layouts and DXF/DWG interchange."
---

# CADCraft: AI operation

Create and verify drawings with CADCraft using geometry commands, structured inspection, layouts and DXF/DWG interchange.

## Operating loop

1. Identify `cadcraft-cli` and its version/build or binary hash; choose headless versus live mode explicitly.
2. Read the relevant reference below, inspect the current command/tool catalog and acquire current IDs. Never guess a sibling app's flags or schema.
3. Use direct CLI for bounded scripted work; persistent MCP for stateful discovery/editing; UI control only for verified UI-dependent behavior.
4. Preserve originals, authorize writes and expensive/network effects, execute small steps and inspect actual results/warnings.
5. Read back affected state, inspect the output, save/reopen when needed and report the checks actually performed. Inspect uncertain state before retrying.

## Non-negotiable product distinctions

- Unsupported imported entity types are not necessarily retained on save.
- Model-space units, paper-space points and viewport scale are distinct.
- Command-prompt workflows are stateful; inspect pending prompts before sending another command.
- SVG/PNG visual similarity does not establish dimensional or CAD round-trip correctness.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| creating drawings or deciding between textual command input and structured commands | [CLI execution and stateful CAD prompts](references/cli-and-command-prompts.md) |
| operating CADCraft through an agent or a live desktop | [MCP sessions and drawing inspection](references/mcp-and-inspection.md) |
| creating dimensionally meaningful drawings rather than visual approximations | [Geometry precision, units and constraint-aware edits](references/geometry-units-and-constraints.md) |
| exporting drawings, dimensions or layout sheets | [Model-space previews versus paper-space publication](references/layouts-fonts-and-plotting.md) |
| opening external CAD files or saving a supposedly compatible drawing | [DXF/DWG round-trip risk and delivery checks](references/file-loss-and-verification.md) |
| setting up an agent, running the supplied helpers, or deciding what has actually been verified | [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Local helpers

`capture_capabilities.py` records catalogs; `run_example.py` runs the authored smoke recipe. Both are in `scripts/`, plan-only until `--execute`, and are not sandboxes. Read the runtime reference first.

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
