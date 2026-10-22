---
name: storytold-soundcraft
description: "Use when editing, mixing or bouncing multitrack audio with SoundCraft — soundcraft-cli or its MCP server, sessions, source media, routing, automation, offline bounces, or a SoundCraft session that fails."
---

# SoundCraft: AI operation

Operate multitrack audio sessions, source media, mixing, routing, automation and offline bounces with SoundCraft.

## Operating loop

1. Identify `soundcraft-cli` and its version/build or binary hash; choose headless versus live mode explicitly.
2. Read the relevant reference below, inspect the current command/tool catalog and acquire current IDs. Never guess a sibling app's flags or schema.
3. Use direct CLI for bounded scripted work; persistent MCP for stateful discovery/editing; UI control only for verified UI-dependent behavior.
4. Preserve originals, authorize writes and expensive/network effects, execute small steps and inspect actual results/warnings.
5. Read back affected state, inspect the output, save/reopen when needed and report the checks actually performed. Inspect uncertain state before retrying.

## Non-negotiable product distinctions

- Headless MCP has no audio device; transport success is not evidence of audible output.
- A .scraft session depends on its Audio Files directory and media availability.
- session.audio_health is not a loudness, routing or plugin-quality audit.
- save_session requires replace:true to overwrite another existing file.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| mixing from scripts or preparing an offline bounce | [CLI edits, session persistence and audio conversion](references/cli-and-session-files.md) |
| editing a session with a persistent agent | [MCP modes, track identity and musical time](references/mcp-and-time-bases.md) |
| diagnosing missing sound or packaging a session | [Decoded media, audio-health scope and portable sessions](references/source-health-and-portability.md) |
| making audio edits whose result must be musically or technically correct | [Gain staging, inserts, sends and automation](references/mixing-routing-and-automation.md) |
| delivering audio or deciding whether a mix is actually valid | [Bounce completion, loudness metrics and final checks](references/bounce-loudness-and-verification.md) |
| setting up an agent, running the supplied helpers, or deciding what has actually been verified | [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Local helpers

`capture_capabilities.py` records catalogs; `run_example.py` runs the authored smoke recipe. Both are in `scripts/`, plan-only until `--execute`, and are not sandboxes. Read the runtime reference first.

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
