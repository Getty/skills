# SoundCraft skill

Operate multitrack audio sessions, source media, mixing, routing, automation and offline bounces with SoundCraft.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [CLI edits, session persistence and audio conversion](references/cli-and-session-files.md) — mixing from scripts or preparing an offline bounce.
- [MCP modes, track identity and musical time](references/mcp-and-time-bases.md) — editing a session with a persistent agent.
- [Decoded media, audio-health scope and portable sessions](references/source-health-and-portability.md) — diagnosing missing sound or packaging a session.
- [Gain staging, inserts, sends and automation](references/mixing-routing-and-automation.md) — making audio edits whose result must be musically or technically correct.
- [Bounce completion, loudness metrics and final checks](references/bounce-loudness-and-verification.md) — delivering audio or deciding whether a mix is actually valid.
- [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) — setting up an agent, running the supplied helpers, or deciding what has actually been verified.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
