---
name: storytold-effectcraft
description: "Use this skill when the user requests EffectCraft operations, CLI/MCP automation, output verification or troubleshooting. Build motion graphics, animate composition/layer properties, manage expressions and render jobs with EffectCraft."
---

# EffectCraft: AI operation

Build motion graphics, animate composition/layer properties, manage expressions and render jobs with EffectCraft.

## Operating loop

1. Identify `effectcraft-cli` and its version/build or binary hash; choose headless versus live mode explicitly.
2. Read the relevant reference below, inspect the current command/tool catalog and acquire current IDs. Never guess a sibling app's flags or schema.
3. Use direct CLI for bounded scripted work; persistent MCP for stateful discovery/editing; UI control only for verified UI-dependent behavior.
4. Preserve originals, authorize writes and expensive/network effects, execute small steps and inspect actual results/warnings.
5. Read back affected state, inspect the output, save/reopen when needed and report the checks actually performed. Inspect uncertain state before retrying.

## Non-negotiable product distinctions

- Keyframe writes default to layer time; explicit comp time must be requested.
- batch and command_batch have different rollback and undo semantics.
- A render owns a snapshot; edits made during rendering do not change that render.
- Scoped mode restricts scripts and UI driving as well as filesystem paths.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| constructing EffectCraft commands or producing a headless composition | [CLI execution, property access and rendering](references/cli.md) |
| registering an EffectCraft agent or dealing with a denied operation | [MCP schemas, scoped access and bridge limitations](references/mcp-schema-and-confinement.md) |
| animating offset, stretched or reversed layers | [Layer identities, property paths and time bases](references/layers-properties-and-time.md) |
| grouping dependent edits or considering JavaScript/expression automation | [Atomic batches versus sequential batches](references/batches-scripts-and-expressions.md) |
| rendering a composition or validating GPU/CPU output | [Render snapshots, cancellation and alpha delivery](references/render-queues-gpu-and-alpha.md) |
| keeping agent work across MCP restarts or responding to a checkpoint warning | [Headless autosave, explicit saves and recovery](references/autosave-and-recovery.md) |
| setting up an agent, running the supplied helpers, or deciding what has actually been verified | [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Local helpers

`capture_capabilities.py` records catalogs; `run_example.py` runs the authored smoke recipe. Both are in `scripts/`, plan-only until `--execute`, and are not sandboxes. Read the runtime reference first.

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
