# Geographic feature APIs and service discovery

## OGC API Features

OGC API Features defines access to geographic feature collections through web interfaces. The Core standard covers discovery and access; additional parts add capabilities such as alternative coordinate reference systems or filtering. Part 1 Core 1.0.1 is a published corrigendum baseline.

Begin with the landing page and follow links. Inspect the advertised conformance declarations, collection metadata, available representations, and links to items. Do not construct every URL from assumptions about a particular server's path layout.

A typical workflow is:

1. discover the API and its conformance classes;
2. inspect collections and select the relevant one;
3. inspect spatial and temporal extent, CRS, schemas or queryables where available;
4. request a bounded subset using supported parameters;
5. follow pagination links until the intended result scope is complete;
6. preserve feature identifiers and source metadata.

A parameter can be valid in one extension and unsupported in Core alone. CQL2 filtering is not universally available just because an endpoint advertises OGC API Features. Check filter languages, queryable properties, and extension conformance.

## Bounding boxes and temporal filters

A bounding-box filter is a useful initial constraint, but its exact interpretation and coordinate reference system must be read from the selected API profile. Do not assume arbitrary projected coordinate arrays are accepted.

A temporal filter applies according to the API's temporal model. A collection's extent, a feature's phenomenon time, and the server's update time are different concepts.

Pagination matters for correctness. A successful first response may contain only a subset. Follow server-provided next links and record any limits, truncation, or changing dataset state. If a multi-page request needs a consistent snapshot, determine whether the service offers one.

## Feature services versus map services

Feature access returns structured geographic objects and attributes. A rendered map service returns images for presentation. Tile services organize content by tile grids and zoom levels. Their outputs are not interchangeable.

WFS belongs to an earlier OGC feature-service family with its own versions and capabilities. WMS focuses on map portrayal. WMTS describes tiled map access. Evaluate the actual version and operations instead of treating all OGC services as one protocol.

A tile response may omit attributes, simplify geometry, or duplicate clipped features across tiles. It can be useful for display and unsuitable as the only source for analytical counting or precise boundary assessment.

## Schema and identity

A server's collection ID, feature ID, external business identifier, and feature type name serve different purposes. Preserve them without assuming they identify the same real-world entity.

If an API provides a schema or queryables definition, use it to interpret field types and supported filters. Unknown or additional properties should be handled according to the application contract. Do not automatically map every property name to an ontology predicate with a claimed standard meaning.

Collection-level metadata is not necessarily provenance for each individual assertion. If records originate from several sources, retain per-record or per-field provenance where available.

## Practical client behavior

Use advertised media types, bounded requests, pagination, and appropriate caching. Observe the selected service's usage policy. Record API version, collection, request parameters, and retrieval time for reproducible exports.

Treat network retries and service availability separately from data completeness. A retryable transport failure should not silently become an empty collection. If filters or conformance are unclear, return a limited result with an explicit capability statement.

An OGC API interface does not dictate the server's database, and supporting spatial SQL locally does not automatically implement the API contract.

