# Document CLI commands and explicit review output

**Read when:** reading, revising or converting documents from shell jobs.

`commands --json` is the reliable discovery entry point. `info FILE`, `text FILE` and `inspect FILE` expose different levels of information. Do not assume every subcommand accepts `--help`; the reviewed dispatcher/validators differ from other Craft applications.

`run` accepts `--file FILE` or `--template NAME`, repeated `--cmd 'ID=JSON'`, `--save OUT`, optional `--print` and `--author NAME`. Preserve a working copy and save to a new path unless overwrite was requested.

```sh
wordcraft-cli inspect source.docx
wordcraft-cli run --file source.docx --author "AI copyedit" \
  --cmd 'review.trackChanges={"value":true}' --save review.docx
wordcraft-cli convert review.docx review.pdf --markup
```

The example enables tracking; it does not itself prove that a content edit was made. Make intended edits with discovered text/style commands, inspect them and save again. Omitting `--markup` from PDF/PNG conversion can change whether the review artifacts appear in the rendered delivery. The same option affects comment lists for certain text-oriented outputs.

Formats have directionality. DOC is an import format in the reviewed CLI; DOCX and several open text/document formats support broader exchange. PDF/PNG are rendered delivery paths rather than equivalent editable masters. Retain native editable structure when revisions, fields, comments and styles matter.

`zotero` invokes a separate integration with a running local application. It is not a purely offline converter and can prompt or change citation fields. Do not execute its trace mode on a private document without considering what the trace records. The installed command's accepted options and current Zotero connection must be verified separately.

## Evidence

- [word-cli](https://github.com/storytold/wordcraft/blob/main/apps/wordcraft-cli/src/main.rs)
- [word-mcp](https://github.com/storytold/wordcraft/blob/main/docs/mcp.md)
