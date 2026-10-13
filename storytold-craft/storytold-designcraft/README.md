# DesignCraft skill

Compose page-layout documents with threaded stories, frames, styles, images and publication exports in DesignCraft.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [CLI scripts and order-dependent export options](references/cli-and-export-order.md) — constructing a page-layout batch or exporting several variants.
- [MCP identity, spread geometry and UTF-8 byte offsets](references/mcp-coordinates-and-utf8.md) — placing frames or editing text through a stateful agent.
- [Threaded stories, styles and overset detection](references/stories-frames-styles-and-overset.md) — flowing long text through pages or changing typography.
- [Linked assets, color and publishing handoffs](references/images-color-and-publishing.md) — placing images or producing print and digital variants.
- [A layout production loop with explicit checks](references/production-and-verification.md) — turning a brief into an editable layout and verified delivery.
- [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) — setting up an agent, running the supplied helpers, or deciding what has actually been verified.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
