# Redaction, sanitization and accessibility evidence

**Read when:** removing confidential information or preparing a security/accessibility-sensitive deliverable.

## Redaction requires removal, not appearance

A black rectangle, hidden text, an annotation or a screenshot with an obscured area is not evidence that underlying data is removed. Discover the actual redaction/sanitizing task tools and schemas from `tools`/`tool_search`; do not imitate a redaction using drawing commands. Review the exact targets before applying irreversible removal.

The application can save in place incrementally, retaining previous bytes. Therefore an in-place save must not be assumed to remove earlier secret content. A new-path/full rewrite is an important persistence distinction, but even a full rewrite does not establish that all relevant content was correctly targeted. Verify the saved artifact independently: extracted/searchable text, comments/forms, metadata, embedded files/images and any other applicable content locations.

Use `pdfcraft-cli audit FILE.pdf` as a detector for faux redactions, not as a comprehensive secrecy proof. Reopen and inspect the actual delivery, not only the working in-memory document. Keep originals in a separate private location and do not bundle an unredacted original alongside a supposedly sanitized public artifact.

## Sanitizing is broader than page text

Choose which metadata, annotations, embedded resources, form data and scripts may remain. The correct policy depends on the user's purpose. Obtain approval for destructive removals and retain an internal change record without copying the removed secrets into that record. Visual inspection alone is inadequate.

## Accessibility review is evidence, not certification

`accessibility_review_record` compares separately opened original and edited documents, writes a JSON record with hashes/rule statuses and reports unresolved/manual-review findings. It does not certify accessibility. Keep a stable original open while editing the second document. Automated rule success does not replace review of reading order, meaningful labels or whether an image description communicates the actual content.

Return explicit verification scope and unresolved checks. Avoid absolute claims such as “all confidential content removed” or “fully accessible” when only a subset of channels/rules was tested.

## Evidence

- [pdf-cli](https://github.com/storytold/pdfcraft/blob/7163ba3dee8becfff6871c9a65d0d8314314742b/apps/pdfcraft-cli/src/main.rs)
- [pdf-automation](https://github.com/storytold/pdfcraft/blob/7163ba3dee8becfff6871c9a65d0d8314314742b/crates/automation/README.md)
