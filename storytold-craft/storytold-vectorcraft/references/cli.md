# CLI grammar, artboard selection and loss-aware conversion

**Read when:** building vector processing scripts or converting an imported illustration.

`vectorcraft-cli commands` prints the command catalog as JSON without requiring a `--json` flag. `info FILE` includes title, units, color mode, artboards, object counts, fonts and import warnings. Read those warnings before overwriting or normalizing an imported file.

```sh
vectorcraft-cli info source.svg
vectorcraft-cli run --in source.svg --export working.vectorcraft --export preview.png
vectorcraft-cli convert working.vectorcraft delivery.pdf
```

`run` accepts `--cmd ID` followed by `--params JSON`, repeated in order. It can export more than one output in one session. This is not the `ID=JSON` grammar used by DeckCraft/GridCraft. Avoid truncating a mutating process's output with a pipe: behavior after a closed pipe is not a portable cross-app transaction boundary.

## Artboard indexing is deliberately inconsistent by option

`convert --artboard I` is zero-based, while `--range '1-3,5'` is one-based. A PDF normally receives all artboards unless restricted; EPS uses artwork bounds; other formats default to the first artboard. Requesting a PNG is not an implicit all-artboard export. Record the selected boards and compare output page/image count with the specification.

`--outline-text` affects SVG text by turning it into paths. It may improve appearance portability but sacrifices editability, text extraction and some accessibility behavior. Use only when those tradeoffs are accepted and retain an editable master.

`--replace-lossy` permits an in-place replacement after a lossy import. It is a safety override, not a quality enhancement. Prefer a new path, preserve the original, and state what the importer omitted or reconstructed from a preview. Import/export support is obtained from the executable's current format list, not from a sibling application's capabilities.

`bench` and `perf` generate measurements or synthetic stress work; they are not capability discovery probes and can consume substantial resources. Keep them outside routine metadata capture.

## Evidence

- [vector-cli](https://github.com/storytold/vectorcraft/blob/main/apps/vectorcraft-cli/src/main.rs)
