# Primary sources and edition notes

Pin the edition used by the task and verify implementation support separately.

## Models and coordinate systems

- [OGC Simple Features Access](https://www.ogc.org/standards/sfa/): geometry and topology standards family.
- [PROJ FAQ](https://proj.org/en/stable/faq.html): coordinate transformations, reference-system definitions, and axis conventions.
- [PostGIS ST_Covers](https://postgis.net/docs/ST_Covers.html): an implementation's boundary-inclusive relation.
- [PostGIS ST_DWithin](https://postgis.net/docs/ST_DWithin.html): distance units and indexed evaluation behavior.

## Exchange and semantic standards

- [GeoJSON, RFC 7946](https://www.rfc-editor.org/rfc/rfc7946): standards-track format published in 2016; use its rules rather than the older arbitrary-CRS GeoJSON convention.
- [GeoPackage 1.4.0](https://www.geopackage.org/spec140/index.html): published OGC encoding standard, 2024-02-06.
- [GeoParquet release index](https://geoparquet.org/releases/), [2.0.0 specification](https://geoparquet.org/releases/v2.0.0/), and [1.1.0 specification](https://geoparquet.org/releases/v1.1.0/): check declared edition and native Parquet logical-type compatibility.
- [GeoSPARQL 1.1](https://docs.ogc.org/is/22-047r1/22-047r1.html): published OGC standard, 2024-01-29, with separate conformance modules.
- [OGC API Features Part 1 Core 1.0.1](https://docs.ogc.org/is/17-069r4/17-069r4.html): feature access and discovery; extension support must be checked.
- [OGC API Features standards page](https://www.ogc.org/standards/ogcapi-features/): related parts and current publication status.

The source/projection distinction, suggested coordinate contract, and example acceptance checks are application guidance. They do not claim to add normative requirements to any of these standards. Examples are original and synthetic.

