# Query forms and graph patterns

## Choose the result type

`SELECT` returns solution mappings, usually presented as rows with variable columns. A mapping may leave some variables unbound. `ASK` reports whether a solution exists. `CONSTRUCT` instantiates a triple template to produce an RDF graph. `DESCRIBE` returns an implementation-defined description; it is unsuitable when a portable, exact export boundary is required.

A basic query over a collection:

```sparql
PREFIX ex: <https://example.org/>
SELECT ?sample ?site
WHERE {
  ?sample a ex:Sample ; ex:collectedAt ?site .
}
```

Each repeated variable joins patterns on a compatible RDF term. A semicolon is syntactic shorthand, not a procedural step. Prefixes expand to full IRIs and have no independent semantic role.

## Join and combine deliberately

Required patterns in a group combine matching bindings. If a sample has two collectors and three classifications, joining both properties can produce six combinations. This is often correct for a relationship table and wrong for a count of samples.

Use `UNION` for alternative matching patterns. A resource satisfying both alternatives can appear more than once. Use `VALUES` to supply a small table of allowed terms or bindings; repeated rows can affect multiplicity, and `UNDEF` leaves a variable unbound rather than binding it to a null value.

```sparql
PREFIX ex: <https://example.org/>
SELECT ?sample ?site
WHERE {
  VALUES ?site { ex:site3 ex:site7 }
  ?sample a ex:Sample ; ex:collectedAt ?site .
}
```

An unconnected variable in a second pattern can unintentionally cross-join the whole dataset. Inspect variable names and scope when a result unexpectedly multiplies.

## Bind expressions and isolate subqueries

Use `BIND` to assign an expression result to a new variable. An expression error does not necessarily remove the whole mapping; it can leave the target variable unbound. Check subsequent filters accordingly. Do not reuse an already-in-scope variable as a `BIND` target where the language forbids it.

Use a subquery to isolate aggregation, deduplication, or a bounded selection before joining presentation fields. Variables not projected from the subquery are not exposed to the outer query. A subquery is not an automatically correlated SQL lateral query; reason from SPARQL scope and joins.

```sparql
PREFIX ex: <https://example.org/>
SELECT ?site ?sampleCount ?label
WHERE {
  { SELECT ?site (COUNT(DISTINCT ?sample) AS ?sampleCount)
    WHERE { ?sample a ex:Sample ; ex:collectedAt ?site }
    GROUP BY ?site }
  OPTIONAL { ?site ex:label ?label }
}
```

Several site labels can repeat the already-computed count across output rows. That does not mean the inner count changed.

## Construct graphs consciously

`CONSTRUCT` instantiates its template for each solution, then the result graph has RDF set semantics. Duplicate constructed triples collapse. Blank nodes in the template are scoped per solution, so they can create a new structured node for each row. Unbound template variables or invalid triple positions cause affected template triples to be omitted.

```sparql
PREFIX ex: <https://example.org/>
CONSTRUCT { ?sample ex:collectedAt ?site }
WHERE { ?sample a ex:Sample ; ex:collectedAt ?site }
```

SPARQL 1.1's standard `CONSTRUCT` result is a graph, not a named-graph dataset export. Use a suitable dataset export mechanism when graph boundaries matter. Prefer `ASK` for existence checks when the interface supports it, while remembering that an implementation's query plan determines actual performance.

Read the [SPARQL 1.1 Query Recommendation](https://www.w3.org/TR/sparql11-query/) for exact grammar, scope, and algebra.
