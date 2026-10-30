# Content and document harvesting

## Keep useful representations

Retain original bytes when allowed, a decoded/rendered view when different, and the exact text or image that supplied evidence. Version and hash each transformation; a transformed-text hash is not the HTTP body's hash.

| Representation | Useful for | Commonly lost |
| --- | --- | --- |
| Raw HTML | Reprocessing, source markup, metadata | Later responses/rendered state |
| Rendered DOM | Dynamic text and associations | Virtualized rows, canvas |
| Markdown/article text | Reading and language models | Tables, variants, footnotes |
| JSON/API response | Typed records and source IDs | Selected UI interpretation |
| Screenshot | Canvas and visual evidence | Offscreen content, precise text |
| Document model | Tables, pages, reading order | Parser-dependent failures |

Before scaling, compare source pages with transformed views, tables and missing fields included.

## Extract structured source data

Prefer documented exports and response JSON over presentation parsing, keeping cursors and IDs. A request seen in the browser is not necessarily a stable API.

Parse JSON-LD without `eval`, handling arrays, `@graph`, multiple types, and `@id` references; use a JSON-LD processor when expansion or graph merging matters, with remote-context loading disabled or controlled. A recursive property search is not a JSON-LD implementation. [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/)

Compare structured data with visible content and record conflicts instead of picking the convenient value. Keep offer currency, seller, validity, and product association across variants and aggregate offers. [Product](https://schema.org/Product), [Offer](https://schema.org/Offer), [AggregateOffer](https://schema.org/AggregateOffer)

Keep table header hierarchy, row labels, units, captions, and notes; expand row/column spans deliberately. Never flatten cells into prose for a model to reconstruct.

## Preserve meaning during cleanup

Decide which fields matter before removing boilerplate; shipping terms, currency, timezone, tax notes, and footnotes often sit outside the main region. Check that article extraction (e.g. Trafilatura's precision/recall modes) keeps the requested fields. [Python usage](https://trafilatura.readthedocs.io/en/latest/usage-python.html), [troubleshooting](https://trafilatura.readthedocs.io/en/stable/troubleshooting.html)

Chunk by complete item, table group, section, or region before token counts, carrying heading and unit context into each chunk. Keep offsets bound to one immutable representation with declared units ([extraction contracts](extraction-contracts.md)); deduplicate overlap and mark truncated records partial.

## Documents and visual content

Route PDFs, office files, and spreadsheets to suitable parsers and check for a text layer before OCR. Keep page and region evidence and table structure. Evaluate the parser, e.g. [Docling](https://docling-project.github.io/docling/), on the actual source types.

Use OCR/vision only when the information is visual or missing from retained text, keeping image dimensions, crop, viewport, and scroll context. Verify ambiguous digits, signs, decimal separators, and merged cells. A screenshot captures a view, not the page inventory.

Bound download size, decompression, parser time, and memory; check file signatures; parse untrusted documents in isolated workers without running scripts or macros.

## Downstream corpus

Store document ID, source URL, canonical candidate, language, source version, fetch time, content hash, sections, and access/retention metadata, with document identity separate from observations. Deduplicate exact content while keeping lineage; near-duplicates are only candidates, since language, currency, edition, or tenant views differ.

Track changed, removed, blocked, and temporarily unavailable sources separately; never delete indexed content because one refresh timed out, and propagate confirmed removals under policy. Hand clean records and lineage to ingestion; chunking, embedding, retrieval evaluation, and answer faithfulness are separate stages.
