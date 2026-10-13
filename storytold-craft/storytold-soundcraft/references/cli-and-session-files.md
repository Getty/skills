# CLI edits, session persistence and audio conversion

**Read when:** mixing from scripts or preparing an offline bounce.

`commands FILTER`, `describe ID` and `plugins` expose different discovery surfaces: engine operations, one command's parameters and built-in plugin IDs. `info` accepts audio files or `.scraft` sessions. Do not infer support for an arbitrary third-party plugin from the built-in list.

```sh
soundcraft-cli run --demo \
  --cmd 'mix.volume={"track":"Kick","db":-6}' \
  --save working.scraft --bounce mix.wav --inspect
```

`run` accepts `--in SESSION` or `--demo`, repeated `--cmd 'ID=JSON'`, an optional bounce range and explicit save/inspection. `script FILE` reads one `ID JSON` command per line; it is not the FilmCraft `{id,params}` JSONL format. Preserve that distinction in code-generated scripts.

`convert IN OUT` can request bit depth, sample rate and normalization. Those are signal/encoding transformations, not merely a change of filename extension. Keep the source and verify the resulting format/sample rate/channel layout. Normalization is a content change requiring an intended loudness/peak policy.

The native `.scraft` project depends on associated media, commonly in `Audio Files/`. A saved session file alone is not necessarily portable. Reopen from the intended delivery location and inspect missing media before claiming a complete handoff.

The `app --port PORT METHOD JSON` route targets a running desktop; `mcp` can be headless or connected. Programmatic calls do not open parameter dialogs, and empty parameters can act on current selection. Always inspect the target track/clip and use explicit parameters where documented.

## Evidence

- [sound-cli](https://github.com/storytold/soundcraft/blob/main/apps/soundcraft-cli/src/main.rs)
- [sound-mcp](https://github.com/storytold/soundcraft/blob/main/docs/mcp.md)
- [soundcraft-readme](https://github.com/storytold/soundcraft/blob/main/README.md)
