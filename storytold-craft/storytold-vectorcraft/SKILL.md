---
name: storytold-vectorcraft
description: "Use when creating, transforming or exporting vector artwork with VectorCraft — vectorcraft-cli or its MCP server, objects, live appearance, artboards, import warnings, or a VectorCraft run that fails."
---

# VectorCraft: AI operation

Create and transform vector documents, inspect objects, control live appearance and export artboards with VectorCraft.

## Operating loop

1. Identify `vectorcraft-cli` and its version/build or binary hash; choose headless versus live mode explicitly.
2. Read the relevant reference below, inspect the current command/tool catalog and acquire current IDs. Never guess a sibling app's flags or schema.
3. Use direct CLI for bounded scripted work; persistent MCP for stateful discovery/editing; UI control only for verified UI-dependent behavior.
4. Preserve originals, authorize writes and expensive/network effects, execute small steps and inspect actual results/warnings.
5. Read back affected state, inspect the output, save/reopen when needed and report the checks actually performed. Inspect uncertain state before retrying.

## Non-negotiable product distinctions

- Bare mcp tries a live app before falling back; specify --headless for deterministic isolation.
- --artboard is zero-based; --range is one-based.
- Scoped MCP root flags imply headless and cannot be combined with --connect.
- Import warnings can indicate lost content; do not bypass --replace-lossy protections casually.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| building vector processing scripts or converting an imported illustration | [CLI grammar, artboard selection and loss-aware conversion](references/cli.md) |
| starting VectorCraft safely or investigating file-access refusals | [Explicit MCP mode selection and filesystem policy](references/mcp-modes-and-roots.md) |
| working on large documents or manipulating geometry and appearance without dumping the full model | [Targeted vector inspection and object-level edits](references/object-queries-and-editing.md) |
| preserving vector editability or exporting illustrations with external dependencies | [Appearance, text and linked assets](references/appearance-fonts-and-links.md) |
| delivering PDF/SVG/raster outputs or validating a lossy import | [Multi-artboard export and round-trip checks](references/export-verification.md) |
| setting up an agent, running the supplied helpers, or deciding what has actually been verified | [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Local helpers

`capture_capabilities.py` records catalogs; `run_example.py` runs the authored smoke recipe. Both are in `scripts/`, plan-only until `--execute`, and are not sandboxes. Read the runtime reference first.

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
