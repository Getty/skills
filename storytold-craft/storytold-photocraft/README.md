# PhotoCraft skill

Edit layered raster images, PSD/PSB documents, masks, adjustments, smart objects and exports through PhotoCraft.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [CLI grammar and persistent headless sessions](references/cli.md) — choosing a PhotoCraft subcommand, constructing argument vectors, or deciding whether state survives.
- [MCP, control authentication and file authority](references/mcp-and-control.md) — starting an agent server, attaching to a live editor, or diagnosing an authorization failure.
- [Document identity, masks and smart-object ownership](references/layers-masks-smart-objects.md) — editing structure, targeting layers, or saving nested smart-object contents.
- [Color, typography, LUTs and format fidelity](references/color-type-and-fidelity.md) — matching an appearance, exporting editable files, or baking a color look.
- [Partial batches, video jobs and recovery](references/jobs-batches-and-recovery.md) — running action chains, exporting a timeline, or handling a failed or cancelled call.
- [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) — setting up an agent, running the supplied helpers, or deciding what has actually been verified.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
