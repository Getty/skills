---
name: storytold-pdfcraft
description: "Use this skill when the user requests PdfCraft operations, CLI/MCP automation, output verification or troubleshooting. Read, inspect, organize, annotate, edit, secure and verify PDFs through PdfCraft's CLI and schema-described automation tools."
---

# PdfCraft: AI operation

Read, inspect, organize, annotate, edit, secure and verify PDFs through PdfCraft's CLI and schema-described automation tools.

## Operating loop

1. Identify `pdfcraft-cli` and its version/build or binary hash; choose headless versus live mode explicitly.
2. Read the relevant reference below, inspect the current command/tool catalog and acquire current IDs. Never guess a sibling app's flags or schema.
3. Use direct CLI for bounded scripted work; persistent MCP for stateful discovery/editing; UI control only for verified UI-dependent behavior.
4. Preserve originals, authorize writes and expensive/network effects, execute small steps and inspect actual results/warnings.
5. Read back affected state, inspect the output, save/reopen when needed and report the checks actually performed. Inspect uncertain state before retrying.

## Non-negotiable product distinctions

- Pages and positions are one-based; geometry uses displayed-page top-left PDF points.
- Document IDs belong to a live session; use one run script or persistent MCP for multistep edits.
- Strict task-tool schemas differ from command_run, which can warn and ignore unknown nested keys.
- Incremental saves retain previous bytes; overlays and successful renders do not establish secure redaction.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| extracting PDF information, scripting a multistep edit, or discovering exact schemas | [CLI commands and session-scoped tool scripts](references/cli-and-tool-scripts.md) |
| starting PdfCraft automation or interpreting a validation refusal | [MCP schemas, compact discovery and filesystem authority](references/mcp-and-root-policy.md) |
| rotating/reordering pages, placing annotations or editing existing text and artwork | [Page indexes, displayed geometry and existing-text edits](references/pages-geometry-and-text.md) |
| filling forms, editing field properties or preserving review intent | [Forms, review annotations and signature-sensitive workflows](references/forms-comments-and-signatures.md) |
| removing confidential information or preparing a security/accessibility-sensitive deliverable | [Redaction, sanitization and accessibility evidence](references/redaction-sanitization-accessibility.md) |
| committing edits or testing a heterogeneous PDF corpus | [Save semantics and PDF acceptance gates](references/save-reopen-and-robustness.md) |
| setting up an agent, running the supplied helpers, or deciding what has actually been verified | [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Local helpers

`capture_capabilities.py` records catalogs; `run_example.py` runs the authored smoke recipe. Both are in `scripts/`, plan-only until `--execute`, and are not sandboxes. Read the runtime reference first.

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
