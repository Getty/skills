# DXF/DWG round-trip risk and delivery checks

**Read when:** opening external CAD files or saving a supposedly compatible drawing.

The reviewed implementation reads DXF across several historical variants and writes a specific supported version; DWG support is provided through its selected library with its own read/write boundaries. Confirm the installed version's actual support rather than promising arbitrary DWG compatibility.

Most importantly, imported entity types that CADCraft does not model are not necessarily preserved on save. A drawing can open and look mostly correct while a subsequent save drops unsupported content. Keep the original immutable, inspect entity types/warnings and export to a new path. Do not normalize an important source file in place merely to test the application.

Compare pre/post entity counts by type, blocks/attributes, layers, styles, text, dimensions, layouts and constraints relevant to the task. Check known dimensions and coordinate bounds numerically. Reopen the saved drawing, render the relevant views and compare layout/plot outputs separately from model-space previews.

For a downstream CAD/CAM/printing workflow, verify the consumer's required version, units, closed paths, annotation behavior and other task-specific invariants. A visually matching SVG cannot prove that DWG attributes, constraints or unsupported entities survived. Report the measured subset and any intentional conversion such as exploding blocks or flattening annotations.

The supplied sample workflow is appropriate for smoke testing command execution and file output. It is not a qualification of an installation for every external CAD format or precision-sensitive production task.

## Evidence

- [cad-cli](https://github.com/storytold/cadcraft/blob/main/apps/cadcraft-cli/src/main.rs)
- [cad-readme-detail](https://github.com/storytold/cadcraft/blob/main/README.md)
