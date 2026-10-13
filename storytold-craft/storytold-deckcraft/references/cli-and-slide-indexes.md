# CLI deck construction and zero-based slide rendering

**Read when:** creating an editable presentation or rendering all slides.

Use `commands FILTER` for the JSON command catalog and `describe ID` for one command. `info FILE` inspects slides/titles/layouts. `run` opens `--in FILE` or `--sample`, applies `--cmd 'ID=JSON'` entries, and saves/exports explicitly.

```sh
deckcraft-cli run --sample \
  --cmd 'slide.new={"layout":"titleOnly","title":"Agent verification"}' \
  --save working.deckcraft --export delivery.pptx
deckcraft-cli render working.deckcraft --all --scale 1 previews/
```

Keep native `.deckcraft` as the working master when its semantics are required and export `.pptx` as an interoperability deliverable. A successful file save does not verify the intended PowerPoint compatibility for animations, media or every style feature.

## Render index base and coverage

The reviewed CLI `render --slide N` uses zero-based indexes and defaults to slide 0. `--all` iterates the whole deck; output filenames are numbered from 1 (`slide-01.png`, etc.). Do not confuse a user-visible filename number with the selector's index. Plain PNG/JPEG conversion uses the first slide rather than automatically rendering every slide.

The source parser's default render scale is 2.0. Set `--scale` explicitly for reproducible previews and record actual image dimensions. An editor-style rendering option and a presentation rendering can differ; select the intended view before comparing output.

There is no reason to depend on a generic `--help` behavior here: the reviewed dispatcher lists commands/describe and version, and unknown top-level arguments produce usage failures. Prefer verified discovery calls and current source/help where available.

`app --port PORT` sends commands/control requests to a running deck; it is not a separate saved-file edit. Inspect live document identity before use.

## Evidence

- [deck-cli](https://github.com/storytold/deckcraft/blob/main/apps/deckcraft-cli/src/main.rs)
- [deck-mcp](https://github.com/storytold/deckcraft/blob/main/docs/mcp.md)
