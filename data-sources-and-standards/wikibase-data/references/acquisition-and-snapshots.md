# Acquisition and reproducible snapshots

## Select an access method by workload

| Workload | Starting point | Important limit |
| --- | --- | --- |
| Known, bounded entity IDs | Entity JSON, Action API, or a supported REST endpoint | Response formats and revision support differ |
| Find candidates by labels | Documented search API | Search results are candidates, not identity proof |
| Find entities by graph patterns | Bounded WDQS query | Service limits, index lag, and endpoint dataset scope |
| Large reproducible import | Dated JSON or full RDF dump | Download, format, completeness, and update coverage |
| Lightweight direct values | Explicit truthy export/query | Qualifiers, references, and non-best ranks are lost |
| Continuous maintenance | Change acquisition plus reconciliation | Finite retention and source lifecycle semantics |

Use current [data-access guidance](https://www.wikidata.org/wiki/Wikidata:Data_access) to select the endpoint. Do not assume the canonical entity JSON, Action API envelope, and REST response are interchangeable. Verify the live API's documented contract and supported entity types. Prefer stable public interfaces over scraping rendered entity pages.

For revision-specific entity data, the linked-data interface documents a `revision` parameter, for example `https://www.wikidata.org/wiki/Special:EntityData/Q42.json?revision=112`. This URL illustrates the parameter syntax; it does not guarantee the example revision is currently retrievable. Cache successfully acquired immutable revisions and record the returned entity and revision, including redirect behavior.

## Capture acquisition separately from content

Record the requested repository/entity/revision, actual response identity, HTTP status, acquisition time, representation, content hash, and available source version metadata. Keep retries and retrieval observations separate from a logical entity snapshot. A hash is a local content identifier, never a substitute upstream revision number.

Keep requested languages, selected components, and other filters in the acquisition contract. Otherwise a later consumer may mistake a partial response for a complete entity. Preserve unknown fields in the raw response even if the normalized model does not expose them yet. Re-encoding JSON preserves parsed information only to the parser's capabilities; it does not preserve original bytes or object ordering.

Honor descriptive User-Agent requirements, caching, backoff, and Retry-After. Bound concurrency and use documented API batching where supported. Do not scatter millions of per-entity requests across a public endpoint to reproduce data already available in a dump.

## Stream dumps with explicit framing

The canonical JSON dump contains an outer JSON array, with entity objects arranged one per line. It is not generic JSON Lines without the array framing and separators. Inspect a sample and use a parser or line-handling strategy that accounts for the opening/closing brackets and commas. Do not load the full dump into memory, assume entity-ID ordering, or truncate data at arbitrary compressed offsets without a resumable framing plan.

Preserve dump URL, date, checksum, compression, parser version, entity types, and included namespaces. JSON and RDF are documented stable interfaces; embedded JSON inside historical XML dumps is not the same stable canonical contract. Choose a supported representation deliberately.

A dump need not represent every entity at one common instant. Use documented validity metadata and per-entity revisions to establish an update baseline. The RDF dump header's `schema:dateModified` describes a validity boundary, while `schema:softwareVersion` describes the export format. Do not use the download's completion time as the earliest necessary update time.

## Make results reproducible

Retain a source manifest and an immutable configuration of all filters and mappings. Checkpoint bounded completed work with the exact dump identity. If parsing fails, retain the failing source location and error, and distinguish partial completion from success. Make a repeated batch produce the same logical result.

Follow [database-download guidance](https://www.wikidata.org/wiki/Wikidata:Database_download), [API documentation](https://www.mediawiki.org/wiki/Wikibase/API), and the [Stable Interface Policy](https://www.wikidata.org/wiki/Wikidata:Stable_Interface_Policy). Resource sizing and throughput depend on measured inputs and chosen tools; this skill makes no hardware promises.
