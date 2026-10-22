---
name: storytold-wordcraft
description: "Use when writing, revising or reviewing a document with WordCraft — wordcraft-cli or its MCP server, paragraphs and styles, sections, tracked changes, export, or a WordCraft run that fails."
---

# WordCraft: AI operation

Write, revise and review structured documents with WordCraft, preserving style, tracked changes and export intent.

## Operating loop

1. Identify `wordcraft-cli` and its version/build or binary hash; choose headless versus live mode explicitly.
2. Read the relevant reference below, inspect the current command/tool catalog and acquire current IDs. Never guess a sibling app's flags or schema.
3. Use direct CLI for bounded scripted work; persistent MCP for stateful discovery/editing; UI control only for verified UI-dependent behavior.
4. Preserve originals, authorize writes and expensive/network effects, execute small steps and inspect actual results/warnings.
5. Read back affected state, inspect the output, save/reopen when needed and report the checks actually performed. Inspect uncertain state before retrying.

## Non-negotiable product distinctions

- review.trackChanges without value toggles; use value:true for reliable enabling.
- Unknown CharProps/ParaProps fields may be ignored; inspect the result.
- Headless filesystem roots cannot be applied to --connect; the reviewed desktop has no equivalent roots.
- Do not assume --help works on every subcommand; use the verified commands catalog.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| reading, revising or converting documents from shell jobs | [Document CLI commands and explicit review output](references/cli.md) |
| opening an agent session or choosing a confinement boundary | [Headless MCP, authorship and live control keys](references/mcp-roots-and-live-control.md) |
| applying formatting or changing document structure without unintended global edits | [Selection scope, style inheritance and silent property omissions](references/selection-styles-and-typography.md) |
| copyediting, commenting or producing a reviewable revision | [Reliable tracked changes and review handoffs](references/tracked-changes-and-review.md) |
| editing a long document, managing repeated outputs or integrating references | [Structured content, citations and mail-merge boundaries](references/tables-sections-fields-and-merge.md) |
| exporting documents or deciding whether a conversion preserved the required semantics | [Editable-versus-rendered delivery checks](references/format-fidelity-and-verification.md) |
| setting up an agent, running the supplied helpers, or deciding what has actually been verified | [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Local helpers

`capture_capabilities.py` records catalogs; `run_example.py` runs the authored smoke recipe. Both are in `scripts/`, plan-only until `--execute`, and are not sandboxes. Read the runtime reference first.

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
