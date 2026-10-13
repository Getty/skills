# Page indexes, displayed geometry and existing-text edits

**Read when:** rotating/reordering pages, placing annotations or editing existing text and artwork.

Pages and positional selectors in the automation table are one-based. Geometry is expressed in PDF points from the top-left of the displayed page, not an assumed bottom-left unrotated PDF coordinate space. Page rotation and display scaling affect coordinate conversion; inspect the displayed bounds before applying a rectangle derived from a screenshot.

Track page identity through reorders, deletions and insertions. A saved ordinal from before a page move can now refer to a different page. Reinspect the page count/order/labels and use a small preview after each structural operation. A single successful rendering of page 1 does not validate the rest of a document.

`object_list` returns recognized page objects with generation-scoped kind/index references. `object_move` can atomically move a bounded set and optionally check the generation. Do not reuse those references after another edit invalidates the object generation. Preserve source text bytes/fonts when the tool promises that behavior, rather than replacing the whole page with an image.

## Existing text is not a word-processing paragraph

Text editing depends on source font resources, subset glyph coverage and measured layout. `text_font_files`, `text_font_import` and `text_fonts` discover/import/list appropriate faces. `text_edit.font_resource` chooses a resource; `text_edit_layout` can measure a draft before committing. Installing a similarly named font does not establish identical metrics or the missing glyphs needed by an existing subset.

`text_edit.ranges` uses disjoint UTF-8 byte ranges. Do not pass Python character indexes, JavaScript UTF-16 indexes or an assumed page-index base as text offsets. Resolve the exact range endpoint convention from the current schema and compute byte boundaries from the exact source text. Refresh text and its generation before applying a second replacement.

After editing, extract the text again, inspect the affected object's bounds and render the region. Text appearance, extraction order and document accessibility are separate acceptance dimensions.

## Evidence

- [pdf-automation](https://github.com/storytold/pdfcraft/blob/7163ba3dee8becfff6871c9a65d0d8314314742b/crates/automation/README.md)
