# Model-space previews versus paper-space publication

**Read when:** exporting drawings, dimensions or layout sheets.

Model-space geometry, paper-space page layouts and viewport scales are separate coordinate systems. A scaled viewport is not a scaled copy of the underlying geometry. Inspect the active space, layout, viewport scale and per-viewport layer visibility before plotting.

The reviewed CLI image exports (`convert` and `run --export` for PNG/SVG/PDF) frame model space. They are not automatically equivalent to plotting a chosen paper-space layout. For layout publication use the relevant PLOT/export engine workflow and discover its actual parameters; do not assume that naming an output `.pdf` selects the intended sheet.

Framing rules are explicit. Convert defaults to extents. Run-export uses the current view if commands changed it, otherwise extents. `--window x0,y0,x1,y1` uses drawing units and requires finite ordered bounds; `--view extents` or `--view current` forces a mode. The rectangle is fitted without distortion, not independently stretched in x/y. These controls cannot be freely combined.

Fonts affect technical meaning when labels, symbols or dimensions are involved. The app uses system TrueType/OpenType fonts and optional build-time font inputs; SHX fonts are not read as native SHX in the reviewed README. Fallback can change glyphs/metrics. `FONTALT`/`FONTFALLBACK` and their CADCraft environment forms are deliberate substitution controls, not proof of original font fidelity.

Validate dimension values, associativity where required, glyph coverage, hatch/island behavior, lineweights/linetypes and page scale in the actual exported output. Keep a dimensional check alongside the visual proof.

## Evidence

- [cad-cli](https://github.com/storytold/cadcraft/blob/main/apps/cadcraft-cli/src/main.rs)
- [cad-readme-detail](https://github.com/storytold/cadcraft/blob/main/README.md)
