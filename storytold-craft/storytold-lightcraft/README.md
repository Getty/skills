# LightCraft skill

Operate a persistent photo catalog, develop RAW files, manage originals/sidecars, and export images with LightCraft.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [CLI operations and their output defaults](references/cli.md) — building shell workflows or selecting between catalog operations, rendering, merge and model services.
- [MCP modes and exclusive library ownership](references/mcp-and-library-lifecycle.md) — opening a persistent library, connecting to the desktop, or resuming after a restart.
- [RAW development, process versions and white balance](references/develop-controls-and-color.md) — changing exposure, color, crops or presets without silently changing the rendering interpretation.
- [Import modes, metadata and source-file preservation](references/catalog-import-and-sidecars.md) — importing a shoot, moving originals, creating albums or handing off RAW edits.
- [Merge, remote denoise and calibration boundaries](references/merge-denoise-and-calibration.md) — processing HDR/panoramas, using a GPU service, or fitting camera profiles.
- [Export policy and acceptance checks](references/export-and-verification.md) — delivering full-size, privacy-sensitive or cross-application photo outputs.
- [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) — setting up an agent, running the supplied helpers, or deciding what has actually been verified.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
