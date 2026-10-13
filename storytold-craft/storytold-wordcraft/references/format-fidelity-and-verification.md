# Editable-versus-rendered delivery checks

**Read when:** exporting documents or deciding whether a conversion preserved the required semantics.

Choose the editable deliverable independently from the visual proof. DOCX/ODT/RTF/HTML/Markdown/TeX/plain text do not preserve identical structures; a PDF preserves a reading appearance rather than the same editing model. Report intentional losses such as flattened fields, removed comments, simplified tables or changed styles.

For text correctness, extract the saved/reopened output and compare the intended changes, not just the word count. For structural correctness, inspect paragraphs, styles, tables, sections and relevant fields/revisions. For visual correctness, render every page and inspect small text, page breaks, headers/footers, lists and tables. These three gates are complementary.

A missing font can alter pagination even when every character is still present. Match the rendering environment or explicitly accept a replacement; never claim pixel-identical output merely because the family name remains in the document. Do not include system font binaries in a delivery bundle.

After a failed batch or connection loss, inspect the live document and saved file separately before retrying. An operation that toggles a formatting/review state is not naturally idempotent. Restore from a checkpoint when the exact partial mutation cannot be determined safely.

Return an honest validation record: which formats were reopened, which pages inspected, whether tracking/comments were preserved, what could not be tested, and which warnings remain. Successful conversion alone is not a complete document review.

## Evidence

- [word-cli](https://github.com/storytold/wordcraft/blob/main/apps/wordcraft-cli/src/main.rs)
- [word-mcp](https://github.com/storytold/wordcraft/blob/main/docs/mcp.md)
- [wordcraft-readme](https://github.com/storytold/wordcraft/blob/main/README.md)
