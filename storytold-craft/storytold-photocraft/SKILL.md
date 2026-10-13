---
name: storytold-photocraft
description: "Use this skill when the user requests PhotoCraft operations, CLI/MCP automation, output verification or troubleshooting. Edit layered raster images, PSD/PSB documents, masks, adjustments, smart objects and exports through PhotoCraft."
---

# PhotoCraft: AI operation

Edit layered raster images, PSD/PSB documents, masks, adjustments, smart objects and exports through PhotoCraft.

## Operating loop

1. Identify `photocraft-cli` and its version/build or binary hash; choose headless versus live mode explicitly.
2. Read the relevant reference below, inspect the current command/tool catalog and acquire current IDs. Never guess a sibling app's flags or schema.
3. Use direct CLI for bounded scripted work; persistent MCP for stateful discovery/editing; UI control only for verified UI-dependent behavior.
4. Preserve originals, authorize writes and expensive/network effects, execute small steps and inspect actual results/warnings.
5. Read back affected state, inspect the output, save/reopen when needed and report the checks actually performed. Inspect uncertain state before retrying.

## Non-negotiable product distinctions

- CLI --cmd takes a separate --params; do not import another app's id=JSON grammar.
- Direct CLI paths are ambient; scoped MCP/serve use separately granted read and write authority.
- An MCP batch is not atomic; response-budget errors may occur after an edit.
- Save smart-object contents inward-to-outward before saving the parent document.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| choosing a PhotoCraft subcommand, constructing argument vectors, or deciding whether state survives | [CLI grammar and persistent headless sessions](references/cli.md) |
| starting an agent server, attaching to a live editor, or diagnosing an authorization failure | [MCP, control authentication and file authority](references/mcp-and-control.md) |
| editing structure, targeting layers, or saving nested smart-object contents | [Document identity, masks and smart-object ownership](references/layers-masks-smart-objects.md) |
| matching an appearance, exporting editable files, or baking a color look | [Color, typography, LUTs and format fidelity](references/color-type-and-fidelity.md) |
| running action chains, exporting a timeline, or handling a failed or cancelled call | [Partial batches, video jobs and recovery](references/jobs-batches-and-recovery.md) |
| setting up an agent, running the supplied helpers, or deciding what has actually been verified | [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Local helpers

`capture_capabilities.py` records catalogs; `run_example.py` runs the authored smoke recipe. Both are in `scripts/`, plan-only until `--execute`, and are not sandboxes. Read the runtime reference first.

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
