# Ticks, frame grids, source ranges and linked tracks

**Read when:** placing, trimming, retiming or moving clips precisely.

FilmCraft's time base is 254016000000 ticks per second. Sequence inspection distinguishes timeline `start`/`end` from `sourceIn`/`sourceOut`; do not substitute source time for sequence time. Commands can expose seconds, frame or timecode forms, but accepted fields remain command-specific.

For a rational frame rate `num/den`, one frame is `254016000000 * den / num` ticks. Use exact integer/rational arithmetic when representable and quantize only at the documented boundary. At 30 fps this is 8467200000 ticks per frame; at 30000/1001 fps it is 8475667200. Avoid accumulating frame positions with repeated floating-point addition.

`timeline.place` snaps start and end independently to the sequence's frame grid. Validate the resulting range and `durationFrames`, not just the requested duration. The inspection count includes a partial final frame. Speed and reverse change how the source interval is traversed; they do not redefine the timeline coordinate system.

## Track and selection identity

Tracks accept live IDs or names such as V1/A2. An invalid explicit track must be treated as a failure, never silently replaced with another track. `timeline.place.track` controls picture placement and `audioTrack` controls sound; specifying an audio track as `track` places sound alone.

Discover clip/item IDs in the active project before using them. For commands supporting explicit `clip(s)` or `item(s)` targets, those targets can remove the selection requirement but not unrelated preconditions. The catalog's enabled state may still describe the current selection rather than the supplied explicit targets. Do not invent an explicit-target parameter on commands that do not document one.

Linked Selection can cause a timeline move to move a picture's sound partner. `timeline.move` returns all moved IDs; inspect that set. Use `linked:false` only when separation is intended. Check gaps, overlaps, sync and neighboring clips after ripple-style operations, and render frames on both sides of each edit boundary.

## Evidence

- [film-agents](https://github.com/storytold/filmcraft/blob/main/docs/agents.md)
- [film-cli](https://github.com/storytold/filmcraft/blob/main/apps/filmcraft-cli/src/main.rs)
