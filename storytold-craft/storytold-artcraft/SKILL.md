---
name: storytold-artcraft
description: "Use this skill for ArtCraft routing, integration boundaries and operational planning. Inspect and integrate Storytold ArtCraft's generative desktop workflow and Rust client without inventing a Craft-style operator CLI."
---

# ArtCraft: AI operation

Inspect and integrate Storytold ArtCraft's generative desktop workflow and Rust client without inventing a Craft-style operator CLI.

## Operating loop

1. Establish the actual product, installed version and requested outcome; distinguish operator work from integration development.
2. Read the matching reference and verify the supported surface. Do not invent a CLI, network API or MCP service.
3. Preserve projects and authorize installations, credentials, uploads, paid generation and publication separately.
4. Carry file/state/job identifiers and warnings across handoffs. Verify the consuming application and actual delivery.
5. Record source, runtime and output evidence separately; stop rather than misreport uncertain outcomes.

## Non-negotiable product distinctions

- No comparable artcraft-cli operator surface was verified in the reviewed sources.
- A Rust HTTP endpoint binding is not a supported public automation API contract by itself.
- Generation can upload user content and incur provider costs; authorize those effects explicitly.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| routing a generation task or deciding whether a proposed automation surface is real | [ArtCraft is not another Craft CLI](references/product-and-automation-boundary.md) |
| building a narrowly scoped adapter rather than guessing backend requests | [How to derive an integration from the real client code](references/source-guided-integration.md) |
| planning or integrating remote generation through ArtCraft | [Generation job records, costs and retry safety](references/generation-jobs-and-approval.md) |
| moving generated assets into an editable Craft workflow | [Handoff from generation to specialized editors](references/creative-handoffs-and-verification.md) |
| starting an integration or evaluating an automation claim | [Integration and evidence boundaries](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
