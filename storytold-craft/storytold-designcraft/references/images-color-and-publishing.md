# Linked assets, color and publishing handoffs

**Read when:** placing images or producing print and digital variants.

`place_image` accepts a file path or base64 and can target an existing frame or create one. File placement, frame geometry, fitting/cropping and actual image resolution are separate states. Inspect them after placement instead of assuming the visible frame contains the full source at appropriate quality.

Record source paths/hashes and whether the handoff requires links or embedded assets. A copied layout file without its external dependencies is not a complete publishing package. Confirm fonts and profiles on the renderer used for the actual export; do not infer them from a preview generated on a different machine.

The application describes RGB, CMYK and Lab workflows and PDF publication options. Select the intended output condition explicitly and discover the installed `--pdf-options` schema. Assigning a profile and converting colors are not interchangeable operations. Screen appearance alone does not establish the printer's intended output condition.

Keep separate export specifications for print PDF, screen PDF and EPUB. Page geometry, bleed/margins, reading order, linked images and navigation do not transfer identically to a reflowable publication. Do not label an EPUB verified solely because the same layout looked right as a PDF.

For a cross-application IDML exchange, compare stories, frame linkage, styles, page/spread structure, images, swatches and any unsupported constructs after reopening. Preserve a native master and visual reference. A successfully opened IDML file is not proof that another layout application's entire feature set survived.

## Evidence

- [design-cli](https://github.com/storytold/designcraft/blob/main/apps/designcraft-cli/src/main.rs)
- [design-mcp](https://github.com/storytold/designcraft/blob/main/docs/mcp.md)
- [designcraft-readme](https://github.com/storytold/designcraft/blob/main/README.md)
