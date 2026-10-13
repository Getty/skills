# Persistence, partial success and retry decisions

**Read when:** coordinating multi-step work or handling uncertain outcomes.

Keep these states distinct: engine memory, a document's undo history, a durable native save, a library checkpoint, an exported artifact, a background job and a remote provider job. A successful call can change one without completing the others.

One-shot CLI processes do not share session IDs. LightCraft persistent libraries have exclusive ownership. EffectCraft headless autosave is opt-in and reports checkpoint failures. PhotoCraft nested smart-object contents need explicit inward-to-outward commits. These are product contracts, not interchangeable saving styles.

Do not assume a tool named batch is atomic. PhotoCraft/FilmCraft/common command batches retain earlier edits; EffectCraft exposes both an atomic edit batch and a sequential common wrapper; specific PdfCraft form/object tools can be locally atomic while its common batch is not. Undo history does not roll back arbitrary files or remote work.

A timeout can follow a completed mutation. Broken stdout pipes can leave later CLI steps/saves running. Some MCP cancellation requests intentionally receive no final response. Inspect current state and actual outputs before retrying, especially for inserts, file writes, moved originals or paid generation requests.

Use controller outcomes such as success, failure and uncertain as bookkeeping, not asserted upstream response enums. Include per-step results, actual created paths, warnings and a checkpoint identifier. When state cannot be determined reliably, stop and preserve evidence rather than fabricating a clean rollback.

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
