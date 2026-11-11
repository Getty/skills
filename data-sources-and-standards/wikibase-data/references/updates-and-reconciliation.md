# Updates, lifecycle changes, and reconciliation

## Choose one update contract deliberately

RecentChanges API and the general recent-change EventStreams feed primarily notify consumers about edits and log events. They do not normally contain the full canonical new entity content or a directly applicable RDF diff. Filter for the intended repository, namespaces, entity types, and event kinds, then fetch or reconcile the appropriate entity revision according to the contract.

Dedicated WDQS RDF streams carry import, diff, delete, and reconcile operations. Verify current stream discovery, subgraph, schema, and serialization; these differ from general edit notifications. Entity-owned triples and linked/shared triples need different handling: deleting one entity must not remove triples still used by another. Entity deletion can require locating owned triples absent from the payload. Reconciliation can replace previously received entity state.

Some events span multiple chunks. Buffer all `sequence` positions from zero through `sequence_length - 1`, check consistent `meta.request_id` and chunk counts, parse and combine each RDF payload field, then apply the complete event. Do not checkpoint a partially reconstructed event; retain incomplete buffer state durably or replay it. Batch files require grouping chunks by request ID. Per-entity ordering does not establish global ordering across entities.

## Bridge the baseline and stream

Define the baseline's guaranteed validity boundary and begin retaining updates with sufficient overlap before it. Apply the baseline, replay the retained changes, then catch up to a recorded position. Deduplicate by source event identity and version semantics. Keep retrieval and application idempotent because retries and overlapping windows can deliver the same change again.

RecentChanges can insert records slightly out of timestamp order; overlap polling windows and persist continuation state. Stream offsets or event IDs are not interchangeable with entity revision IDs. Avoid committing a checkpoint before the corresponding entity state is durably applied. If the implementation cannot atomically persist both, design a replay-safe handoff and document it.

Verify actual retention for the selected API or stream. It is finite and can differ by stream/configuration. Detect when the oldest required change is no longer available. Do not silently resume “from now” and claim continuity; obtain a newer baseline or perform an adequate reconciliation. Periodically compare selected entities against authoritative current data to catch gaps and operational errors.

## Preserve lifecycle events

Record redirects and merges as source lifecycle changes, retaining the original identifier and observed target. Resolve redirect chains carefully, detect loops, and keep historical snapshots interpretable. Do not replace every old identifier globally without considering historical evidence and external references.

Treat deletion, restoration, and suppression separately from a failed fetch. A timeout, forbidden response, unknown endpoint, or transient missing response is not sufficient evidence of deletion. Preserve a tombstone or lifecycle record when supported by authoritative evidence. Do not erase historical provenance solely because the current source disappears; apply the actual retention and access policy.

Define handling of out-of-order revisions. A delayed event should not downgrade a known newer snapshot. If only current entity fetching is used, explicitly accept that intermediate revisions may be skipped; this maintains current state but does not reconstruct complete history. If every revision matters, acquire the specified revision and handle unavailable or suppressed versions explicitly.

## Keep filtered subsets correct

An entity can enter or leave the selection when a property changes. A class hierarchy change can affect many entities that were not directly edited. Track the dependency of the selection on properties, linked entities, and hierarchy closure. Refresh membership when those dependencies change; filtering only events for already-selected IDs is insufficient for a growing subset.

Export-format changes can alter RDF without a source entity revision change. Keep representation version and transformation version in the reconciliation key, and support rebuilds when needed. Do not conflate “same revision” with “same serialized export under all software versions.”

Consult [RecentChanges](https://www.mediawiki.org/wiki/API:RecentChanges), [EventStreams](https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams_HTTP_Service), [Streaming Updater](https://wikitech.wikimedia.org/wiki/Wikidata_Query_Service/Streaming_Updater), and [Public Update Stream](https://wikitech.wikimedia.org/wiki/Wikidata_Query_Service/Streaming_Updater/Public_Update_Stream). The checkpointing and subset-maintenance strategies here are implementation guidance, not an exactly-once delivery guarantee.
