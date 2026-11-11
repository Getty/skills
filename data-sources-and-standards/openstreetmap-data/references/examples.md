# Small original examples

All identifiers, names, and coordinates below are synthetic. The fixtures illustrate the data model and must not be uploaded as real OSM edits.

## Native XML and dependency geometry

```xml
<osm version="0.6" generator="synthetic-example">
  <node id="1001" version="1" lat="50.0" lon="10.0"/>
  <node id="1002" version="1" lat="50.0" lon="10.1"/>
  <way id="2001" version="1">
    <nd ref="1001"/>
    <nd ref="1002"/>
    <tag k="highway" v="service"/>
    <tag k="name" v="Example Access Road"/>
  </way>
</osm>
```

The way has no coordinate array of its own. Its geometry is assembled from the referenced nodes, in order. A filter that retains the way but discards both nodes cannot assemble the complete geometry.

## A change to a dependency

```xml
<osmChange version="0.6" generator="synthetic-example">
  <modify>
    <node id="1002" version="2" lat="50.1" lon="10.1"/>
  </modify>
</osmChange>
```

After this change, the derived geometry for way 2001 must be refreshed even though the way remains version 1. Replaying node version 2 should be idempotent; subsequently observing an older version must not revert the current node.

This small document illustrates a change body. It does not supply replication-feed position, transaction durability, or recovery guarantees.

## Inspecting a local extract

The following are example Osmium Tool commands. Confirm the installed tool's options and available files before execution.

```sh
osmium fileinfo region.osm.pbf
osmium check-refs region.osm.pbf
osmium tags-filter region.osm.pbf nwr/industrial -o selected.osm.pbf
```

The last command selects objects having an `industrial` key and uses the tool's normal reference handling. It is not a comprehensive definition of industrial sites: some relevant features use other tags. A production profile needs explicit tag coverage, dependencies, and checks for the relation types it retains.

## Role-aware linking

Consider a synthetic feature with these tags:

```json
{
  "name": "Example Works",
  "industrial": "factory",
  "operator": "Example Manufacturing Ltd"
}
```

The feature names a physical works. The operator text names an organization but is not a globally unique organizational identifier. Retain the feature identity, create or resolve an organization candidate separately, and attach an operator relation with source evidence.

If a later source provides a role-specific external identifier, compare it with the candidate. Do not rewrite the facility's identity to become the organization.

## Acceptance questions

Can the system distinguish a node ID from a way ID? Does moving a node invalidate dependent geometry? Can a newly relevant feature enter the filtered set? Does a deleted object disappear from active search results? Can a reader identify the source generation and the filter that produced an export?

These questions are useful even when the output consists only of files and no online service is operated.

