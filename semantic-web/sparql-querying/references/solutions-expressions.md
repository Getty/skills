# Multisets, missing values, and expressions

## Preserve the intended multiplicity

SPARQL evaluates solution sequences with multiset behavior: equal-looking rows can occur more than once. Projection can hide the variables that distinguish the original matches. `DISTINCT` removes duplicate projected mappings; `REDUCED` allows some duplicate elimination but does not guarantee a fully distinct result.

Count the intended entity or relation before attaching multi-valued descriptive data. `COUNT(*)` counts solution mappings; `COUNT(?x)` counts bound, non-error values of that expression; `COUNT(DISTINCT ?x)` counts distinct accepted values. None automatically knows the business unit of observation.

## Place OPTIONAL filters intentionally

Compare these complete queries:

```sparql
PREFIX ex: <https://example.org/>
SELECT ?sample ?mass
WHERE {
  ?sample a ex:Sample .
  OPTIONAL { ?sample ex:mass ?mass . FILTER(?mass > 10) }
}
```

```sparql
PREFIX ex: <https://example.org/>
SELECT ?sample ?mass
WHERE {
  ?sample a ex:Sample .
  OPTIONAL { ?sample ex:mass ?mass }
  FILTER(?mass > 10)
}
```

The first retains samples without a matching mass above ten, leaving `?mass` unbound. The second removes rows whose mass comparison is false or errors, including unbound mass values. This difference often explains why an “optional field” unexpectedly becomes mandatory.

A filter's scope follows the enclosing group, not a simple line-by-line execution model. Moving filters or reordering dependent OPTIONAL patterns can change meaning. A textual rearrangement is not automatically an optimization.

## Treat errors and absence separately

An unbound variable is not an RDF null literal. Use `BOUND`, `COALESCE`, or `IF` when the contract needs explicit missing-value behavior. `COALESCE` chooses the first expression that does not error; it can also mask malformed input, so do not use it to silently turn invalid quantities into zero.

A filter retains a mapping only when its expression has a true effective boolean value. Type errors and unbound variables can eliminate mappings. Logical operators have defined error behavior, so do not import host-language truthiness rules. Invalid casts, incompatible datatypes, and malformed lexical values deserve small reproductions.

## Compare terms versus values

Use `sameTerm` when exact RDF term identity matters. Numeric `=` can compare values across compatible numeric datatypes and lexical forms. For example, differently spelled integer literals can denote the same value while remaining distinct terms. `STR` removes datatype or language information and should not be used casually to force equality.

An IRI and a literal containing its textual spelling are different terms. Language-tagged strings with different tags are different RDF terms. Check language selection with the intended `LANG`/`LANGMATCHES` policy rather than silently collapsing all labels.

## Choose the right negation

`FILTER NOT EXISTS` tests whether a pattern has a match in the current solution context. `MINUS` removes compatible mappings with shared bindings under its defined algebra. They are not interchangeable: with no shared variables, `MINUS` does not remove all left-hand rows merely because its right side has matches.

Use a missing-property test only relative to the selected dataset and entailment regime. It means no matching statement is available there; it does not prove the real-world property is false. This distinction matters when an RDF graph is incomplete or when related statements live in another named graph.

The authoritative details are the [SPARQL expressions and algebra](https://www.w3.org/TR/sparql11-query/). These examples deliberately use ordinary RDF 1.1 terms without vendor extensions.
