# Service roles, operating boundaries, and licensing

## Select by function

| Need | Appropriate component | What it does not establish |
| --- | --- | --- |
| Retain native geographic objects | Extract files and an object processor | Search ranking, routing, or styled maps automatically |
| Spatial containment or distance | A spatial query engine and appropriate geometries | Real-world ownership or commercial relationships |
| Search names and addresses | A geocoder such as Nominatim | Complete OSM coverage or exact boundary containment |
| Display maps | A renderer or tile service, for example Martin | A complete queryable source dataset |
| Deliver prepared vector tiles | A tile archive such as PMTiles plus a client/server | General source editing or arbitrary feature queries |
| Road route calculations | A routing engine such as OSRM with a chosen profile | Maritime supply paths or evidence of actual traffic |

These are examples of implementations and packaging, not additional requirements of the OSM data model. One application can combine them, but each has its own build, storage, update, and performance contract.

## Public services versus installed software

Policies for an operator's public endpoint are not inherent limits of the software. The public Nominatim endpoint has restrictions on request rate, bulk and systematic queries, autocomplete, identification, and caching. Check the live policy before writing a client. A separately operated instance needs an explicit capacity and access policy of its own.

The standard OSM raster tile service is not a bulk map download endpoint. Its policy addresses attribution, identification, caching, and prohibited bulk fetching. A compatible client is not automatically entitled to use any tile provider.

Prefer processing extracts for repeated broad data selection. Do not route an offline ingestion workload through thousands of individual geocoder requests when the task is a structured extract.

## Tiles and archives

Vector tiles organize data by tile coordinate and zoom, often with simplification, clipping, and a deliberately limited attribute set. Features can occur in multiple tiles. They are effective for display but can be misleading as a canonical analytical dataset.

PMTiles is an archive format designed for efficient range access to prepared tiles. Its normal use is read-only distribution; updating archive contents requires producing a revised archive. Keep the authoritative features and the process that generated tiles if refresh is required.

Martin can serve tiles from supported data sources, including databases and archives. Choose a source based on update frequency and query needs. Installing a tile server alone does not provide address search or routing.

## Attribution and database rights

OSM data is distributed under the Open Database License (ODbL). The project's copyright page and linked license are primary starting points. Preserve attribution and license information in the source manifest and plan how users of exports or maps will receive the required notices.

Distinguish source databases, derived databases, collective databases, and produced works when assessing obligations. The classification depends on the actual processing and distribution. Do not announce that every joined field acquires the same license, or that making an image always removes every obligation.

For a concrete publication or redistribution decision, consult the current license text and relevant OSM Foundation guidance; explain the specific data flow instead of providing a blanket legal conclusion. A general ingestion design can still retain source-level provenance and separate layers without deciding every eventual distribution case.

Other linked sources have their own terms. A Wikidata identifier attached to an OSM feature does not erase the provenance or licensing of either dataset. Public access to an API is also distinct from permission to redistribute its responses.

## Operational output

Document the selected component, geographic coverage, data generation, refresh process, query capability, and endpoint policy. Name known gaps. Quote measured capacity for the actual dataset and configuration, and leave unmeasured capacity as an estimate.

