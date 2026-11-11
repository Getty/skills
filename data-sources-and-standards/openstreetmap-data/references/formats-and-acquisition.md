# Formats, acquisition, and scope

## Choose the smallest adequate source

Start with geographic and thematic requirements. A regional extract often supports an initial application better than a full planet import. However, a region boundary can cut ways or relations; provider extraction rules determine whether dependent objects and crossing features are complete.

Record a source manifest containing the provider URL, retrieval date, snapshot timestamp if available, bounding area, file hash, source format, intended interpretation, and update-feed association. Do not substitute the local download time for the dataset's effective snapshot time.

## Important formats

| Format or source | Typical role | Important distinction |
| --- | --- | --- |
| OSM XML | Readable native objects and debugging fixtures | Large and verbose; use a streaming parser for large files |
| OSM PBF | Compact bulk snapshots and some history products | Binary protocol-buffer-based blocks, not compressed JSON |
| History files | Multiple object versions | Greater scope than a current-state snapshot |
| OsmChange / OSC | Creates, modifications, and deletions | A change document needs a compatible baseline |
| GeoJSON or GeoPackage export | Selected, assembled geographic features | Usually loses native OSM edit structure unless explicitly carried |
| Vector tiles | Display-oriented features by tile and zoom | May simplify, clip, omit attributes, and repeat features |

PBF supports block-based decoding and compact representation of repeated strings and coordinates. Use maintained libraries or tools rather than implementing the binary format casually. Compression ratio does not directly predict the size of a spatial index, relational import, or derived geometry store.

A snapshot, an extract, a full-history file, and a replication stream answer different questions. Verify which product was downloaded before promising historical reconstruction.

## APIs and bulk data

The editing API is designed around OSM's editing data model. Overpass supports queries over OSM data with its own language and instance limits. Nominatim resolves names and addresses. A tile endpoint returns a presentation product. None is an interchangeable replacement for bulk extracts.

For a recurring broad query, first evaluate extracts and local processing. For a bounded exploratory query, an appropriate API may be enough. Review the selected endpoint's documented policy and availability instead of assuming unlimited bulk extraction.

Regional providers such as Geofabrik publish extracts and related update information. Check the selected region's current page and feed metadata. Do not combine a timestamp from one provider with a sequence number from a different replication system.

## Processing tools and dependencies

Osmium Tool provides established commands for inspecting, filtering, extracting, and applying changes. Other tools can import OSM into databases or specialized indexes. Select a tool by supported input, relation handling, update semantics, and output requirements.

A tag filter is only part of extraction. If a selected way needs untagged coordinate nodes, those nodes are support data. If a selected administrative relation crosses the boundary, the selection may need geometry outside that boundary. Understand the tool's reference-completion behavior and verify the resulting file.

When storing only assembled geometries, retain enough source state or a rebuild mechanism to refresh them. Otherwise a later node edit may be impossible to apply correctly.

## Estimate from representative data

Measure at least input bytes, retained objects by type, dependency expansion, assembled geometry count, invalid or incomplete geometries, index size, build duration, and typical query latency. Estimate larger regions from comparable density and feature mix, and state the uncertainty.

No single RAM requirement follows from “uses OSM.” A tile archive reader, a regional geocoder, a bulk filter, and a global routing engine have different working sets. Avoid transporting sizing advice from one product to another.

