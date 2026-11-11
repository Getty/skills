---
name: openstreetmap-data
description: "Use when acquiring, filtering or joining OpenStreetMap data — nodes, ways, relations, tags, PBF and XML extracts, OsmChange diffs, geometry assembly, Nominatim geocoding, routing, tiles, ODbL obligations."
---

# OpenStreetMap Data

Use OpenStreetMap (OSM) as a versioned community-maintained geographic dataset. OSM combines a small object model with extensible tagging conventions; it is not one fixed industry ontology, and its database is not the same product as a rendered map, geocoder, or routing service.

Build the answer around the user's actual need: geographic context, feature extraction, name or address resolution, spatial analysis, route calculation, or visual presentation. These operations require different derived data and have different completeness limits.

## Working procedure

1. **Define the contract.** Record the area, feature types, required attributes, output, acceptable age, and whether historical states are needed. Determine whether the task needs points, complete geometries, or only identifiers.
2. **Identify the source.** Record provider, extract coverage, snapshot date, file format, checksum when available, license, and compatible update feed. Treat provider-specific omissions and clipping as part of the data contract.
3. **Decode the native objects.** Preserve typed object identities, versions, tags, ordered way references, and typed relation members with roles. Use established parsers for PBF or XML.
4. **Select with dependencies.** Retain the nodes, member ways, and relations needed to interpret selected features. A dependency can be needed even if it does not match the business filter.
5. **Construct a queryable projection.** Assemble geometries, parse selected tags, build the required lookup or spatial indexes, and retain links back to the source objects. Keep source tags separate from derived attributes.
6. **Define change handling.** Track feed position, apply creates/modifications/deletions, update reverse dependencies and derived geometry, and detect newly relevant objects. Publish a consistent generation rather than partially refreshed indexes.
7. **Check the result.** Inspect unresolved references, invalid geometry, ambiguous entity links, missing attributes, and source coverage. Describe measured limits; do not invent a universal hardware minimum.

## Choose the reference

- Read [the native data model](references/data-model.md) before interpreting objects, tags, timestamps, or identity.
- Read [formats and acquisition](references/formats-and-acquisition.md) when choosing extracts, PBF/XML, APIs, or processing tools.
- Read [updates and filtering](references/updates-and-filtering.md) when designing reproducible filtered datasets, incremental refresh, or recovery.
- Read [identity and context](references/identity-and-context.md) when joining OSM to organizations, Wikidata, named places, or business datasets.
- Read [services and licensing](references/services-and-licensing.md) when deciding whether geocoding, routing, tiles, or a spatial database is needed.
- Read [worked examples](references/examples.md) for small original fixtures and practical checks.
- Consult [primary sources](references/sources.md) for current documentation and policies.

## Rules that prevent misleading results

- Use the tuple `(source, object_type, object_id)`; a node and a way with the same numeric ID are different objects.
- A closed way does not automatically denote an area. Interpret feature tags and relation structure.
- A place, physical facility, operator, owner, brand, and administrative unit are separate entities and roles.
- An edit timestamp records a database edit, not necessarily when something changed in the real world.
- Preserve original tags before applying key-specific normalization. Semicolons, units, language suffixes, and conditional expressions do not have one universal parser.
- Absence of a tag or feature is missing information, not proof of absence in reality.
- A matching `wikidata` tag is an identity assertion to examine. It is not proof that every related organization or nearby feature has that identity.
- Public service usage policies apply to the named endpoint; software installed elsewhere has its own operating limits.
- Geometry, addresses, and names do not establish commercial supply relationships.

## Expected answer or deliverable

Give a source and scope decision, a selection rule, a dependency policy, an update plan if needed, and one representative example. For a proposed service, explain its function and what evidence it can return. State whether examples were only parsed or also executed against a real tool. Preserve source and license metadata so later exports remain attributable.
