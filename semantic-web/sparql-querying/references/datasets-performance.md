# Dataset scope, inference, and performance

## Define the dataset

A query operates over a default graph and named graphs. The service can supply a default dataset, and query/protocol options can select another. Do not assume the default graph is the union of every stored graph; stores often offer configurable behavior.

`GRAPH <iri> { ... }` matches a selected named graph. `GRAPH ?g { ... }` ranges over named graphs and binds their names. The default graph is not one of those named-graph bindings. A graph IRI identifies a graph in the dataset; it does not automatically certify the provenance of its contents.

```sparql
PREFIX ex: <https://example.org/>
SELECT ?g ?sample ?site
WHERE {
  GRAPH ?g { ?sample ex:collectedAt ?site }
}
```

Use `FROM` to describe contributions to the query's default graph and `FROM NAMED` to describe available named graphs. Supplying only `FROM NAMED` does not implicitly populate the default graph. A `FROM` graph does not automatically become available by the same name inside `GRAPH`. Loading policies and protocol dataset parameters can affect how service endpoints implement these choices.

Keep graph selection explicit when results must distinguish sources or releases. A union can collapse repeated identical triples and erase which graph supplied them. Conversely, joining patterns across named graphs can create combinations that no individual source asserted together.

## Declare inference

A store can answer over asserted triples, materialized entailments, query-rewritten consequences, or a mixture. Record whether the active regime is simple, RDF, RDFS, a supported OWL profile, or a vendor rule set. A graph containing subclass axioms does not by itself force the endpoint to infer superclass membership.

An explicit path such as `rdf:type/rdfs:subClassOf*` can capture a particular traversal when the necessary triples are present. It is not a complete substitute for all RDFS or OWL entailment. Explain the requested consequence rather than labeling the path “full reasoning.”

Equality inference can multiply or merge apparent identifiers. Keep the logical result policy separate from how the endpoint materializes `owl:sameAs` consequences or chooses representative terms.

## Measure before rewriting

Inspect the actual plan and cardinalities if the engine exposes them. Useful observations include candidate counts for selective patterns, join order, graph-index usage, filter placement, path evaluation, intermediate solution size, and remote-service calls. A small final result can still require huge intermediate work.

Common opportunities include restricting known identifiers with `VALUES`, choosing selective required patterns, avoiding accidental cross joins, aggregating before joining many labels, and anchoring property paths. Textual pattern order is only a hint on some engines; it is not a portable control over execution order.

Do not move a filter across OPTIONAL, change EXISTS to MINUS, remove duplicates, or push a limit through a join without checking semantic equivalence. Compare the intended result multiset, RDF graph, or aggregate on a fixture that contains the relevant edge case.

## Separate query tuning from operations

Record cold versus warm cache, data version, inference state, indexes, concurrency, timeout, result serialization, and network transfer when measuring latency. Keep queries comparable by consuming the full intended result or measuring a clearly stated first-page goal.

A public endpoint may impose result caps, execution limits, or rate controls. Detect truncation and inspect response metadata or service documentation. Do not call a partial result a complete answer because the request returned successfully. Use a dump or maintained local snapshot when the job requires reproducible exhaustive processing and the endpoint contract cannot provide it.

Primary references: [Query](https://www.w3.org/TR/sparql11-query/), [Entailment Regimes](https://www.w3.org/TR/sparql11-entailment/), [Protocol](https://www.w3.org/TR/sparql11-protocol/), and [Service Description](https://www.w3.org/TR/sparql11-service-description/).
