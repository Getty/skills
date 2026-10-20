# Validated React Flow editor example

This original example combines a small untrusted-input parser, numeric-port DAG rules, bounded local snapshot history, and a controlled React Flow UI. It is intentionally not a production workflow executor or collaboration implementation.

## Run the tested core without installing anything

From the skill root:

```sh
node --test tests/graph-model.test.mjs
```

## Install and validate the UI in a networked environment

The manifest's ranges are illustrative compatibility constraints, **not a tested dependency lock or a security-approved version set**. Review current patched releases, peer requirements, install scripts, and the project's runtime policy before resolving them. No lockfile was fabricated.

```sh
cd examples/flow-editor
npm install
npm run typecheck
npm run build
npm run dev
```

Commit the generated lockfile after review. The authoring environment could not access the registry; dependency installation, external-library typechecking, production build, and real browser behavior were not executed. The TSX received syntax transpilation only. See [validation](../../VALIDATION.md).

## Exercise

Connect the default nodes by button or handles; add a process; move nodes; export/import; undo/redo; delete selected nodes. Try malformed JSON, unknown types, duplicate IDs, invalid ports, and cycles. The canvas has explicit dimensions, required CSS, stable type maps, and named handles. Node moves commit a history snapshot at drag end, not every pointer event.

## Deliberate limits

The example has three node types, one input per receiver, no actual evaluation, no persistence service, no authentication, no reconnect UI, no grouping/layout engine, and no collaborative undo. The button alternative connects only the default nodes; a production editor needs a complete accessible port-selection command UI. Large-graph hover validation should use a revision-scoped validated index rather than repeatedly parsing the whole graph. Selection is transient and can reset when applying a document snapshot. Multi-selection drag/resize history needs a dedicated transaction controller before production use. Viewport persistence and imported-schema migration are described in references but not implemented here.
