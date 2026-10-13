# CLI execution, property access and rendering

**Read when:** constructing EffectCraft commands or producing a headless composition.

Discovery uses `commands`, optional filtering and `--json`; `exec --list --schemas` exposes schemas through the CLI. `props COMP LAYER --flat` discovers property paths; `get` reads a property; `set` writes a property or keyframe. Do not guess paths from the visible property label.

The reviewed CLI's project default is a demo for many one-shot commands but an empty project for MCP. Use `--empty`, `--demo` or `--project FILE.ecproj` explicitly. Saving requires `--save` or `--save-as`; inspecting an in-memory project after a successful command is not a saved project.

```sh
effectcraft-cli props Main '#1' --flat --project source.ecproj --json
effectcraft-cli set Main '#1' transform/position '[100,360]' \
  --time 0 --project source.ecproj --save-as edited.ecproj
effectcraft-cli render-frame --project edited.ecproj --comp Main \
  --time 0 --out preview.png
```

Compositions can be IDs/names; `-` selects the active comp. Layers accept IDs, names or `#n`, where n is one-based from the top. Names can collide and ordinal positions can shift. Prefer inspected IDs in a bounded live operation.

`run` accepts alternating command IDs and JSON objects, not FilmCraft's JSONL filename grammar. `script FILE.jsx`/`--eval` executes JavaScript through the application's scripting object model; it is an execution surface requiring separate trust review. Template rendering uses `.ectemplate` plus explicit values; do not pretend it is the same format as a project.

`render-frame` and `render` have different scopes and output options. A relative `--out` is relative to the process working directory; queue outputs follow the project's queue settings. Specify comp, range, frame rate, resolution, quality, color/alpha channels and audio policy intentionally. `--gpu` requests a GPU path; verify the actual backend instead of inferring it from hardware presence.

## Evidence

- [effect-cli](https://github.com/storytold/effectcraft/blob/main/apps/effectcraft-cli/src/main.rs)
- [effect-agents](https://github.com/storytold/effectcraft/blob/main/docs/agents.md)
