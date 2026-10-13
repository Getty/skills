---
name: storytold-artcraftx
description: "Use this skill for ArtCraft-X routing, integration boundaries and operational planning. Understand and integrate the experimental ArtCraft-X Tauri generation application, its IPC boundary and development lifecycle."
---

# ArtCraft-X: AI operation

Understand and integrate the experimental ArtCraft-X Tauri generation application, its IPC boundary and development lifecycle.

## Operating loop

1. Establish the actual product, installed version and requested outcome; distinguish operator work from integration development.
2. Read the matching reference and verify the supported surface. Do not invent a CLI, network API or MCP service.
3. Preserve projects and authorize installations, credentials, uploads, paid generation and publication separately.
4. Carry file/state/job identifiers and warnings across handoffs. Verify the consuming application and actual delivery.
5. Record source, runtime and output evidence separately; stop rather than misreport uncertain outcomes.

## Non-negotiable product distinctions

- The Vite development port is not a generation REST API.
- A registered Tauri invoke handler is not an externally reachable MCP or CLI endpoint.
- Development startup and hot reload must not be mistaken for durable production job management.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| routing tasks to the experimental application or inspecting integration options | [ArtCraft-X automation evidence and Tauri IPC](references/product-and-ipc-boundary.md) |
| starting a local development copy or diagnosing reload behavior | [Development startup is not production automation](references/development-lifecycle.md) |
| designing a narrowly scoped automation path | [Credential and file boundaries in a generative desktop adapter](references/credentials-jobs-and-files.md) |
| comparing ArtCraft-X with ArtCraft or validating an experimental integration | [Verification scope and migration boundaries](references/verification-and-migration.md) |
| starting an integration or evaluating an automation claim | [Integration and evidence boundaries](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
