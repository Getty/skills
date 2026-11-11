# Primary sources and freshness limits

Wikimedia documentation and deployment policies evolve. Pin source revisions or downloaded schemas when reproducibility matters and recheck endpoint limits and available streams before implementation.

| Source | Contract or purpose |
| --- | --- |
| [Wikibase DataModel](https://www.mediawiki.org/wiki/Wikibase/DataModel) | General model and value semantics |
| [Canonical entity JSON](https://doc.wikimedia.org/Wikibase/master/php/docs_topics_json.html) | Public serialization, snaks, rank, ordering, terms, and typed values; mutable master documentation |
| [RDF Dump Format](https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format) | Full/truthy RDF, predicate families, export metadata, special values, and WDQS differences |
| [Data access](https://www.wikidata.org/wiki/Wikidata:Data_access) | Choosing services and current access conventions |
| [Database download](https://www.wikidata.org/wiki/Wikidata:Database_download) | Canonical dumps, framing, and format stability |
| [Wikibase Action API](https://www.mediawiki.org/wiki/Wikibase/API) | Module entry point; inspect live API help for parameters |
| [Ranking](https://www.wikidata.org/wiki/Help:Ranking) | Preferred, normal, deprecated, and best-rank selection |
| [Statements](https://www.wikidata.org/wiki/Help:Statements), [Qualifiers](https://www.wikidata.org/wiki/Help:Qualifiers), [Sources](https://www.wikidata.org/wiki/Help:Sources) | Wikidata's editorial statement conventions |
| [P31](https://www.wikidata.org/wiki/Property:P31), [P279](https://www.wikidata.org/wiki/Property:P279) | Actual property meanings; do not generalize these IDs to unrelated repositories |
| [RecentChanges API](https://www.mediawiki.org/wiki/API:RecentChanges) | Polling, continuation, finite history, and timestamp overlap |
| [EventStreams HTTP Service](https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams_HTTP_Service) | Discovery, event schema, resume behavior, and stream-dependent retention |
| [Streaming Updater](https://wikitech.wikimedia.org/wiki/Wikidata_Query_Service/Streaming_Updater) and [Public Update Stream](https://wikitech.wikimedia.org/wiki/Wikidata_Query_Service/Streaming_Updater/Public_Update_Stream) | RDF diffs, lifecycle operations, shared-data semantics, and dataset scope |
| [Stable Interface Policy](https://www.wikidata.org/wiki/Wikidata:Stable_Interface_Policy) | Stable interfaces, compatibility promises, extensibility, and exclusions |

Treat documentation examples and historical configuration values as examples, not current service guarantees. In particular, do not hardcode a retention duration, endpoint partition, entity count, hardware requirement, or stream identifier from memory. A stream's naming and schema need direct verification.

The bundled material is original synthesis. JSON examples are synthetic and do not assert real-world Wikidata facts. No full dump, production-scale updater, or external database is implied by the examples. The skill is independent of storage technology and does not require any sibling skill. A faithful source import preserves what Wikidata says; application truth assessment remains a separate responsibility.
