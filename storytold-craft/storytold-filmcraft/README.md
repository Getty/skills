# FilmCraft skill

Inspect, edit and render video projects and timelines with FilmCraft, including media health, timing and export jobs.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [CLI sessions, scripts and saves](references/cli.md) — driving FilmCraft from subprocesses or constructing a reproducible timeline job.
- [MCP, desktop bridging and error layers](references/mcp-and-control.md) — configuring an agent session, discovering tools, or distinguishing protocol failures from command failures.
- [Ticks, frame grids, source ranges and linked tracks](references/timeline-time-and-targeting.md) — placing, trimming, retiming or moving clips precisely.
- [Media identity, offline assets and project interchange](references/media-and-interchange.md) — importing media, relinking a project, or transferring an edit between applications.
- [Exports, progress, cancellation and delivery gates](references/render-jobs-and-delivery.md) — rendering a sequence or recovering from an uncertain export outcome.
- [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) — setting up an agent, running the supplied helpers, or deciding what has actually been verified.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
