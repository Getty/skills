# Document identity, masks and smart-object ownership

**Read when:** editing structure, targeting layers, or saving nested smart-object contents.

## Establish identity before selection-sensitive work

Inspect the active document, dimensions, mode, depth, layer tree and history. Save a baseline and record the IDs returned by the live session. Names are useful labels but may be duplicated; layer order changes under insert, grouping and deletion. Do not persist session IDs as reusable templates across reopened documents.

A layer's raster mask and vector mask are different objects. `hasMask` reports a raster mask; `hasVectorMask` reports vector-mask presence, while `vectorMaskEnabled` records its enabled state or absence. A disabled vector mask is still present. A selection, a mask attached to a layer and the currently edited mask target are also distinct states.

For a localized adjustment, define the intended region, inspect selection bounds, create or target the appropriate adjustment layer, and verify which mask receives the operation. Compare both the affected region and an untouched control region. Do not interpret an apparently unchanged image as proof that a mask was attached correctly: the mask may be disabled, inverted, or attached to the wrong layer.

## Preserve editability deliberately

Keep type as type, adjustments as adjustments and smart objects as smart objects when that is part of the deliverable. Rasterizing, flattening or converting a smart object to layers is a structural change requiring a working copy and an explicit reason. A visually correct PNG does not verify the editable structure of a PSD or native file.

Embedded smart-object workflows use `layer.smartObjects.editContents`, `layer.smartObjects.saveContents`, and, for a deliberate structural conversion, `layer.smartObjects.convertToLayers`. A returned/opened contents document has a parent relationship. Saving it with `doc_save` exports that child; it does not substitute for `saveContents` into the parent.

For nested smart objects, commit the innermost contents first, then each enclosing contents document, then save the outer document. Reopen that outer file and inspect/render again. External linked sources may be refused by the automation policy even when the corresponding interactive feature exists; do not work around a refusal by expanding access without authorization.

## Safe experiments

`image.duplicate` or `history.newDocument` can create a new active document for experiments. Record that the active-document identity changed. Undo on the old document cannot recover a disk file overwritten by the experiment. Prefer named checkpoints over a guessed number of undo calls.

## Evidence

- [photo-mcp](https://github.com/storytold/photocraft/blob/184c226a76c9ca6234d473912d438feaa48c1cb0/docs/mcp.md)
- [photo-control](https://github.com/storytold/photocraft/blob/184c226a76c9ca6234d473912d438feaa48c1cb0/docs/control-protocol.md)
- [photocraft-readme](https://github.com/storytold/photocraft/blob/main/README.md)
