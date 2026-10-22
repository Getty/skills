---
name: storytold-craft
description: "Use when a creative task needs a Storytold Craft application and it is unclear which one, or when work is split across several Craft editors — routing between products, comparing their CLIs and MCP servers, handing assets from one editor to another."
---

# Storytold Craft Overview: AI operation

Route AI-operated creative work to the correct Storytold product and coordinate CLI/MCP workflows without assuming a shared API.

## Operating loop

1. Establish the actual product, installed version and requested outcome; distinguish operator work from integration development.
2. Read the matching reference and verify the supported surface. Do not invent a CLI, network API or MCP service.
3. Preserve projects and authorize installations, credentials, uploads, paid generation and publication separately.
4. Carry file/state/job identifiers and warnings across handoffs. Verify the consuming application and actual delivery.
5. Record source, runtime and output evidence separately; stop rather than misreport uncertain outcomes.

## Non-negotiable product distinctions

- The twelve editors share ideas, not one CLI grammar, parameter schema or sandbox policy.
- A repository capability is not necessarily present in an installed release.
- ArtCraft, ArtCraft-X and the launcher do not have a comparable operator CLI verified here.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| choosing the correct application or splitting a cross-application workflow | [Product routing by editable object and task](references/product-routing.md) |
| building an orchestrator or translating plans into argument vectors | [CLI grammar matrix: do not normalize by guessing](references/cli-grammar-matrix.md) |
| configuring an agent client or reducing discovery overhead | [MCP mode selection and tool-name boundaries](references/mcp-modes-and-tool-names.md) |
| isolating an agent, granting file access or investigating denied operations | [Filesystem authority is product- and mode-specific](references/filesystem-and-authority-matrix.md) |
| coordinating multi-step work or handling uncertain outcomes | [Persistence, partial success and retry decisions](references/persistence-and-failure-semantics.md) |
| building a pipeline across several Craft applications | [Cross-product asset contracts](references/cross-product-handoffs.md) |
| updating the skills or deciding how strong a claim can be | [Source evidence, version drift and collection maintenance](references/source-evidence-and-updates.md) |
| testing whether the skills improve real agent behavior | [Fresh-agent evaluation and regression protocol](references/agent-evaluation.md) |
| starting an integration or evaluating an automation claim | [Integration and evidence boundaries](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
