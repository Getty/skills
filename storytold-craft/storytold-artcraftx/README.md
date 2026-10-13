# ArtCraft-X skill

Understand and integrate the experimental ArtCraft-X Tauri generation application, its IPC boundary and development lifecycle.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [ArtCraft-X automation evidence and Tauri IPC](references/product-and-ipc-boundary.md) — routing tasks to the experimental application or inspecting integration options.
- [Development startup is not production automation](references/development-lifecycle.md) — starting a local development copy or diagnosing reload behavior.
- [Credential and file boundaries in a generative desktop adapter](references/credentials-jobs-and-files.md) — designing a narrowly scoped automation path.
- [Verification scope and migration boundaries](references/verification-and-migration.md) — comparing ArtCraft-X with ArtCraft or validating an experimental integration.
- [Integration and evidence boundaries](references/runtime-and-evidence.md) — starting an integration or evaluating an automation claim.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
