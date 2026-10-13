# EffectCraft skill

Build motion graphics, animate composition/layer properties, manage expressions and render jobs with EffectCraft.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [CLI execution, property access and rendering](references/cli.md) — constructing EffectCraft commands or producing a headless composition.
- [MCP schemas, scoped access and bridge limitations](references/mcp-schema-and-confinement.md) — registering an EffectCraft agent or dealing with a denied operation.
- [Layer identities, property paths and time bases](references/layers-properties-and-time.md) — animating offset, stretched or reversed layers.
- [Atomic batches versus sequential batches](references/batches-scripts-and-expressions.md) — grouping dependent edits or considering JavaScript/expression automation.
- [Render snapshots, cancellation and alpha delivery](references/render-queues-gpu-and-alpha.md) — rendering a composition or validating GPU/CPU output.
- [Headless autosave, explicit saves and recovery](references/autosave-and-recovery.md) — keeping agent work across MCP restarts or responding to a checkpoint warning.
- [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) — setting up an agent, running the supplied helpers, or deciding what has actually been verified.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
