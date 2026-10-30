# End-to-end recipes

Domain-specific traps per task type. The general rules live in the topic references.

## Product catalog

Prefer an approved export or API. Otherwise inspect listing responses, JSON-LD and detail pages across variants, and define product, offer and variant identity before deduplicating. Discover through listings; fetch detail pages only for missing fields. Compare a deterministic plan with a small LLM sample when descriptions vary.

A bare number is not a price: record currency, tax inclusion, unit, seller, availability and observation time where requested. Keep discounted, old, range and subscription prices apart, and an unavailable price distinct from zero. Never infer currency from the user's country or a lone symbol. Check duplicate variants and cross-record price attribution. Resolve conflicts by field evidence, not by a majority vote among models. Accept against a known ID inventory or reliable listing total; otherwise report the discovered set with its coverage uncertainty.

## Documentation to a RAG corpus

Pin version, language, canonical candidate and path scope; discover through sitemap or navigation. Capture headings, code blocks, tables, warnings and links, and compare Markdown with the rendered source on table-heavy pages before choosing a content filter. Keep versions and languages apart where meaning differs. Hand the documents to ingestion for chunking and retrieval evaluation. A successful vector-store import says nothing about a missed section: measure acquisition coverage and content retention separately.

## Events or job listings from heterogeneous pages

Fix field semantics first: start versus publication date, local time versus UTC, salary amount versus range, organization versus location. Extract raw date and range expressions with evidence and resolve them only when context gives a unique reading. Use template selectors where a layout group allows, schema-constrained LLM extraction for variable prose. Deduplicate by stable source IDs or explicit matching rules, never by similar titles alone. Keep cancelled or closed records as status observations. Gold samples need missing locations, multiple dates, recurring events and ambiguous ranges. Personal data: [privacy and rights](privacy-and-rights.md).

## Price or content monitoring

A change is a business event, not a byte difference: compare normalized field values with source time and hash, and suppress dynamic banners only through a tested transform. Never emit a price-drop event because a failed extraction became null. Use idempotent event keys and confirmation rules for noisy sources. Build a reusable command first; configure a schedule or notification only when asked, through an available authorized mechanism. Asking how to monitor a site is not a request for paid recurring jobs or messages to others.

## JavaScript directory with virtualized rows

Look for an authorized response carrying record IDs and cursors first. Otherwise collect rows as they appear, since virtualized rows leave the DOM, and stop on verified exhaustion, repeated state, budget expiry or access failure ([browser automation](browser-automation.md)). Record filters and sort order. Turn the repeated interaction into deterministic code; keep an agent fallback only for exceptional layouts and verify its final state independently.

## Tables from scanned documents

Keep original files and page images with hashes; keep coordinates and table structure through OCR, and use a model only where the parser leaves ambiguity. Validate totals, units, row alignment, negative signs, merged cells and footnotes against the image, and keep unknown cells unknown. Evaluate a hand-labeled sample before a large archive; a clean spreadsheet can still hold misaligned rows.

## Repair an existing scraper

Reproduce on retained snapshots, locate the failing stage, and compare the last good with the first bad snapshot ([troubleshooting](troubleshooting.md)). Make the smallest change that fixes the observed failure, add a fixture for the changed layout, and replay existing variants to catch silent field swaps and lower recall. Deploy with a canary and a rollback point; never fix a selector by dropping the records it misses.

## Choose a stack for a new project

Run the same URLs and saved snapshots through two or three plausible approaches and report the winner for this workload only, not as a universal ranking. Pilot measures: [tool selection](tool-selection.md).
