# Entity identity, context, and joins

## Match entities at the right level

An OSM feature can represent a building, site, entrance, administrative area, transport route, or another geographic object. A business dataset may describe a legal entity, corporate group, security, or organizational role. Matching names alone can conflate these levels.

Represent the physical site and the organization separately. Link them with an explicit role such as operates, owns, occupies, or uses a brand, supported by the relevant source. A company headquarters location does not identify all manufacturing sites, and a parent company is not necessarily the legal operator of a facility.

Store candidate links with the matched identifiers, context, evidence, mapping method, confidence where appropriate, and review status. An algorithmic confidence value is not a standardized OSM field.

## Wikidata links

The usual intent of `wikidata=Q...` is to identify the mapped feature itself. A key such as `operator:wikidata=Q...` links the operator. Similar role-specific keys must be interpreted according to their own conventions; do not collapse them into the identity of the feature.

A Wikidata entity can correspond to several OSM objects, and one real-world feature may be represented by multiple components. Conversely, an OSM boundary or route relation may represent a particular geographic aspect of a broader entity.

Wikidata's OpenStreetMap relation ID property identifies a relation, not arbitrary node or way IDs. Preserve the type when importing such a reference. A numeric reference without object type is not a complete OSM identifier.

Treat cross-dataset links as source assertions. Check implausible type combinations, obsolete references, and whether a link names a site or an organization before automatic merging.

## Location is not one field

Distinguish a representative point, surveyed entrance, postal address, building footprint, site perimeter, and administrative boundary. They support different tasks.

A centroid can lie outside a concave polygon or inside a hole. A label point may be chosen for map display rather than spatial containment. An address can name a mailing destination rather than the operating site. Retain the geometry role and the method used to derive it.

For containment, use suitable boundary geometry and a documented boundary rule. A reverse geocoder's nearby address response is not equivalent to exact point-in-polygon analysis. Nominatim explicitly searches for a suitable nearby indexed object and returns its address information.

Administrative containment can be interpreted differently across datasets and political contexts. Preserve source, identifiers, time, and any competing assertions instead of treating one result as a universal political statement.

## Batches and bounded context

A practical batch resolution result should contain the input term, candidates, selected identity if resolved, required contextual features, and reasons for ambiguity or omission. Language and native names matter; retaining only translated labels can reduce match quality.

Define contextual expansion by relation type and depth. For a facility, useful context might include operating organization, city, region, country, and nearby transport infrastructure. Unbounded traversal can pull in an entire corporate group or geographic graph.

Report truncation and scope. A query that returns only selected ports should not claim to list every transport option. When using distance thresholds, state the geometry, measurement model, and units.

## Spatial relationships and business evidence

Proximity supports geographic context. It does not prove access, a route, trade volume, or a supplier relationship. A road routing engine can estimate a route permitted by its road profile; it does not establish that goods actually travel that route.

Use OSM to support questions about where features are and how mapped infrastructure connects. Use explicit business or operational evidence for who supplies whom, ownership percentages, production capacity, and actual shipment paths.

