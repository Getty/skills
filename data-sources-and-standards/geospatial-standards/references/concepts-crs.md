# Geographic concepts and coordinate reference systems

## Feature, geometry, and observation

A feature is an identifiable thing being represented: a building, river, administrative area, or other object. Geometry describes a spatial aspect of that feature. The same facility can have an entrance point, footprint, site boundary, and a simplified display geometry.

A location role belongs in the data contract. A representative point does not have the same meaning as a perimeter. A postal address is a structured reference to a place, not necessarily a surveyed position. An organization is not itself a polygon merely because one of its sites has a boundary.

A coverage associates values with positions or spatial domains, for example a temperature raster. Vector feature collections and raster coverages have different representation and query needs. Do not force every geographic dataset into individual point records.

## What a CRS supplies

A coordinate reference system connects coordinate values to a reference framework. Relevant aspects can include datum or reference frame, coordinate system, axes, units, projection, dimensionality, and vertical reference. Dynamic reference frames can also require a coordinate epoch.

A CRS identifier is useful but not a substitute for understanding the data pipeline. Record what the source declares and what the consuming library expects. Keep a complete definition when an authority identifier alone cannot preserve a custom system.

Longitude/latitude in degrees, easting/northing in meters, and geocentric Cartesian coordinates are not interchangeable arrays. A third ordinate may describe ellipsoidal height, another vertical datum, or something application-specific; do not assume sea-level height.

## Axis order

OGC CRS84 specifies longitude followed by latitude. EPSG:4326's authority definition uses latitude followed by longitude. Many software interfaces expose a traditional x/y convention even for data associated with EPSG:4326. The interface convention must be checked rather than inferred solely from the authority code.

RFC 7946 GeoJSON uses longitude/latitude. OSM XML exposes named latitude and longitude attributes. A WKT geometry literal used by GeoSPARQL can carry a CRS IRI that determines coordinate interpretation. Explicit conversion at format boundaries prevents silent swapping.

Use a test point for which swapping produces a visibly different location. Values such as 10 and 50 remain numerically legal in either order, so range validation alone cannot detect the mistake.

## Assignment versus transformation

Assigning a CRS labels existing numbers. Transforming applies a coordinate operation and usually changes them. Relabeling projected meter coordinates as longitude/latitude does not make them geographic coordinates.

A transformation can depend on area of use, epoch, datum grids, and available operations. Record the chosen operation and important resources for reproducibility. A successful library call does not establish that the selected operation is suitable for the accuracy required.

PROJ and other coordinate libraries can inspect and transform coordinate systems. Use current documentation for axis options and operation selection. Do not silently fall back to a lower-accuracy operation when the result is used as precise evidence.

## Precision and uncertainty

Decimal places describe numerical representation; positional accuracy concerns closeness to the actual location. Rounding more digits into a file does not improve a geocoded or approximate point.

Keep source-reported precision, accuracy, collection method, and interpretation where available. A building-sized uncertainty may matter for a hazard boundary even when the point is stored with many decimal places.

Spatial data also has temporal uncertainty. A boundary may have changed since a facility was recorded. Preserve geometry validity dates when known and source publication or retrieval times separately.

## A minimum coordinate contract

For a reusable output, record feature identity, geometry role, CRS, axis convention, dimensionality, units, source, source time, transformation history, and any known accuracy. Mark unknown values explicitly. This is suggested application metadata, not a claim that every exchange standard requires all these fields.

