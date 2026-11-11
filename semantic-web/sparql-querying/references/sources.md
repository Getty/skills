# Primary sources and version status

The skill's portable baseline is the SPARQL 1.1 Recommendation family, published **21 March 2013**.

## Query language and result contracts

- [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/) — graph patterns, solution mappings, algebra, expressions, property paths, aggregates, and result forms.
- [SPARQL 1.1 Overview](https://www.w3.org/TR/sparql11-overview/) — scope of the family and links to its separate specifications.
- [Query Results JSON](https://www.w3.org/TR/sparql11-results-json/) — term-aware SELECT/ASK results, including omitted bindings for unbound variables.
- [Query Results CSV and TSV](https://www.w3.org/TR/sparql11-results-csv-tsv/) — exchange formats with different term-preservation characteristics; CSV alone can lose RDF-term distinctions.
- [SPARQL 1.1 Entailment Regimes](https://www.w3.org/TR/sparql11-entailment/) — query behavior under selected semantic regimes.

## Execution and mutation

- [SPARQL 1.1 Update](https://www.w3.org/TR/sparql11-update/) — graph-store changes, templates, dataset selection, and graph management.
- [SPARQL 1.1 Federated Query](https://www.w3.org/TR/sparql11-federated-query/) — SERVICE evaluation and failure handling.
- [SPARQL 1.1 Protocol](https://www.w3.org/TR/sparql11-protocol/) — HTTP query/update operations and dataset parameters.
- [SPARQL 1.1 Service Description](https://www.w3.org/TR/sparql11-service-description/) — service capability metadata.
- [SPARQL 1.1 Graph Store HTTP Protocol](https://www.w3.org/TR/sparql11-http-rdf-update/) — graph-level HTTP operations, distinct from the query language.

## Newer work

[SPARQL 1.2 Query Language](https://www.w3.org/TR/sparql12-query/) revises SPARQL 1.1. Consult its [publication history](https://www.w3.org/standards/history/sparql12-query/) before presenting newer features as stable. Other 1.2 documents can have different dates and statuses.

[RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/) has a publication status of its own. RDF 1.2 or legacy RDF-star support in a store does not by itself prove current SPARQL 1.2 conformance.

Check engine documentation for query plans, indexes, transaction guarantees, extensions, timeout behavior, and supported entailment. These are implementation-specific. Examples and tuning workflows in this skill are original synthesis rather than copied endpoint recipes.
