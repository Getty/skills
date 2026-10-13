# Safe table edits, formatting and workbook acceptance

**Read when:** performing real spreadsheet changes rather than isolated formula tests.

Inspect sheet names/order, used ranges, tables, defined names, current selection and history before writing. Bound the target rectangle and check whether it intersects tables, merged cells, spill ranges or existing formulas. Do not clear a convenient large area simply to make an example fit.

When writing a data table, preserve headers, column meanings, types and formulas separately. Use `create_table` when the task requires a real table object, not merely a colored range. Use discovered formatting fields for appearance and re-read raw values/formulas to ensure formatting did not conceal an input error.

Sort/filter commands operate on a defined range and header policy. Verify that whole records moved together and that formulas/table references still point to the intended data. A sort on one isolated column can produce a plausible but semantically corrupted dataset.

For an acceptance sample, write numeric inputs and a simple formula, re-read both raw and formatted values, save, reopen and re-evaluate. Then validate the task's more difficult features. Inspect all checker coverage counts; no-oracle and volatile cases must remain visible in the report.

A useful delivery contains the editable workbook, an inspection report, applicable `check` JSON (`gridcraft-check/1` in the reviewed version), and unresolved fidelity limitations. The checker caps example listings with `--max-report`, not the underlying counts. Do not present the displayed examples as the complete failure set.

## Evidence

- [grid-mcp](https://github.com/storytold/gridcraft/blob/main/docs/mcp.md)
- [grid-cli-guide](https://github.com/storytold/gridcraft/blob/main/docs/cli.md)
