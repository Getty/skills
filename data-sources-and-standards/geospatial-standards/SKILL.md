---
name: geospatial-standards
description: "Use when exchanging, querying or validating geodata — coordinate reference systems, axis order, WKT and WKB, OGC Simple Features, GeoJSON, GeoPackage, GeoParquet, GeoSPARQL, OGC API Features, containment and distance queries."
---

# Geospatial Standards

Use this skill to connect geographic meaning, coordinate systems, geometry, exchange formats, and query interfaces. A format can carry coordinates correctly while the application still misinterprets their axis order, location role, measurement units, or time.

Start from the question the user needs to answer. Finding a place name, testing containment, measuring distance, displaying a map, and computing a transport route are distinct operations.

## Working procedure

1. **Identify the geographic object.** Distinguish the real-world feature from its geometry and from a label or address. Decide whether the task concerns a representative point, entrance, footprint, boundary, route, or coverage.
2. **Establish the reference system.** Record CRS, axis order, units, dimensionality, and coordinate epoch or vertical datum when relevant. If unknown, retain the uncertainty instead of guessing.
3. **Choose the representation.** Select a geometry model and an exchange format based on fidelity, size, update pattern, software compatibility, and the need for attributes or multiple geometries.
4. **Define the spatial predicate.** State what “inside,” “near,” “intersects,” or “distance” means, including boundary behavior and measurement model.
5. **Validate at several levels.** Check syntax, format requirements, geometry validity, CRS consistency, and domain plausibility. A parsed file is not proof of all five.
6. **Separate source and derivation.** Preserve source geometry, timestamps, transformation parameters, and any repair or simplification. Distinguish observation time from file creation time.
7. **Check implementation support.** Verify the exact specification edition and advertised conformance. Do not assume every RDF store implements GeoSPARQL functions or every API supports CQL2.
8. **Return a reproducible result.** Include source generation, units, boundary policy, uncertainty, and a small example that exposes likely coordinate mistakes.

## Reference map

- Read [concepts and coordinate systems](references/concepts-crs.md) before interpreting coordinates, accuracy, or transformations.
- Read [geometry and queries](references/geometry-and-queries.md) when selecting containment, intersection, distance, or indexing behavior.
- Read [exchange formats](references/exchange-formats.md) to choose GeoJSON, WKT/WKB, GeoPackage, or GeoParquet.
- Read [GeoSPARQL](references/geosparql.md) when representing geography in RDF or querying spatial RDF.
- Read [feature APIs](references/features-apis.md) when discovering or consuming OGC services.
- Read [worked examples](references/examples.md) for original GeoJSON, RDF, and query illustrations.
- Read [primary sources and version notes](references/sources.md) before claiming current standard or implementation support.

## Standards and implementations

A standard defines a contract. An implementation may support only part of that contract or add extensions. PostGIS, GDAL, PROJ, spatial libraries, and RDF engines are implementation choices; they are not requirements of every geographic data model.

Use precise names: GeoJSON is an interchange format; GeoPackage is a standardized SQLite-based container; GeoParquet adds geospatial conventions to Parquet; GeoSPARQL defines an RDF vocabulary and spatial query capabilities; OGC API Features describes access to geographic features.

## Essential interpretation rules

- A feature can have several geometries for different purposes and times.
- Assigning a CRS changes metadata; transforming coordinates changes coordinate values according to a defined operation.
- Geographic angular coordinates are not meter distances.
- GeoJSON coordinate arrays use longitude before latitude under RFC 7946.
- CRS authority axis order and a software API's coordinate convention must both be checked.
- A point on a boundary may need a different predicate from a point strictly inside.
- An index returns or accelerates candidate selection; exact spatial semantics still matter.
- Geometry precision, positional accuracy, and source completeness are different quantities.
- A displayed map, geocoded address, or road route is not evidence of ownership or actual commercial movement.

Provide implementation code only to the extent needed by the request. Clearly label synthetic data, illustrative queries, and execution limits.
