# CLI execution and stateful CAD prompts

**Read when:** creating drawings or deciding between textual command input and structured commands.

`cadcraft-cli commands FILTER` emits the command catalog; `info FILE` gives a drawing summary. `run` accepts a file, `--sample` or `--metric`, a textual script/`.scr` file, and repeated `--cmd 'ID JSON'`. Use `--save` for the editable drawing and `--export` for an image/vector/PDF view.

```sh
cadcraft-cli sample bracket bracket.dxf
cadcraft-cli run bracket.dxf --save working.dxf --export preview.png --view extents
cadcraft-cli info working.dxf
```

`--script TEXT` and `--script-file FILE.scr` drive the command prompt. That prompt has state: a point, option or confirmation can be expected instead of a new command. Before retrying or sending another command, inspect/cancel/complete the pending operation as appropriate. Structured commands bypass some interactive prompting but still have their own validation/preconditions.

MCP exposes `command_line` for prompt-style interaction and `execute` for command IDs with JSON. They are different grammars. Do not pass a `.scr` text string as JSON params, and do not guess a JSON field from an AutoCAD prompt keyword.

The command-line drafting notation includes absolute points, `@dx,dy` relative offsets and `@distance<angle` polar notation. Document units, active coordinate system and command state must be defined before those values are meaningful. Use metric startup only when intended, and inspect the resulting units rather than relying on filename conventions.

Like several sibling CLIs, a closed stdout pipe does not necessarily stop later run commands, saves or exports. Capture bounded complete results; do not use `| head` as cancellation.

## Evidence

- [cad-cli](https://github.com/storytold/cadcraft/blob/main/apps/cadcraft-cli/src/main.rs)
- [cad-readme-detail](https://github.com/storytold/cadcraft/blob/main/README.md)
