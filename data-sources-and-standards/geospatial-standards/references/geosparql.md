# GeoSPARQL: spatial semantics in RDF

## Purpose and scope

GeoSPARQL is an OGC standard connecting geographic information with RDF and SPARQL. Version 1.1 defines a core vocabulary, geometry representations, topological relations, functions, and several conformance modules. It does not require every RDF store to become a complete geographic information system.

Separate three capabilities when evaluating an engine:

- storing RDF terms from the GeoSPARQL vocabulary;
- executing geometry functions over supported literals;
- deriving or rewriting topological relations according to supported entailment and query-rewrite behavior.

An engine may support the first and not the others. State the tested module, geometry serialization, CRS, and function coverage.

## Features and geometries

A `geo:Feature` is distinguished from a `geo:Geometry`. A feature can link to multiple geometries using `geo:hasGeometry`; `geo:hasDefaultGeometry` identifies a default for applicable operations.

Separate geometry resources allow different representations, roles, times, and provenance. For example, a physical site can have a footprint and a representative point. Do not attach several unqualified coordinate strings and assume a query will select the intended one.

Geometry serialization properties, including `geo:asWKT`, point to typed literals. The `geo:wktLiteral` datatype gives the lexical string a specific interpretation. A plain string that happens to look like WKT is not the same RDF term.

## Coordinate reference systems

A GeoSPARQL WKT literal can start with a CRS IRI in angle brackets. With no explicit CRS, the GeoSPARQL WKT profile defaults to CRS84. Preserve the declared CRS and follow its coordinate-axis interpretation.

Use explicit CRS84 in introductory examples so longitude/latitude ordering is visible. Check engine support before mixing coordinate systems; do not assume every implementation automatically performs the needed transformations.

Units are part of function signatures where the standard requires them. A distance query should specify a supported unit IRI and verify how the engine interprets coordinate systems and dimensionality.

## Relations and functions are different

A triple such as `featureA geo:sfWithin featureB` is an RDF assertion. A filter using `geof:sfWithin` calculates a relationship from supplied geometry literals when the implementation supports that function.

The existence of geometry triples does not guarantee that all corresponding topological relation triples have been materialized. Conversely, an asserted relation may come from a source or previous calculation that should be examined separately from current geometry.

Inference and query-rewrite modules can connect vocabulary relations with geometry operations, but their support must be established. A generic SPARQL endpoint may simply treat the function IRI as unsupported.

## Provenance and time

A spatial relationship can be derived from two geometry versions using a particular operation. Keep the source versions, calculation time, CRS and boundary policy, and any repair or transformation used.

An organization's facility can be inside an area without the organization itself having that area's polygon as its geometry. Model the organization-to-site relationship separately from site-to-area topology.

GeoSPARQL supplies spatial representation and operations. It does not by itself settle disputed borders, establish legal jurisdiction, or supply the validity dates of boundaries. Those require domain assertions and sources.

## Implementation checks

Parse the RDF first, then execute a minimal supported function query. Test a point inside, outside, and on a polygon boundary. Test the chosen serialization and CRS explicitly. If the engine rejects a function, report the unsupported capability instead of rewriting the result as though the standard had been evaluated.

For interoperability, preserve original geometry values and record any converted representation. Only claim conformance to the modules and edition actually verified.

