# Layer identities, property paths and time bases

**Read when:** animating offset, stretched or reversed layers.

Inspect project, comp and layer in that order. `get_layer` returns the property tree and paths; a group path is not a writable leaf. Use `depth`/`flat` to bound discovery and `get_property` for a single leaf. Effect insertion returns an instance path and parameter paths; retain those instead of assuming the effect became `#1`.

Layer selectors can be IDs, names or one-based `#n` indexes. All-digit strings can be interpreted as IDs if no matching name exists. Avoid ambiguous naming in automation templates and reacquire IDs after opening another project.

## Three different times

Comp time, layer-local time and the current time indicator must not be conflated. Keyframe writes default to layer time. `timeBase:"comp"` explicitly requests composition seconds. `get_property`/`prop.get` time is composition time, while returned key times include layer-local time and, where documented, both bases. Read the operation's exact contract rather than applying one time convention to the whole API.

For an unstretched layer whose start is 10.5 seconds, a key at comp time 15.3 seconds is at layer time 4.8 seconds. Stretching/reversal changes that mapping. Explicit writes snap to the nearest comp frame before conversion to stored layer time. Inspect returned timing metadata and outside-range warnings; a key can exist but have no visible effect in the rendered range.

Set layer placement with the discovered `layer.timing` fields. Trim deltas are relative to each layer's own endpoints. Validate the final keyframes and render before, at and after a transition, not just one arbitrary time.

For effect creation with initial values, the `add_effect` convenience tool applies the operation as one undo step and rejects a failing initial value without leaving a half-configured effect. That local guarantee is not a promise that every multi-command sequence is atomic.

## Evidence

- [effect-agents](https://github.com/storytold/effectcraft/blob/main/docs/agents.md)
