# Storytold Craft Overview skill

Route AI-operated creative work to the correct Storytold product and coordinate CLI/MCP workflows without assuming a shared API.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [Product routing by editable object and task](references/product-routing.md) — choosing the correct application or splitting a cross-application workflow.
- [CLI grammar matrix: do not normalize by guessing](references/cli-grammar-matrix.md) — building an orchestrator or translating plans into argument vectors.
- [MCP mode selection and tool-name boundaries](references/mcp-modes-and-tool-names.md) — configuring an agent client or reducing discovery overhead.
- [Filesystem authority is product- and mode-specific](references/filesystem-and-authority-matrix.md) — isolating an agent, granting file access or investigating denied operations.
- [Persistence, partial success and retry decisions](references/persistence-and-failure-semantics.md) — coordinating multi-step work or handling uncertain outcomes.
- [Cross-product asset contracts](references/cross-product-handoffs.md) — building a pipeline across several Craft applications.
- [Source evidence, version drift and collection maintenance](references/source-evidence-and-updates.md) — updating the skills or deciding how strong a claim can be.
- [Fresh-agent evaluation and regression protocol](references/agent-evaluation.md) — testing whether the skills improve real agent behavior.
- [Integration and evidence boundaries](references/runtime-and-evidence.md) — starting an integration or evaluating an automation claim.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
