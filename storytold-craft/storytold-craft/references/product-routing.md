# Product routing by editable object and task

**Read when:** choosing the correct application or splitting a cross-application workflow.

| Task's primary object | Product | Route boundary |
|---|---|---|
| Layered raster image, masks, smart objects | PhotoCraft | Not a RAW-library replacement. |
| Photo catalog, RAW settings, originals/sidecars | LightCraft | A catalog edit and a pixel export are different outputs. |
| Editable paths, objects, artboards | VectorCraft | Raster export does not preserve vector editability. |
| Timeline, clips, sequences, media edit | FilmCraft | Do not substitute composition-local animation semantics. |
| Composition, layer properties, keyframes, effects | EffectCraft | Layer time and comp time differ. |
| Spreads, frames, threaded stories, publication | DesignCraft | Not a generic word-processing model. |
| Existing PDF pages, annotations/forms/redaction | PdfCraft | Not a substitute for the original authoring format. |
| Paragraphs/styles, sections, review revisions | WordCraft | Preserve fields/revisions, not only appearance. |
| Cells/formulas, sheets, tables and calculation | GridCraft | Cached/displayed values are not live formulas. |
| Slides, shapes, layouts and presentation playback | DeckCraft | Static proof is not animation verification. |
| CAD entities, units, blocks, layouts | CADCraft | Visual similarity is not geometric/fidelity proof. |
| Audio tracks, sources, routing and bounces | SoundCraft | A headless session has no physical audio output. |
| Generative creative desktop/SDK investigation | ArtCraft | No comparable operator CLI verified here. |
| Experimental Tauri generation workflow | ArtCraft-X | Dev-server HTTP is not native IPC. |
| Install/update/launch the editors | Craft Launcher | Not the editors' document-operation API. |

Load the product's own SKILL.md and only the relevant thematic references. The overview is optional: every product folder carries its own source ledger, runtime rules, examples and validation scope. Do not load the whole collection into one prompt.

If a task spans products, split it into explicit handoffs. Each stage needs its own input/output format, identity, authority and acceptance criteria. Similar product branding does not establish a shared project model or lossless interchange.

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
