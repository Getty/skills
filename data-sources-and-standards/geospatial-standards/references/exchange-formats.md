# Choosing an exchange format

## Match the contract to the workload

| Representation | Suitable use | Main checks |
| --- | --- | --- |
| GeoJSON | Web interchange and readable feature examples | Longitude/latitude, geometry nesting, RFC 7946 rules |
| WKT or WKB geometry | Compact or textual geometry interchange | Geometry dialect, dimensions, CRS supplied separately or by profile |
| GeoPackage | Portable spatial datasets in one database file | Required tables, geometry encoding, declared extensions |
| GeoParquet | Columnar analytics and large feature batches | Version, geometry encoding, CRS, metadata, reader support |
| RDF with GeoSPARQL | Linked entities, spatial vocabulary, RDF queries | Geometry datatypes, CRS IRIs, engine conformance |

A container or serialization does not decide identity, ownership, provenance, or real-world completeness. Preserve those as application data.

## GeoJSON: RFC 7946

GeoJSON defines geometry objects, Features, and FeatureCollections. Features carry a geometry, properties, and optionally an identifier. A null geometry is allowed. Use the standard geometry nesting rather than an application-specific list of coordinates called GeoJSON.

Coordinates follow WGS 84 longitude/latitude in decimal degrees; the older arbitrary `crs` member does not restore general projected-CRS support in RFC 7946. Transform a projected source before emitting conforming coordinates.

Closed polygon rings, exterior/interior ring structure, winding rules, and antimeridian behavior matter. An antimeridian-spanning bounding box cannot always be interpreted by assuming the west longitude is numerically less than the east longitude. Readers are advised not to reject polygons solely for older winding conventions.

Foreign members can carry application metadata, but they do not redefine the standard members. Keep feature IDs stable and distinguish them from array position.

## WKT and WKB

Well-known text and well-known binary serialize geometries. Basic WKT such as `POINT(10 50)` does not itself identify a CRS. Some systems add extended representations, such as an SRID prefix, that are not accepted by every consumer.

Do not confuse geometry WKT with WKT2 for coordinate reference system definitions. They share a phrase, not the same grammar or purpose. A GeoSPARQL WKT literal has a defined optional CRS IRI prefix and datatype.

For binary values, check byte order, dimensional extensions, and the exact supported dialect. A blob containing geometry bytes is not automatically a valid GeoPackage geometry value.

## GeoPackage 1.4

GeoPackage is a standardized SQLite container with defined metadata and content conventions. It supports feature data and tile data, with extensions for additional capabilities. An arbitrary SQLite file containing coordinates is not a conforming GeoPackage.

For features, inspect the content registration, spatial reference definitions, geometry column declarations, and GeoPackage geometry binary headers. Check extensions before assuming a consumer can read every table. Use a conforming writer and validation tooling rather than hand-building a superficially similar file.

GeoPackage is useful for portable delivery and inspection. Concurrency and update behavior depend on the actual application and SQLite usage; the format does not supply an online API automatically.

## GeoParquet editions

Check the declared version and the reader's compatibility. GeoParquet 1.1 and 2.0 are materially different profiles.

Version 2.0 uses Parquet GEOMETRY or GEOGRAPHY logical types with WKB payloads. GeoParquet metadata names the primary geometry column and describes geometry columns. Version 1.1 supports additional native encodings; do not assume those encoding choices carry over unchanged.

In 2.0, the logical type's CRS and any GeoParquet CRS metadata must agree. Missing GeoParquet CRS metadata defaults to CRS84, whereas explicit null denotes an undefined or unknown CRS. Check this together with the logical type rather than silently substituting a CRS. Native geospatial Parquet can exist without the GeoParquet metadata profile.

Geometry columns have structural restrictions, including root-level placement. A byte array named “geometry” without the required logical type or metadata is not enough to claim the selected GeoParquet version.

Columnar pruning and optional spatial covering metadata can help retrieval, but a collection of Parquet files is not a general spatial database by itself. File layout, statistics, indexes, and the query engine still determine lookup behavior.

