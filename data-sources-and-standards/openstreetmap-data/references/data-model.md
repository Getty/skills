# Native objects, tags, and interpretation

## The three main object types

A **node** has an identifier and a geographic position. It can be a point feature with tags, a coordinate used by a way, or both. A **way** contains an ordered sequence of node references. It can represent a road, another linear feature, or an area when the tagging and closure support that interpretation. A **relation** contains an ordered list of members, each with an object type, reference, and role. Relations can express multipolygons, boundaries, routes, restrictions, and other structures.

An identifier is meaningful within its object type. Store node 42 and way 42 separately. Keep versions and source metadata alongside the identity; a new version is a revision of that OSM object, not a newly identified real-world entity.

Changesets group editing activity. They do not guarantee that all edits describe one real-world event, one survey, or one business transaction. Contributor and changeset metadata can be absent in extracts supplied for particular uses. Do not assume an extract contains complete editing history.

## Native structure and derived geometry

Maintain a distinction between:

- source objects and their references;
- an assembled feature geometry;
- a normalized domain interpretation;
- identity links to external entities.

A road way's shape depends on its referenced nodes. Moving a node can change the road's derived geometry without changing the way's version. A relation can depend on several ways and nodes; missing members can make its geometry incomplete even when the relation object is present.

Polygon assembly requires domain rules. A closed way tagged as a roundabout remains a linear road representation; other closed ways may denote areas. Multipolygon rings can consist of multiple member ways, and member roles help distinguish outer and inner rings. Do not derive an area from closure alone or silently discard holes.

Node order matters for geometry and can matter for directional semantics. Relation member order should be preserved even when a particular relation interpretation does not use it. Unknown relation types can remain uninterpreted without losing their source structure.

## Tagging is extensible

Tags are string key/value pairs. Familiar keys include `name`, `highway`, `building`, and `operator`, but accepted conventions evolve and usage varies. A wiki description, approved proposal, and measured use in the database are different forms of evidence about a tag.

Preserve the original key/value. A normalized field should record the parsing rule or profile that produced it. Useful distinctions include:

- `name`, `official_name`, `short_name`, and language-specific names;
- a feature's current type versus lifecycle tags such as proposed, construction, disused, or abandoned;
- numbers versus numbers accompanied by units or descriptive text;
- unconditional restrictions versus expressions under a `:conditional` key;
- a scalar value versus a key whose convention permits multiple values.

Do not split all values on semicolons, remove language suffixes, or treat every apparent number as the same datatype. Keep unparsed values when interpretation is uncertain.

## Space, time, and coverage

Native node coordinates use geographic latitude and longitude on WGS 84. Coordinate order in an OSM XML attribute pair is explicit; a later GeoJSON coordinate array follows GeoJSON's longitude/latitude rule. Make transformations and axis conventions explicit at export boundaries.

The edit timestamp and version support source history. They do not establish a precise real-world validity interval. A mapper may record a facility after it opens or remove it after it closes. Application claims about operation dates need their own supporting evidence.

OSM object identity can change when contributors split, merge, replace, or remodel features. A long-lived business identifier should therefore be distinct from a current OSM reference. Store link provenance and allow multiple linked features.

Completeness is contextual. Missing mapped loading bays, ownership tags, or railway access must not become negative assertions. Include coverage and extraction policy in results so downstream consumers can distinguish “not selected,” “not mapped,” and “explicitly tagged otherwise.”

