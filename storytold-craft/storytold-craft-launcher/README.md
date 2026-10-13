# Craft Launcher skill

Manage discovery, installation, version compatibility and safe update handoffs for Storytold Craft applications via the ArtCraft Launcher.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [Launcher scope and product identity](references/catalog-and-product-identity.md) — finding/installing the specialized Craft editors.
- [Platform installation paths and separate CLI assets](references/platform-paths-and-cli-discovery.md) — locating an installed editor or diagnosing command not found.
- [Update approval, checksums and quiescent handoff](references/safe-updates-and-release-evidence.md) — updating editors used by active agents.
- [Launcher diagnostics and post-install verification](references/logs-diagnostics-and-handoff.md) — investigating failed installs or handing control to an editor skill.
- [Integration and evidence boundaries](references/runtime-and-evidence.md) — starting an integration or evaluating an automation claim.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
