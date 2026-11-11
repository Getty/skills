# Updates and federated queries

## Select mutation semantics deliberately

SPARQL Update operates on a graph store. `INSERT DATA` adds specified triples; `DELETE DATA` removes specified triples. `DELETE`/`INSERT` with `WHERE` evaluates a pattern and uses its bindings to instantiate deletion and insertion templates. An RDF graph's set behavior makes repeated identical inserted triples redundant, but blank-node generation and broader update patterns can make a request non-idempotent.

```sparql
PREFIX ex: <https://example.org/>
WITH ex:inventoryGraph
DELETE { ?sample ex:status ex:Pending }
INSERT { ?sample ex:status ex:Reviewed }
WHERE {
  ?sample a ex:Sample ; ex:status ex:Pending .
  VALUES ?sample { ex:sample8 ex:sample9 }
}
```

Preview the `WHERE` bindings against the same graph context when planning an update. Restrict by stable identifiers or an explicit business condition. A preview can become stale under concurrent writes; use the store's transaction or conditional-update facilities when that matters.

`WITH` supplies a default graph context for relevant parts of a modify operation. `USING` and `USING NAMED` define the dataset used by `WHERE` and can alter how that default is selected. Explicit `GRAPH` clauses can target other graphs. Read these together rather than assuming one clause controls every triple in a request.

Blank nodes cannot be used as durable keys across separate requests. `DELETE DATA` does not accept blank nodes, and blank nodes in deletion templates are restricted. Match the intended node through graph patterns instead. Insertion templates can create fresh blank nodes per solution, so retries need particular care.

## Distinguish graph management

`CLEAR` removes graph content while `DROP` removes a graph from the store; exact persistence of empty graphs depends on store capabilities. `CREATE`, `LOAD`, `COPY`, `MOVE`, and `ADD` have distinct graph-store effects. `LOAD` can retrieve external data, so document retrieval policy and format handling.

`SILENT` suppresses specified operation errors; it does not prove success. Do not broadly silence failures in a migration. Multi-operation request handling, isolation, rollback behavior, and concurrent transactions need verification against the actual service; a standard-looking request is not a portable promise of every database transaction property.

## Federate with explicit coverage

`SERVICE` evaluates a pattern at another SPARQL endpoint and joins the returned bindings. Plan which variables are known locally and which must be retrieved remotely. A selective identifier table can reduce data transfer, but batching limits and engine optimizer behavior vary.

```sparql
PREFIX ex: <https://example.org/>
SELECT ?site ?label
WHERE {
  VALUES ?site { ex:site3 ex:site7 }
  SERVICE <https://data.example.org/sparql> {
    ?site ex:label ?label
  }
}
```

The endpoint is illustrative and is not meant to be contacted. Never assume that an endpoint in source data is an authorized network destination. Bound federation hosts, timeouts, response sizes, and credentials according to the environment.

`SERVICE SILENT` changes failure behavior; failed remote evaluation may leave surrounding results without enrichment. Therefore “no remote label” can mean missing data or an unavailable service depending on the query and failure handling. Report coverage and failures separately when completeness matters.

Avoid declaring remote blank nodes identical across calls. Independent endpoints can update at different times, so a federated result need not correspond to one global snapshot. Record dataset releases or retrieval times for reproducibility and retain the remote query/parameters when debugging.

Use [SPARQL Update](https://www.w3.org/TR/sparql11-update/) for mutation semantics, [Federated Query](https://www.w3.org/TR/sparql11-federated-query/) for SERVICE, and the [Graph Store HTTP Protocol](https://www.w3.org/TR/sparql11-http-rdf-update/) when operating on whole graph representations through HTTP.
