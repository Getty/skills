# Geometry, topology, and spatial queries

## Geometry types and validity

The Simple Features family supplies common geometric concepts such as points, curves or line strings, polygons, multi-geometries, and geometry collections. Different formats and software implementations support different subsets and extensions.

Syntactically valid coordinates can describe an invalid polygon. Problems include self-intersections, malformed rings, inappropriate holes, and incompatible dimensions. Geometry validation is separate from JSON/XML parsing and from checking whether a feature belongs in the domain.

Geometry repair can change topology or type. Preserve the original representation and record the repair method, software version when relevant, and resulting change. A repair that makes a polygon processable is not proof that it reconstructs the intended real-world boundary.

Simplification is also a transformation. A boundary simplified for a small-scale map may be unsuitable for assigning a facility near its edge.

## Topological relations

The DE-9IM framework describes how interiors, boundaries, and exteriors intersect. This helps explain why everyday words such as “inside” are insufficient as a query specification.

For a point and polygon, a point on the polygon boundary is not within the polygon under the usual Simple Features within predicate. An implementation's covers predicate can include boundary points. Select the behavior intentionally, especially for administrative assignment or risk classification.

Intersects is broad: it includes touching as well as overlap. Overlaps has more specific dimension and intersection requirements. Contains, covers, and intersects are not interchangeable shortcuts.

Empty geometries, null values, and invalid geometries require explicit handling. Null can mean unknown or absent representation; an empty geometry is an actual geometry value with no positions. Do not silently treat both as a confirmed feature outside every area.

## Distance and area

A planar geometry calculation uses the units and assumptions of its coordinate space. A calculation on raw longitude/latitude values can yield degrees, not meters. A geodesic or geography calculation uses a different measurement model.

For local engineering distances, an appropriate projected CRS may be suitable. For broad geographic extent, use an appropriate geodesic method and document whether its model is spherical or ellipsoidal. A projection suitable for visualization is not automatically suitable for accurate area or distance.

Distance from point to footprint, point to centroid, and entrance to road network answer different questions. Define both the objects and the measurement. A straight-line distance is not a travel distance.

Buffers also depend on units and the geometric model. A numerical radius of 1000 is meaningless without those definitions. Crossing the antimeridian or operating near the poles deserves explicit examples and tests.

## Indexes and exact predicates

Spatial indexes commonly organize envelopes or other approximations so an engine can narrow the candidate set. Overlapping bounding boxes do not establish intersecting feature geometries. Preserve an exact predicate after coarse filtering when the question requires it.

Index behavior is implementation-specific. Inspect the query plan and actual data distribution rather than promising constant-time spatial lookup. Large or overlapping geometries can make envelope filters less selective.

PostGIS provides indexed spatial predicates and distinguishes geometry and geography behavior. In that implementation, ST_DWithin on geometry uses the coordinate system's units, while geography distance is expressed in meters. ST_Covers includes boundary points. These are useful examples of why checking the implementation's documented semantics matters.

## Reproducible analysis

Return the relevant input geometry versions, selected predicate, boundary rule, CRS, measurement units, and tolerance or uncertainty policy. An application may choose to flag points near a boundary for review rather than force a single assignment.

If combining a physical site with a disaster area or an administrative region, keep the two source geometries separate from the derived relationship. The relationship can change when either input is updated.

