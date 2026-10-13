# CLI workbook operations and command-script grammar

**Read when:** inspecting spreadsheets, running edits or evaluating a formula without a GUI.

`commands --json` discovers engine operations; `functions --json` discovers worksheet functions/signatures. A command catalog is not a formula-function catalog. Filter commands with `--search` and functions with `--search`/`--category` as appropriate.

`info FILE --json` returns workbook structure. `cat FILE --range RANGE` reads a bounded area, optionally formulas/CSV. `eval FORMULA --in FILE --sheet SHEET --cell A1 --json` evaluates in a defined context without requiring a document-edit command. Define both sheet and origin when relative references matter.

```sh
gridcraft-cli run --in source.xlsx \
  --cmd 'cell.set={"cell":"D2","input":"=B2*C2"}' \
  --cmd 'edit.fillDown={"range":"D2:D20"}' \
  --out edited.xlsx --print A1:D5
```

`run` opens `--in`, a named sample or a blank workbook. It processes repeated `--cmd` and `--script` arguments in their given order, then saves/prints. The first failing step stops the run unless a different behavior is explicitly documented by the installed build. Do not infer rollback of preceding changes or external writes.

A command step can be bare ID, `ID=JSON`, `ID JSON` or a JSON object `{command,params}` in a script. Blank/comment lines are skipped. `--quiet` suppresses routine non-null results; it does not turn failures into success. Keep diagnostic output when validating an unfamiliar command.

`convert IN OUT` supports the documented workbook/tabular output formats and optional sheet selection. CSV/TSV is a selected sheet/data projection, not an editable multi-sheet workbook. Use `check` for calculation-oracle and round-trip checks, with its limitations described separately.

For a live app, `send PORT METHOD JSON` is a one-shot control request. It is not MCP and does not create a new workbook session. Capture/verify the existing workbook identity before mutating it.

## Evidence

- [grid-cli-guide](https://github.com/storytold/gridcraft/blob/main/docs/cli.md)
