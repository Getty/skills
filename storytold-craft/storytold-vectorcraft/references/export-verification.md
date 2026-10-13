# Multi-artboard export and round-trip checks

**Read when:** delivering PDF/SVG/raster outputs or validating a lossy import.

Use a two-track acceptance test. Structurally inspect artboard count, selected board IDs, layer/object types, text content, hidden material, links and editable effects. Visually inspect every delivered board at a fixed preview scale and inspect small text, thin strokes, clipping and gradients at a more detailed scale where necessary.

Write to a new output path. For import/export round trips, keep a warning ledger and compare the original and reopened working file. An EPS imported from a preview, or a format that omits hidden text/art, must be described as reconstructed/partial rather than lossless. Do not invoke `--replace-lossy` without an accepted destructive change.

Verify the delivery's page count and bounds. `--artboard` and `--range` use different index bases; test the boundary cases explicitly. PDF, EPS and raster exports have different default board/bounds selection. A single valid PNG does not prove a multi-board export completed.

A bounded document preview answers “does this look right?” It does not verify the final file's ICC profile, font portability, editability or downstream importer behavior. Reopen the actual delivery when possible and retain both structural and visual evidence. Report any validation that could not be performed rather than converting an upstream feature claim into a task result.

## Evidence

- [vector-cli](https://github.com/storytold/vectorcraft/blob/main/apps/vectorcraft-cli/src/main.rs)
- [vector-mcp](https://github.com/storytold/vectorcraft/blob/main/docs/mcp.md)
