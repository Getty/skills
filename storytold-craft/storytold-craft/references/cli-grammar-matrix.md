# CLI grammar matrix: do not normalize by guessing

**Read when:** building an orchestrator or translating plans into argument vectors.

| Product | Command execution form | Discovery |
|---|---|---|
| PhotoCraft | `run FILE --cmd ID --params JSON --out FILE` | `commands --json` |
| LightCraft | `run ... ID key=value ...`; JSONL script option | `commands --json`, `controls --json` |
| FilmCraft | `exec ID key=value`; `run FILE.jsonl` with `{id,params}` | `commands --json`, `describe ID` |
| VectorCraft | `run --in FILE --cmd ID --params JSON --export FILE` | `commands` (JSON) |
| EffectCraft | `exec`, property `get/set`, or `run ID JSON ...` | `commands --json`, schema discovery |
| DesignCraft | `run --cmd ID=JSON`; separate native `script` | `commands`, `describe ID` |
| PdfCraft | `run TOOL key=value`; array script `{tool,args}` | `tools` (JSON Schemas) |
| WordCraft | `run --file FILE --cmd ID=JSON --save FILE` | `commands --json` |
| GridCraft | `run --cmd ID=JSON`; `{command,params}` JSONL supported | `commands --json`, `functions --json` |
| DeckCraft | `run --in FILE --cmd ID=JSON --save/--export FILE` | `commands`, `describe ID` |
| CADCraft | `run FILE --cmd 'ID JSON'`; prompt `.scr` scripts | `commands` |
| SoundCraft | `run --cmd ID=JSON`; script lines `ID JSON` | `commands`, `describe ID`, `plugins` |

This is a routing index, not a complete command specification. Consult the product reference for option ordering, save behavior, input initialization and errors. Do not add `--json`, `--help`, `--headless`, `--connect`, `--bridge` or filesystem-root flags uniformly across all products.

Construct subprocess argument arrays without a shell. Keep JSON typed and encoded once. A list of source-reviewed examples is not an installed command catalog: capture the binary's current catalog and compare it to the intended operation before mutation.

The supplied recipe JSON files are explicitly controller manifests, not a new upstream universal script language. The native example scripts retain their product-specific grammars.

## Evidence

- [craft-launcher-readme](https://github.com/storytold/craft-launcher/blob/main/README.md)
- [photo-cli](https://github.com/storytold/photocraft/blob/184c226a76c9ca6234d473912d438feaa48c1cb0/apps/photocraft-cli/src/lib.rs)
- [light-cli](https://github.com/storytold/lightcraft/blob/main/apps/lightcraft-cli/src/main.rs)
- [film-cli](https://github.com/storytold/filmcraft/blob/main/apps/filmcraft-cli/src/main.rs)
- [vector-cli](https://github.com/storytold/vectorcraft/blob/main/apps/vectorcraft-cli/src/main.rs)
- [effect-cli](https://github.com/storytold/effectcraft/blob/main/apps/effectcraft-cli/src/main.rs)
- [design-cli](https://github.com/storytold/designcraft/blob/main/apps/designcraft-cli/src/main.rs)
- [pdf-cli](https://github.com/storytold/pdfcraft/blob/7163ba3dee8becfff6871c9a65d0d8314314742b/apps/pdfcraft-cli/src/main.rs)
- [word-cli](https://github.com/storytold/wordcraft/blob/main/apps/wordcraft-cli/src/main.rs)
- [grid-cli-guide](https://github.com/storytold/gridcraft/blob/main/docs/cli.md)
- [deck-cli](https://github.com/storytold/deckcraft/blob/main/apps/deckcraft-cli/src/main.rs)
- [cad-cli](https://github.com/storytold/cadcraft/blob/main/apps/cadcraft-cli/src/main.rs)
- [sound-cli](https://github.com/storytold/soundcraft/blob/main/apps/soundcraft-cli/src/main.rs)
