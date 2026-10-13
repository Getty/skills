# Source evidence, version drift and collection maintenance

**Read when:** updating the skills or deciding how strong a claim can be.

This collection was authored from repository documentation, selected implementation slices and targeted source searches reviewed on 2026-10-12. It is not a complete audit of every file or a simultaneous release snapshot. The source ledger records file/blob identities where captured and pinned commits where available; unpinned README links can move.

Use the following evidence ladder: source reviewed; binary/catalog observed; operation executed; native save/reopen verified; delivery inspected; fresh-agent task passed. Never relabel one level as another. Static validation of an example proves syntax/structure, not that an installed editor accepted or correctly executed it.

On update, compare both CLI dispatch/usage and MCP tool schemas/handlers. Track save/overwrite rules, path authority, units/index bases, strictness of nested parameters, warning fields, defaults and cancellation semantics. A familiar command name can change behavior without disappearing from the catalog.

Do not use README feature percentages as task-level acceptance tests. Preserve boundary cases in the evaluation set: a partial batch, non-ASCII text offsets, missing assets/fonts, a save/reopen cycle, a lossy import, a timeout and a constrained-path refusal.

The supporting repositories—shared libraries/fonts, service infrastructure, corpora, release actions and launcher assets—can explain dependencies and tests. They are not automatically additional operator applications. Investigate their relevant files when a task requires it rather than creating fictitious user-facing CLIs for every repository in the organization.

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
