# MCP modes, track identity and musical time

**Read when:** editing a session with a persistent agent.

`soundcraft-cli mcp` starts a headless engine without a window or audio device. `--demo` is useful for an isolated functional sample. `--connect 7801` drives a desktop started with `--control 7801`. A headless transport-play command cannot prove sound reached a speaker; use an offline bounce and inspect/listen to it where possible.

Tools include `list_commands`, `execute`, `batch`, `inspect_session`, open/save/new session, import and bounce helpers. `batch.keep_going` controls continuation. A failed step still makes the tool result an error even when later steps ran. Read all results; do not assume a global rollback contract that was not established.

Positions can be sample counts, a seconds object or bars/beats-style strings. They are not interchangeable numeric literals. Resolve the session sample rate, tempo/meter map and the specific command's accepted time form before editing. Changing tempo can alter the musical interpretation of positions; distinguish audio sample placement from musical beat placement.

Tracks can be selected by name or ID, clips by ID. Names can collide or be renamed; retain freshly inspected IDs for a bounded sequence. After trimming, moving or splitting, inspect the actual clips and playlist state before issuing another operation with old IDs.

The common pipeline is inspect session → resolve sources/tracks/clips → apply a bounded edit → inspect routing/automation → bounce → verify → save/reopen. UI screenshots are useful only for live interaction state; they cannot verify the waveform or perceived result of an offline audio job.

## Evidence

- [sound-mcp](https://github.com/storytold/soundcraft/blob/main/docs/mcp.md)
- [sound-cli](https://github.com/storytold/soundcraft/blob/main/apps/soundcraft-cli/src/main.rs)
