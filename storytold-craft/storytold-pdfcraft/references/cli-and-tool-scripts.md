# CLI commands and session-scoped tool scripts

**Read when:** extracting PDF information, scripting a multistep edit, or discovering exact schemas.

`pdfcraft-cli tools` returns the automation table with JSON Schemas. This is a schema-bearing tool catalog, not merely a list of menu labels. The same table powers `run` and MCP. Prefer exact task-tool schemas over guessing parameters from a command's English name.

```sh
pdfcraft-cli info source.pdf
pdfcraft-cli text source.pdf --page 1
pdfcraft-cli edit source.pdf --rotate 1:90 --out rotated.pdf
pdfcraft-cli render rotated.pdf --page 1 --dpi 96 --out preview.png
```

The CLI also exposes combine, extract and split. Ranges in these interfaces are one-based. `--help` is handled at the top level and immediately after a subcommand in the reviewed parser. `check` is a robustness harness that opens/inspects/renders files in separate child processes with time limits. `audit` detects faux redactions and fails when it finds them; it is not a proof that every possible confidential datum is absent.

## One script, one document-ID space

A single `run TOOL key=value...` creates its own automation session. Opening a document in one process does not make its ID usable in another process. Use persistent MCP or `run --script FILE.json` for dependent operations. The native script is an array of `{tool,args}` entries; a per-step `out` writes an image result. It is not FilmCraft JSONL and not PhotoCraft's action format.

In the reviewed CLI implementation, fresh script document IDs are allocated in sequence starting at 1. For persistent or mixed workflows always bind the actual returned IDs rather than assuming 1. Saving/closing a document and switching sessions changes what an ID refers to.

`--root DIR` constrains tool and output paths, with relative paths resolving inside that root. The script file itself may be read from outside the root. Accordingly, root confinement does not make an unreviewed script trustworthy; it limits its file authority after loading. Root setup and script approval are separate checks.

The supplied example script is a native read-only tool sequence. Review and adapt its input filename/query before running it; its syntax is checked locally, but it was not executed against a PdfCraft binary during bundle construction.

## Evidence

- [pdf-cli](https://github.com/storytold/pdfcraft/blob/7163ba3dee8becfff6871c9a65d0d8314314742b/apps/pdfcraft-cli/src/main.rs)
- [pdf-automation](https://github.com/storytold/pdfcraft/blob/7163ba3dee8becfff6871c9a65d0d8314314742b/crates/automation/README.md)
