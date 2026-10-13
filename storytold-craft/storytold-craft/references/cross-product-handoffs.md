# Cross-product asset contracts

**Read when:** building a pipeline across several Craft applications.

Examples of sensible pipelines include LightCraft → PhotoCraft for RAW development followed by layered editing; VectorCraft → DesignCraft/DeckCraft for illustrations in publications/presentations; EffectCraft → FilmCraft for rendered motion graphics in a timeline; SoundCraft → FilmCraft for a mixed audio deliverable; and WordCraft/DesignCraft/DeckCraft → PdfCraft for final PDF inspection/review. These are proposed workflows, not claims of automatic native-project interchange.

Each handoff should record:

1. The actual file format and editable semantics retained or intentionally flattened.
2. Dimensions, units, duration/rate, color/alpha or audio-channel interpretation as relevant.
3. External dependencies, input/output hashes, producing binary/catalog identity and warnings.
4. A consumer-side import, inspection and bounded render/bounce check.

PNG carries pixels, not editable layers or vector paths. A video render carries frames, not an editable effect graph. PDF carries a page representation, not the complete authoring model. CSV carries tabular data, not the full spreadsheet's formulas/styles/objects. Preserve editable masters separately whenever required.

Do not force all product coordinates into one untyped number. Distinguish displayed PDF points, DesignCraft spread points, DeckCraft slide points, image pixels/normalized crop coordinates, CAD model units, FilmCraft ticks and SoundCraft samples/beats. Convert only with known origins, scales and rates.

An output valid in the producing app is not automatically valid in the consuming app. Reopen it in the next stage, compare semantic invariants and stop on unaccepted losses. Keep stage completion and whole-pipeline completion separate.

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
