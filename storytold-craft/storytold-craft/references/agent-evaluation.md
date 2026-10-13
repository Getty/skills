# Fresh-agent evaluation and regression protocol

**Read when:** testing whether the skills improve real agent behavior.

Use a fresh agent context with only the selected product skill, a bounded task, a known installed binary and a disposable workspace. Do not preload the expected answer. Capture the agent's actual tool calls, catalog discovery, file changes, warnings, output inspection and final report.

The per-skill evaluation cases are prompts plus explicit expected/forbidden behaviors. They were checked for structure during packaging; they were not executed by real fresh agents here. Do not turn that static check into a pass rate.

Score at least routing correctness, schema/parameter fidelity, authority preservation, unit/index correctness, persistence, recovery, output verification and honesty about unperformed checks. An attractive final artifact does not excuse overwriting originals or inventing successful validation.

Include negative tests: a missing CLI, unsupported build feature, unknown nested field, missing media/font, out-of-root path, partial batch, ambiguous timeout and mismatched CLI/desktop versions. Use local mock services for protocol tests; authorize any real paid generation separately.

Compare results with and without the skill at the same software revision and task budget. Record failure categories rather than only a single score. Re-run after meaningful source/schema changes. Passing synthetic tests of the bundled Python helpers does not measure the creative applications or an LLM's behavior.

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
