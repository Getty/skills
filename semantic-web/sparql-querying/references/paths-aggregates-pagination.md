# Property paths, aggregates, and pagination

## Express reachability

A property path matches relationships through graph structure. Use `/` for sequence, `|` for alternatives, `^` for inverse direction, `?` for zero-or-one, `*` for zero-or-more, and `+` for one-or-more steps. These operators describe graph matching, not an ordered route object returned to the caller.

```sparql
PREFIX ex: <https://example.org/>
SELECT DISTINCT ?ancestor
WHERE { ex:site3 ex:partOf+ ?ancestor }
```

`+` requires a nonzero path, although a cycle can still lead back to the starting node. `*` includes a zero-length match. If the question is strict ancestry, decide how self-reachability and cycles should be handled.

Arbitrary-length paths identify reachable endpoints; they do not enumerate every route or return path length. Fixed sequences can produce duplicate visible results through hidden intermediate variables. Do not use result row counts as route counts without an explicit path model.

A negated property set excludes specified predicates for a step; it is not the complement of an arbitrary path expression. Anchor broad paths with a known start or end when possible. Unbounded traversal over a large connected graph can be expensive even if the final result is small.

## Aggregate the correct unit

```sparql
PREFIX ex: <https://example.org/>
SELECT ?site (COUNT(DISTINCT ?sample) AS ?count)
WHERE { ?sample a ex:Sample ; ex:collectedAt ?site }
GROUP BY ?site
HAVING(COUNT(DISTINCT ?sample) >= 2)
ORDER BY DESC(?count) STR(?site)
```

`GROUP BY` partitions solutions; aggregate expressions operate within each group. `HAVING` filters groups. Projected nonaggregate expressions must obey grouping rules. Use subqueries when an intermediate count needs to be joined with labels or additional relations.

`SUM(DISTINCT ?amount)` is not a general remedy for duplicate joins: two different observations with the same numeric amount may both need to contribute. Deduplicate by observation identity before summing. `SAMPLE` chooses a representative without a portable deterministic choice, and `GROUP_CONCAT` should not be treated as a guaranteed ordered list.

Check empty input, unbound expressions, invalid values, and mixed numeric datatypes when these affect a total. Avoid financial or exact decimal calculations after converting values through floating-point display strings.

## Order before paginating

Without `ORDER BY`, result order is not guaranteed. With ties, page boundaries can still vary. Add a stable unique tiebreaker that is present for every intended row. Blank-node labels are unsuitable as portable pagination keys.

`LIMIT` and `OFFSET` select a slice of the solution sequence. They do not provide a transaction snapshot across requests. Concurrent inserts or deletes can cause skipped or repeated items even with a deterministic sort. Ask the store for snapshot semantics or use an immutable dataset release when consistent traversal is required.

For large offsets, keyset pagination can be useful if the result has a stable ordered key:

```sparql
PREFIX ex: <https://example.org/>
SELECT DISTINCT ?sample
WHERE {
  ?sample a ex:Sample .
  FILTER(isIRI(?sample))
  FILTER(STR(?sample) > "https://example.org/sample/0042")
}
ORDER BY STR(?sample)
LIMIT 100
```

This example paginates IRI strings, not numeric identifiers. Preserve the exact ordering expression in the cursor comparison and include all tie-breaker components for compound keys. Store collation, datatype ordering, and endpoint extensions can affect more elaborate schemes; verify the actual execution environment.

Consult the [SPARQL 1.1 Query specification](https://www.w3.org/TR/sparql11-query/) for path, aggregate, and solution-modifier semantics.
