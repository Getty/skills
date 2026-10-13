# CLI sessions, scripts and saves

**Read when:** driving FilmCraft from subprocesses or constructing a reproducible timeline job.

Use `commands --json` for discovery and `describe ID` for one command's current parameters and enabled state. `inspect` returns project/sequence structure; `probe MEDIA` examines a source without importing it. Catalog discovery, media probing and timeline mutation are separate operations.

The CLI uses global options and subcommands rather than PhotoCraft's repeated `--cmd` interface:

```sh
filmcraft-cli --project source.fcproj --save-as edited.fcproj \
  exec file.newBin name=AgentReview
filmcraft-cli --project edited.fcproj inspect sequence
filmcraft-cli --project edited.fcproj render --seconds 1 --out preview.png
```

`exec ID` accepts `key=value` pairs or a JSON parameter object. Values that parse as JSON keep their types; other values become strings. `run FILE.jsonl` reads `{id,params}` steps in one process, accepts stdin as `-`, and recognizes comment lines. `--keep-going` continues past failed steps; retain every result instead of declaring the whole script successful.

Use `--save` to write back to the opened project only when authorized, or `--save-as` to preserve an independent working file. A headless process without a save does not establish persistent project changes. `--bridge HOST:PORT` targets the desktop's actual session and cannot simultaneously select a separate headless `--project`/`--demo`.

## Export has an additional health gate

`export OUT` normally waits for completion and supports presets, explicit settings, range, scaling, audio policy and queue selection. `export --list-presets` discovers presets. The reviewed high-level CLI export/render commands warn and exit 1 if they drew offline-media placeholders, unless `--allow-offline` was explicitly supplied. This is stronger than the generic engine/MCP export's success contract. Do not add `--allow-offline` to make CI green without accepting the placeholder content.

Exit 2 is a usage failure; exit 1 includes command failures and unaccepted offline media. A closed stdout reader does not cancel the program: later script steps, exports and saves can still execute. Do not use `| head` as a way to stop a mutating run.

## Evidence

- [film-cli](https://github.com/storytold/filmcraft/blob/main/apps/filmcraft-cli/src/main.rs)
