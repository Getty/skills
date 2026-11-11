# Original examples and interpretation checks

These examples use synthetic features and are illustrative rather than an assertion about a real site.

## GeoJSON feature

```json
{
  "type": "Feature",
  "id": "site-example",
  "geometry": {
    "type": "Point",
    "coordinates": [10.0, 50.0]
  },
  "properties": {
    "name": "Example Site",
    "geometry_role": "representative_point"
  }
}
```

The coordinate order is longitude, latitude. The custom `geometry_role` property is application metadata, not a standardized GeoJSON property. The point does not define the site's perimeter or its entrance.

A GeoJSON parser accepting this document establishes syntax and structure only to the extent checked by that parser. It does not verify the site's real location.

## GeoSPARQL representation

```turtle
@prefix ex: <https://example.invalid/geo/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .

ex:site a geo:Feature ;
    geo:hasGeometry ex:site-point ;
    geo:hasDefaultGeometry ex:site-point .

ex:site-point a geo:Geometry ;
    geo:asWKT
        "<http://www.opengis.net/def/crs/OGC/1.3/CRS84> POINT(10 50)"^^geo:wktLiteral .

ex:area a geo:Feature ;
    geo:hasGeometry ex:area-boundary .

ex:area-boundary a geo:Geometry ;
    geo:asWKT
        "<http://www.opengis.net/def/crs/OGC/1.3/CRS84> POLYGON((9 49, 11 49, 11 51, 9 51, 9 49))"^^geo:wktLiteral .
```

The geometry nodes are distinct from the features. Parsing this RDF does not execute GeoSPARQL.

## A geometry function query

```sparql
PREFIX ex: <https://example.invalid/geo/>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>

SELECT ?site
WHERE {
  ?site geo:hasDefaultGeometry/geo:asWKT ?point .
  ex:area geo:hasGeometry/geo:asWKT ?boundary .
  FILTER(geof:sfWithin(?point, ?boundary))
}
```

A supporting engine should identify the synthetic site as within this polygon. A generic SPARQL parser can accept the syntax without supplying the function implementation.

For a boundary case, change the point to `POINT(9 50)`. Under the within relation, this boundary point does not pass the filter. If the requirement is to include boundary points, select and verify the corresponding boundary-inclusive predicate supported by the chosen engine.

## A measurement contract

For “sites within five kilometers of a port,” define:

- which site and port geometry roles are used;
- whether the measurement is straight-line/geodesic or along a route;
- the CRS and measurement model;
- units and the exact threshold rule;
- source geometry versions and treatment of uncertainty.

The sentence alone is insufficient to choose a correct query. A route distance additionally requires a suitable network and access profile; a geometry distance does not provide those.

