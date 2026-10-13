# Format directionality and workbook round-trip losses

**Read when:** opening XLS/XLSB/ODS files or exporting a workbook for another application.

The reviewed XLS (BIFF8) importer retains values, formulas, number formats, merges, dimensions and defined names, but not all font/fill/border/chart/object information. XLS output is not supported through the documented path. Convert to XLSX deliberately and retain the original.

XLSB and ODS import are data-oriented: formula cells can become last-saved values and formatting/other workbook features can be omitted. Opening the result successfully, recalculating it or saving it as XLSX cannot recover formulas that were never imported. Read import warnings before claiming that the workbook remains editable or equivalent.

## What check measures

`check` saves/reopens the recalculated workbook and compares package consistency, sheet structure, values/formulas, number formats, merges, names, tables, conditional formatting, validation, charts, comments, hyperlinks and pivots. It also checks OOXML part/relationship integrity that could otherwise cause repair dialogs.

A category list defines the measured coverage, not an exhaustive statement about every Excel feature. For macros, external links, advanced objects or application-specific extensions outside that list, obtain separate evidence. Do not claim macro preservation merely because a `.xlsm` input was accepted by the checker.

CSV/TSV/JSON/HTML exports are different projections of workbook content. Select the intended sheet and range, preserve data types as far as the target supports, and report loss of formulas, styling, multiple sheets or objects. Do not overwrite an original workbook with a data-only projection.

Retain input/output hashes, warnings, producer/cache status, category diffs and a rendered/structural comparison appropriate to the target. An unchanged displayed table does not prove that its underlying formulas and validation rules survived.

## Evidence

- [grid-cli-guide](https://github.com/storytold/gridcraft/blob/main/docs/cli.md)
