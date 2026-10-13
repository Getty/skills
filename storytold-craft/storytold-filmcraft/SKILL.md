---
name: storytold-filmcraft
description: "Use this skill when the user requests FilmCraft operations, CLI/MCP automation, output verification or troubleshooting. Inspect, edit and render video projects and timelines with FilmCraft, including media health, timing and export jobs."
---

# FilmCraft: AI operation

Inspect, edit and render video projects and timelines with FilmCraft, including media health, timing and export jobs.

## Operating loop

1. Identify `filmcraft-cli` and its version/build or binary hash; choose headless versus live mode explicitly.
2. Read the relevant reference below, inspect the current command/tool catalog and acquire current IDs. Never guess a sibling app's flags or schema.
3. Use direct CLI for bounded scripted work; persistent MCP for stateful discovery/editing; UI control only for verified UI-dependent behavior.
4. Preserve originals, authorize writes and expensive/network effects, execute small steps and inspect actual results/warnings.
5. Read back affected state, inspect the output, save/reopen when needed and report the checks actually performed. Inspect uncertain state before retrying.

## Non-negotiable product distinctions

- Time uses 254016000000 ticks per second; never confuse ticks, frames and seconds.
- Headless MCP has ambient filesystem access; PhotoCraft root flags are not accepted.
- Engine/MCP export can succeed while drawing offline-media placeholders; inspect offlineMedia.
- Breaking a stdout pipe does not cancel execution or a pending save.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| driving FilmCraft from subprocesses or constructing a reproducible timeline job | [CLI sessions, scripts and saves](references/cli.md) |
| configuring an agent session, discovering tools, or distinguishing protocol failures from command failures | [MCP, desktop bridging and error layers](references/mcp-and-control.md) |
| placing, trimming, retiming or moving clips precisely | [Ticks, frame grids, source ranges and linked tracks](references/timeline-time-and-targeting.md) |
| importing media, relinking a project, or transferring an edit between applications | [Media identity, offline assets and project interchange](references/media-and-interchange.md) |
| rendering a sequence or recovering from an uncertain export outcome | [Exports, progress, cancellation and delivery gates](references/render-jobs-and-delivery.md) |
| setting up an agent, running the supplied helpers, or deciding what has actually been verified | [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Local helpers

`capture_capabilities.py` records catalogs; `run_example.py` runs the authored smoke recipe. Both are in `scripts/`, plan-only until `--execute`, and are not sandboxes. Read the runtime reference first.

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
