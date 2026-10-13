# Gain staging, inserts, sends and automation

**Read when:** making audio edits whose result must be musically or technically correct.

Inspect tracks, inserts, sends, buses, automation, mutes/solos and source availability before changing levels. A silent mix can be caused by routing, selection, automation or unavailable processing rather than a missing source. Keep the health query separate from signal-path inspection.

Use documented units. `mix.volume` takes dB in the reviewed example; do not pass a linear amplitude ratio as though it were dB. Plugin parameters have their own units, ranges and normalized representations. Discover the installed plugin/command schema rather than importing parameter names from another DAW.

A static gain change can be overridden or modulated by automation. Inspect automation lanes/mode at the relevant times and verify the effective result across the range, not at a single playhead position. Track sends and pre/post-fader choices, where supported, can change whether a level edit also changes effects balance.

For insert changes, record order as well as plugin identity/settings. Processing order matters: a compressor before an EQ is not generally equivalent to the reverse. This is a signal-chain acceptance rule, not a claim that the application optimizes or normalizes arbitrary plugin order.

Apply one conceptual change at a time, compare a short bounded bounce and inspect the associated state. Avoid irreversible normalization, destructive source edits or broad track selection when the brief asks for a mix adjustment. Preserve a checkpoint so a technically valid but unwanted sonic result can be compared and reverted deliberately.

## Evidence

- [sound-mcp](https://github.com/storytold/soundcraft/blob/main/docs/mcp.md)
- [sound-cli](https://github.com/storytold/soundcraft/blob/main/apps/soundcraft-cli/src/main.rs)
- [soundcraft-readme](https://github.com/storytold/soundcraft/blob/main/README.md)
