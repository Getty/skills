# Geometry precision, units and constraint-aware edits

**Read when:** creating dimensionally meaningful drawings rather than visual approximations.

Define model units, origin, coordinate system, working extents and tolerance before geometry creation. A rectangle that looks correct in a PNG can still be the wrong size, non-closed, non-planar or expressed in unintended units. Use numeric entity inspection and relevant measurements as acceptance criteria.

Keep absolute positions, relative offsets and polar input separate. JSON operation angles/units must come from the installed command documentation; do not infer them from an interactive polar prompt. Use finite values and sensible bounds. Reject non-finite coordinates and degenerate windows before issuing commands.

Layers organize visibility, locking, plotting and appearance. Selection commands should inspect layer state as well as entity IDs, especially when hidden/locked entities remain in the document. A visually absent object is not necessarily deleted.

Constraints can re-solve geometry after an edit. Inspect the resulting constraint state and entity coordinates rather than assuming the requested point remained exactly where it was placed. A conflicting or underdefined system may require an explicit design decision, not additional guessed constraints. Preserve a checkpoint before large parametric changes.

Blocks, nested inserts, attributes, hatches, dimensions and free geometry are distinct semantic structures. Exploding a block or converting an annotation to raw lines can improve interchange at the cost of editability. Obtain acceptance for that tradeoff and verify entity counts/topology after the conversion.

For reusable drawings, deliver both the intended numeric specification and a visual proof. A renderer is an observation tool, not a geometric correctness oracle.

## Evidence

- [cad-readme-detail](https://github.com/storytold/cadcraft/blob/main/README.md)
- [cad-cli](https://github.com/storytold/cadcraft/blob/main/apps/cadcraft-cli/src/main.rs)
