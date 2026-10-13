# Selection scope, style inheritance and silent property omissions

**Read when:** applying formatting or changing document structure without unintended global edits.

Read the document structure and relevant text before changing selection. An identical phrase can occur in a heading, table, footnote and body paragraph; choose the intended occurrence and inspect context. A command operating on current selection is not safely reusable after another tool moved the caret.

Character and paragraph properties are partial objects. Omitted fields keep the style-chain value; they do not reset to zero/false. `format.set` uses `props`, and `styles.modify` takes a style ID with optional character/paragraph property objects. Lengths are points, and color representations have specific accepted forms.

The reviewed `CharProps`/`ParaProps` handling can ignore unknown fields. A typo may therefore produce a successful no-op or partial edit. Validate keys against the current documented property list and inspect stored properties and rendered output after applying them. CLI option validation does not imply identical strictness inside these nested objects.

Choose between changing the named style and adding direct formatting. A style change can affect every dependent paragraph; a local formatting change can obscure intended inheritance. Preserve the user's document architecture rather than painting an entire report with repeated per-run properties.

Complex-script and East Asian font properties can differ from Latin properties. Some direct formatting operations mirror size/bold/italic into complex-script fields when not explicitly supplied, while style modifications only change supplied fields. For mixed-language documents verify the actual scripts, glyph coverage, line breaks and direction rather than assuming a single font field covers everything.

After edits, compare extracted text to the requested changes, inspect selection/caret and review paragraph pagination. A visually unchanged paragraph may still carry unintended direct formatting, and an unchanged property dictionary may still render differently under a missing font.

## Evidence

- [word-mcp](https://github.com/storytold/wordcraft/blob/main/docs/mcp.md)
