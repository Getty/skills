---
name: storytold-designcraft
description: "Use when composing or exporting page layouts with DesignCraft — designcraft-cli or its MCP server, spreads, frames, threaded stories, overset text, styles, publication export, or a DesignCraft run that fails."
---

# DesignCraft: AI operation

Compose page-layout documents with threaded stories, frames, styles, images and publication exports in DesignCraft.

## Operating loop

1. Identify `designcraft-cli` and its version/build or binary hash; choose headless versus live mode explicitly.
2. Read the relevant reference below, inspect the current command/tool catalog and acquire current IDs. Never guess a sibling app's flags or schema.
3. Use direct CLI for bounded scripted work; persistent MCP for stateful discovery/editing; UI control only for verified UI-dependent behavior.
4. Preserve originals, authorize writes and expensive/network effects, execute small steps and inspect actual results/warnings.
5. Read back affected state, inspect the output, save/reopen when needed and report the checks actually performed. Inspect uncertain state before retrying.

## Non-negotiable product distinctions

- Story offsets are UTF-8 bytes, not Unicode character indexes.
- Geometry is spread-space points, y down; rendered page indexes are zero-based.
- --page, --scale and --pdf-options apply to the exports that follow them.
- Rendered text is not proof that every story fits; inspect overset.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| constructing a page-layout batch or exporting several variants | [CLI scripts and order-dependent export options](references/cli-and-export-order.md) |
| placing frames or editing text through a stateful agent | [MCP identity, spread geometry and UTF-8 byte offsets](references/mcp-coordinates-and-utf8.md) |
| flowing long text through pages or changing typography | [Threaded stories, styles and overset detection](references/stories-frames-styles-and-overset.md) |
| placing images or producing print and digital variants | [Linked assets, color and publishing handoffs](references/images-color-and-publishing.md) |
| turning a brief into an editable layout and verified delivery | [A layout production loop with explicit checks](references/production-and-verification.md) |
| setting up an agent, running the supplied helpers, or deciding what has actually been verified | [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Local helpers

`capture_capabilities.py` records catalogs; `run_example.py` runs the authored smoke recipe. Both are in `scripts/`, plan-only until `--execute`, and are not sandboxes. Read the runtime reference first.

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
