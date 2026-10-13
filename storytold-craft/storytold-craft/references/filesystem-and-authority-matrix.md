# Filesystem authority is product- and mode-specific

**Read when:** isolating an agent, granting file access or investigating denied operations.

| Product/mode | Reviewed native policy |
|---|---|
| PhotoCraft MCP/serve | Separate granted read/write roots; absent authority is denied. Direct CLI uses ordinary OS paths. |
| VectorCraft scoped MCP | Optional root flags activate scope and imply headless; paths are cwd-relative before checking; connected app enforces its own roots. |
| WordCraft scoped MCP | Optional root flags constrain headless; not accepted with connect; reviewed desktop has no equivalent roots. |
| EffectCraft scoped MCP | Repeatable roots; read permitted under read/write roots, writes under write roots; absolute paths; scripts and some UI paths refused. |
| PdfCraft MCP/tool run | Optional single root covers reads/writes and resolves relative paths inside it; UI uses a separate descriptor. |
| FilmCraft MCP | No corresponding root flags in the reviewed parser; ambient OS authority. |
| Other editor modes | No universal native-confinement contract established by this review; verify installed options and isolate at OS level as needed. |

A loopback listener is not an OS sandbox, a token is not file confinement, and a read-only hint is not authorization. Path-root checks can have explicitly documented local race limitations. Avoid hostile shared writable directories and restrict the executing account/container where the threat model requires it.

Authorize these effects independently: modifying an open document, saving over an existing path, deleting/moving originals, loading plugins/scripts, starting a network service, uploading private assets, spending provider credits and publishing output. Do not route around a denied filesystem operation through a script or UI click.

The metadata probe sends only discovery requests, but launching a native application is still executing trusted code that may initialize settings or libraries. The probe is not a sandbox and does not establish that a binary is safe.

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
