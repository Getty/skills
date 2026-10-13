# Color, typography, LUTs and format fidelity

**Read when:** matching an appearance, exporting editable files, or baking a color look.

## Specify the rendering contract

Record document color model, bit depth, ICC profile intent, dimensions and alpha policy. RGB, CMYK, Lab, grayscale and high-bit-depth images are not interchangeable byte buffers. A color-mode conversion, assigning a profile, converting to a profile and soft-proofing have different meanings. Resolve the appropriate command and parameters from the installed registry; never select a conversion because it makes a warning disappear.

For PSD/PSB delivery, evaluate the actual constructs used: groups, masks, type, blend modes, styles, adjustment layers, smart objects and hidden content. Upstream corpus results are evidence about that corpus, not a promise of lossless round-trip for an arbitrary file. Keep the original and record import/export warnings. Prefer a native working file plus an explicit interoperability export when the format contract permits it.

## Font fidelity is observable

`convert` and `run` warn about missing families on stderr; compact `info` carries warnings in JSON. `run` can attach warnings to the command result that first exposes the missing font. A successful file save can therefore still use fallback rendering. The original family declaration is not silently repaired by those warnings. Discover `type.resolveMissingFonts` to inspect or intentionally replace families, then check line breaks, bounds and glyph coverage again.

Do not package fonts without distribution rights. A screenshot produced with a fallback is not evidence that another machine has the original font. Record the intended family and the installed match in the handoff.

## Color Lookup Table export

`file.export.colorLookupTables` bakes a color-only 3D LUT. Valid lattice sizes are 2–129. Select all visible top-level adjustment layers, a current selected scope, or an explicit unique `layers` list; do not combine a selected scope and a conflicting explicit list. Explicit IDs must identify existing visible top-level adjustment layers.

The engine uses document stack order, bottom to top, not the order of IDs supplied by the caller. Omitting `path` returns the `.cube` text instead of writing it. Spatial masks, vector masks and clipping cannot be represented faithfully in a color-only LUT; grouped adjustments are not exported as independent layers. Describe this loss in the deliverable rather than calling the LUT an exact copy of the document look.

## Evidence

- [photo-cli-guide](https://github.com/storytold/photocraft/blob/184c226a76c9ca6234d473912d438feaa48c1cb0/book/src/automation/cli.md)
- [photocraft-readme](https://github.com/storytold/photocraft/blob/main/README.md)
