---
name: storytold-lightcraft
description: "Use when importing, developing or exporting photos with LightCraft — lightcraft-cli or its MCP server, the photo catalog, RAW development, originals and sidecars, or a LightCraft run that fails."
---

# LightCraft: AI operation

Operate a persistent photo catalog, develop RAW files, manage originals/sidecars, and export images with LightCraft.

## Operating loop

1. Identify `lightcraft-cli` and its version/build or binary hash; choose headless versus live mode explicitly.
2. Read the relevant reference below, inspect the current command/tool catalog and acquire current IDs. Never guess a sibling app's flags or schema.
3. Use direct CLI for bounded scripted work; persistent MCP for stateful discovery/editing; UI control only for verified UI-dependent behavior.
4. Preserve originals, authorize writes and expensive/network effects, execute small steps and inspect actual results/warnings.
5. Read back affected state, inspect the output, save/reopen when needed and report the checks actually performed. Inspect uncertain state before retrying.

## Non-negotiable product distinctions

- A library has one owning process; use connect mode rather than opening it twice.
- CLI render defaults to full size, while the MCP export helper defaults to a 3000-pixel long edge.
- Move import changes original files; undo does not put them back.
- White-balance scale and develop process version are part of the image specification.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| building shell workflows or selecting between catalog operations, rendering, merge and model services | [CLI operations and their output defaults](references/cli.md) |
| opening a persistent library, connecting to the desktop, or resuming after a restart | [MCP modes and exclusive library ownership](references/mcp-and-library-lifecycle.md) |
| changing exposure, color, crops or presets without silently changing the rendering interpretation | [RAW development, process versions and white balance](references/develop-controls-and-color.md) |
| importing a shoot, moving originals, creating albums or handing off RAW edits | [Import modes, metadata and source-file preservation](references/catalog-import-and-sidecars.md) |
| processing HDR/panoramas, using a GPU service, or fitting camera profiles | [Merge, remote denoise and calibration boundaries](references/merge-denoise-and-calibration.md) |
| delivering full-size, privacy-sensitive or cross-application photo outputs | [Export policy and acceptance checks](references/export-and-verification.md) |
| setting up an agent, running the supplied helpers, or deciding what has actually been verified | [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Local helpers

`capture_capabilities.py` records catalogs; `run_example.py` runs the authored smoke recipe. Both are in `scripts/`, plan-only until `--execute`, and are not sandboxes. Read the runtime reference first.

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
