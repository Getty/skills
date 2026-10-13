# MCP mode selection and tool-name boundaries

**Read when:** configuring an agent client or reducing discovery overhead.

All twelve specialized editors have a reviewed `-cli mcp` entry point, but startup behavior differs. Most default to an in-process headless session. VectorCraft's bare MCP can attach to a live app and then fall back; explicitly select `--headless` there. Project/library/demo startup options and save behavior remain product-specific.

Common wrappers (`command_list`, `command_run`, `command_batch`, `doc_inspect`, `render_preview`) exist in several apps, but not as a proven universal replacement for every product's documented tools. WordCraft/DesignCraft/CADCraft/SoundCraft use families such as `execute`; GridCraft uses `execute_command`; DeckCraft uses `run_command`. Discover the actual catalog before dispatch.

Some catalogs provide complete tool input schemas, some provide prose parameter descriptions, and some have a mix. PdfCraft has a schema-described task table; EffectCraft can expose command schemas; LightCraft's generated command tools retain prose/free-form engine params. Do not silently promote prose to authoritative JSON Schema.

Compact mode is useful where explicitly supported, notably LightCraft and PdfCraft. Retain meta-discovery so the agent can find an omitted specialist capability. Bound tool/resource queries rather than dumping whole projects or libraries into context.

Raw desktop control is generally a separate JSON-lines protocol with `{id,method,params}` and `{ok,...}` replies. It is not MCP JSON-RPC just because the JSON looks similar. PhotoCraft requires per-connection authentication; PdfCraft uses a private control-descriptor file; WordCraft has a control-key mechanism. Other apps must be checked individually.

Several apps share a documented default port 7979. Assign distinct live-control endpoints and verify the expected app/document before editing. A successful connection to the wrong Craft app is not a harmless configuration error.

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
