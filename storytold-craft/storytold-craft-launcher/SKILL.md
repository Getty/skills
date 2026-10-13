---
name: storytold-craft-launcher
description: "Use this skill for Craft Launcher routing, integration boundaries and operational planning. Manage discovery, installation, version compatibility and safe update handoffs for Storytold Craft applications via the ArtCraft Launcher."
---

# Craft Launcher: AI operation

Manage discovery, installation, version compatibility and safe update handoffs for Storytold Craft applications via the ArtCraft Launcher.

## Operating loop

1. Establish the actual product, installed version and requested outcome; distinguish operator work from integration development.
2. Read the matching reference and verify the supported surface. Do not invent a CLI, network API or MCP service.
3. Preserve projects and authorize installations, credentials, uploads, paid generation and publication separately.
4. Carry file/state/job identifiers and warnings across handoffs. Verify the consuming application and actual delivery.
5. Record source, runtime and output evidence separately; stop rather than misreport uncertain outcomes.

## Non-negotiable product distinctions

- The product executable is artcraft-launcher; a craft-launcher-cli management API was not verified.
- Installing a GUI does not prove that a compatible CLI is on PATH, especially on macOS.
- Package formats, elevation and sandbox paths differ across platforms.

## Load references selectively

Do not load this folder wholesale. Read the matching topic and consult source/runtime evidence when version-sensitive details matter.

| Read when | Reference |
|---|---|
| finding/installing the specialized Craft editors | [Launcher scope and product identity](references/catalog-and-product-identity.md) |
| locating an installed editor or diagnosing command not found | [Platform installation paths and separate CLI assets](references/platform-paths-and-cli-discovery.md) |
| updating editors used by active agents | [Update approval, checksums and quiescent handoff](references/safe-updates-and-release-evidence.md) |
| investigating failed installs or handing control to an editor skill | [Launcher diagnostics and post-install verification](references/logs-diagnostics-and-handoff.md) |
| starting an integration or evaluating an automation claim | [Integration and evidence boundaries](references/runtime-and-evidence.md) |
| verifying claims, exact source identities or version drift | [Sources and review boundaries](references/sources.md) |

## Evidence and independence

Source review: 2026-10-12; not a claim of full feature parity or live acceptance. This folder is self-contained. Its evaluation cases are not-run test plans, not passed LLM benchmarks. See [VALIDATION.md](VALIDATION.md).
