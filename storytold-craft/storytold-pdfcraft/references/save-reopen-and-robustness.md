# Save semantics and PDF acceptance gates

**Read when:** committing edits or testing a heterogeneous PDF corpus.

`doc_save` writes atomically; an in-place save is incremental, while a new path writes a full document. `doc_close` refuses to drop dirty changes unless discard is explicit. Preserve these distinctions in recovery logic: dirty state, a queued client response and a durable file are different facts.

After a generic batch failure, earlier successful changes remain. Read document summary, dirty/history state and per-step results. Do not retry page moves, deletes or comment insertion without checking whether the previous call completed. For a new-path delivery, reopen it in a fresh document and compare page count, labels, bookmarks, form values, annotations and required metadata.

`check` runs each file's open/inspect/render work in a separate child process with a wall-clock limit. This is useful for finding hangs or crashes without losing the whole corpus run. Its success is robustness evidence at the chosen rendering settings, not proof of typography, signature validity, accessibility or data preservation. Record failed files and timeouts separately from content-validation failures.

Bound extraction and rendering for large/untrusted PDFs. Start with metadata and selected pages; expand coverage deliberately. Prefer native text extraction over OCR when real text exists. OCR is an additional interpretation step, not a guarantee of exact text; retain the original and report uncertain recognition where material.

Maintain an output manifest with input/output hashes, page-selection/rotation decisions, tool/schema snapshot, actual warnings and checks performed. Do not write passwords or unredacted extracted text into broadly shared logs. Export images can themselves contain the confidential content being reviewed.

## Evidence

- [pdf-cli](https://github.com/storytold/pdfcraft/blob/7163ba3dee8becfff6871c9a65d0d8314314742b/apps/pdfcraft-cli/src/main.rs)
- [pdf-automation](https://github.com/storytold/pdfcraft/blob/7163ba3dee8becfff6871c9a65d0d8314314742b/crates/automation/README.md)
