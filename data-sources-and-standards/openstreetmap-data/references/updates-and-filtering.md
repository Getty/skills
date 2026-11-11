# Updates, filtered projections, and recovery

## Define the state contract

Decide whether the output represents the latest known snapshot, a sequence of immutable snapshots, or a historical archive. A file containing one version per object cannot answer arbitrary historical questions.

A useful generation manifest records source identity, baseline timestamp or sequence, highest applied sequence, interpretation profile version, checksums, build time, and completeness checks. The manifest is a suggested application convention, not part of the OSM standard.

Replication feeds commonly publish sequential change files and state information. Sequence numbers identify positions in their own feed. A daily sequence is not a minute sequence, and a regional provider may have its own sequence space and clipping rules.

## Apply changes with a compatible baseline

1. Obtain a snapshot and its documented replication position or coverage.
2. Preserve changes needed to bridge snapshot creation through import completion.
3. Apply creates, modifications, and deletions in the feed's defined order.
4. Update source objects and invalidate dependent derived features.
5. Validate a complete generation before exposing it to readers.
6. Persist the checkpoint only when the related state is durable.

A version guard helps prevent replay from overwriting a newer source object with an older one. It does not fix an unobserved change gap or a baseline associated with the wrong feed.

Deletion must remove active derived records and stale lookup entries. If historical or audit use is required, retain a tombstone or history entry separately. Never infer deletion just because an object is absent from an arbitrary clipped extract.

## Maintain dependency information

A selected road way depends on coordinate nodes. A selected multipolygon may depend on several ways and their nodes. Keep reverse dependency information such as node-to-ways and member-to-relations, or use a proven importer's equivalent mechanism.

If a node moves, rebuild all affected geometries even if their own source versions did not change. If tags change, reevaluate selection and normalized fields. If a relation gains or loses a member, update both geometry and dependency records.

Separate source revisions from projection revisions. A single source change can create several updated derived features; an interpretation-profile change can rebuild projections without any new OSM edit.

## Filter changes are a first-class case

A system that listens only for already-retained object IDs cannot discover an object that newly acquires a relevant tag. It can also miss a new dependency outside the initial selection.

Choose an explicit strategy:

- keep broader source state and derive narrow outputs;
- inspect the relevant broader change stream and fetch missing dependency state;
- periodically rebuild the filtered set from a compatible extract.

State the trade-off in storage, processing, latency, and completeness. “Incremental updates supported” is insufficient without an entry/exit policy for the selection.

Changes to the filtering profile may require backfill. If all chemical facilities were discarded, a new profile asking for them cannot recover the past snapshot from the reduced output alone.

## Publishing files consistently

Immutable output generations are straightforward: build all shards and indexes for generation G, validate them, then atomically publish a manifest pointing to G. Readers pin a generation for the duration of a batch.

An overlay or log can reduce rewriting, but then lookup must define version ordering, tombstones, duplicate handling, compaction, and the relation between base and overlay. A compressed data file alone provides neither random lookup nor update semantics.

For geographically split files, address features crossing shard boundaries. Stable source keys and a documented primary location help prevent duplicate counting. Dependency geometry can extend outside the shard that owns the logical feature.

## Recovery and acceptance checks

Detect unavailable sequences, incompatible snapshots, corrupt downloads, and unresolved dependencies. Do not label a projection current when a feed gap remains. Recover from a verified checkpoint or perform a controlled rebuild.

Exercise at least these cases: moving a shared node, removing a tag that selected a feature, adding a newly relevant feature, changing relation membership, deleting an object, replaying a change, and rebuilding under a changed profile. These checks validate data behavior, not merely that a parser accepts the file.

