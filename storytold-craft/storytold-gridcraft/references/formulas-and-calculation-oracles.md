# Formula validation and independent cached-value oracles

**Read when:** checking calculation correctness or interpreting gridcraft-cli check results.

`check` compares recalculated formula values against cached results stored by a prior calculating producer. It uses numeric tolerance, error-kind comparison and exact text/boolean comparison. A cached zero written by a non-calculating library is not automatically a trustworthy oracle.

Files requesting full calculation on load, or formula cells without a stored value, can be classified as no-oracle. Volatile formulas and their dependent cells are skipped. Counts for checked, matched, mismatched, noOracle and volatile must be included in any correctness claim. An exit status of zero with zero independently checked formulas is not evidence that the workbook's formulas were independently validated.

The checker groups mismatches by function and by type transition, and identifies primary mismatches whose precedents did not already mismatch. Start debugging at those primary cases instead of fixing every downstream error independently. Use a minimized workbook or `eval` call with the same reference context.

## Formula semantics to preserve

Retain the actual formula text, origin cell, sheet, names, table references and input types. Relative references depend on origin; filling a formula down is not equivalent to copying the exact formula string into every row. Spill ranges and circular/error states need explicit inspection rather than conversion to displayed text.

Discover support from the installed function catalog. A function with a familiar name is not proof that every optional argument, locale behavior or edge case matches Excel. Validate the signatures and a representative edge case for the task. A formula result matching a simple arithmetic expectation is useful smoke evidence, but it is weaker than independent corpus validation.

The checker normalizes some error representations for XLSX storage, including certain spill/calculation/circular cases. Distinguish allowed serialization equivalences from true semantic fidelity when reading a round-trip report.

## Evidence

- [grid-cli-guide](https://github.com/storytold/gridcraft/blob/main/docs/cli.md)
- [grid-mcp](https://github.com/storytold/gridcraft/blob/main/docs/mcp.md)
