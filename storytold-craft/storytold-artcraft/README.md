# ArtCraft skill

Inspect and integrate Storytold ArtCraft's generative desktop workflow and Rust client without inventing a Craft-style operator CLI.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [ArtCraft is not another Craft CLI](references/product-and-automation-boundary.md) — routing a generation task or deciding whether a proposed automation surface is real.
- [How to derive an integration from the real client code](references/source-guided-integration.md) — building a narrowly scoped adapter rather than guessing backend requests.
- [Generation job records, costs and retry safety](references/generation-jobs-and-approval.md) — planning or integrating remote generation through ArtCraft.
- [Handoff from generation to specialized editors](references/creative-handoffs-and-verification.md) — moving generated assets into an editable Craft workflow.
- [Integration and evidence boundaries](references/runtime-and-evidence.md) — starting an integration or evaluating an automation claim.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
