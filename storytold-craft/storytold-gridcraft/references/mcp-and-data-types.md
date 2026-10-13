# MCP helpers, bounded ranges and formula-valued strings

**Read when:** reading/writing cells or building an agent-facing workbook adapter.

`gridcraft-cli mcp` starts an in-process workbook engine; `--in FILE` or `--sample NAME` supplies a starting workbook. `--connect 7979` drives a desktop started with `--control 7979`. The MCP server and a TCP control endpoint use different envelopes despite both being newline-delimited JSON.

Tools include `list_commands {search?}`, `execute_command {command,params?}`, `inspect_workbook`, `list_functions`, `read_range`, `write_range`, `get_cell`/`set_cell`, formatting, tables, charts, sorting and filtering. Do not replace their names/argument fields with PhotoCraft's common-wrapper vocabulary.

`read_range` can return raw or formatted values and formulas. Its default is the used range, which can be far larger than the area relevant to the task. Always bound reads on untrusted or large workbooks and inspect sheet/used-range metadata first. A sparse sheet with a distant styled cell can be expensive to dump naively.

`write_range.values` is two-dimensional; strings beginning with `=` are formulas. Therefore arbitrary imported text is not automatically literal text. Decide whether a field is intended as a formula, number, boolean or literal string and discover the explicit literal-input mechanism before writing formula-looking untrusted content. Do not invent an escape rule without checking this application's parser.

`get_cell` separates value, formula, display text and style. Keep those representations separate during verification. Number formatting changes display, not necessarily the stored numeric value. A table that looks correct in formatted output may contain strings rather than usable numbers, or cached values instead of live formulas.

MCP failures can appear as protocol invalid-params errors or tool results with `isError:true`. Parse both. The reviewed server can return JSON inside a text block; do not assume every successful response has a standardized `structuredContent` shape.

## Evidence

- [grid-mcp](https://github.com/storytold/gridcraft/blob/main/docs/mcp.md)
- [grid-cli-guide](https://github.com/storytold/gridcraft/blob/main/docs/cli.md)
