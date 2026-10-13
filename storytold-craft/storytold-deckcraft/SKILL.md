---
name: storytold-deckcraft
description: "Use this skill when the user requests DeckCraft operations, CLI/MCP automation, output verification or troubleshooting. Build, inspect and export presentations with DeckCraft while preserving editable shapes, slide structure and presentation intent."
---

# DeckCraft: AI operation

Build, inspect and export presentations with DeckCraft while preserving editable shapes, slide structure and presentation intent.

## Operating loop

1. Identify `deckcraft-cli` and its version/build or binary hash; choose headless versus live mode explicitly.
2. Read the relevant reference below, inspect the current command/tool catalog and acquire current IDs. Never guess a sibling app's flags or schema.
3. Use direct CLI for bounded scripted work; persistent MCP for stateful discovery/editing; UI control only for verified UI-dependent behavior.
4. Preserve originals, authorize writes and expensive/network effects, execute small steps and inspect actual results/warnings.
5. Read back affected state, inspect the output, save/reopen when needed and report the checks actually performed. Inspect uncertain state before retrying.

## Non-negotiable product distinctions

- A PNG conversion can cover only the first slide; use render --all for coverage.
- A static render does not verify animation, transitions or embedded media playback.
- Use --save for the editable working document and explicit exports for deliveries.
- Do not assume generic --help flags or schema parity with another Craft app.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| creating an editable presentation or rendering all slides | [CLI deck construction and zero-based slide rendering](references/cli-and-slide-indexes.md) |
| building slides semantically or mapping pointer operations | [MCP tools, slide points and live UI control](references/mcp-and-coordinate-spaces.md) |
| turning an outline into a structured presentation | [Editable shapes, layouts and text hierarchy](references/slide-structure-and-text.md) |
| using media/transitions or exporting PowerPoint/PDF deliverables | [Static versus live presentation behavior](references/media-animation-and-interchange.md) |
| finishing a deck or recovering after a partial sequence of edits | [Presentation verification and safe recovery](references/verification-and-recovery.md) |
| setting up an agent, running the supplied helpers, or deciding what has actually been verified | [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Local helpers

`capture_capabilities.py` records catalogs; `run_example.py` runs the authored smoke recipe. Both are in `scripts/`, plan-only until `--execute`, and are not sandboxes. Read the runtime reference first.

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
