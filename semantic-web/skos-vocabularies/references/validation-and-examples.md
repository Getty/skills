# Validation and examples

## Distinguish validation layers

Validate syntax first with an RDF parser, then integrity with the selected SKOS entailment assumptions, then the application profile. Finally, review editorial meaning. A parser checks serialization; an OWL reasoner may infer consequences without giving the closed-world completeness checks expected by an editor. A SHACL profile can check completeness, but its requirements must be disclosed.

Use these categories in findings:

| Category | Example |
| --- | --- |
| RDF syntax failure | Unterminated literal or malformed list syntax |
| SKOS integrity conflict | Two distinct preferred labels with the same language tag |
| SKOS entailment-dependent conflict | Related concept also reachable through broader links |
| Local profile failure | Missing required English definition |
| Editorial warning | Two concepts with identical labels and unclear scope |

Check concept/scheme disjointness; collection disjointness from concepts and schemes; lexical-property disjointness; preferred-label uniqueness by language; hierarchical-versus-associative conflicts; and exact-match incompatibilities. For XL, check literal-form cardinality and the simple labels obtained from the XL pattern. Do not declare cycles, absent labels, or multiple scheme memberships invalid under SKOS solely because a local tool dislikes them.

## Work through a complete small vocabulary

Synthetic Turtle, using a private notation datatype:

```turtle
@prefix ex: <https://example.org/vocab/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

ex:scheme a skos:ConceptScheme ;
    skos:prefLabel "Travel subjects"@en ;
    skos:hasTopConcept ex:transport .
ex:transport a skos:Concept ;
    skos:inScheme ex:scheme ;
    skos:prefLabel "Transport"@en .
ex:rail a skos:Concept ;
    skos:inScheme ex:scheme ;
    skos:prefLabel "Rail transport"@en, "Schienenverkehr"@de ;
    skos:altLabel "Railway transport"@en ;
    skos:notation "003"^^ex:LocalCode ;
    skos:definition "Transport using vehicles guided by rails."@en ;
    skos:broader ex:transport .
```

Verify that the English and German preferred labels do not conflict. Preserve the code's leading zeros. Infer `ex:rail skos:broaderTransitive ex:transport`; do not reinterpret the relation as class subsumption. The example intentionally leaves language coverage incomplete to demonstrate that a local translation requirement differs from standard consistency.

## Query with explicit assumptions

Use SPARQL 1.1 property paths to find asserted broader-link ancestors without requiring precomputed closure:

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT DISTINCT ?concept ?ancestor
WHERE {
  ?concept skos:broader+ ?ancestor .
}
```

A cycle can make `?concept` equal `?ancestor`; decide whether to flag or exclude that result. This path follows only `skos:broader` triples available in the dataset. If the graph stores narrower links, mapping links, or only broaderTransitive links, enable appropriate entailment or adapt the query. Avoid describing a query as complete without stating its graph and inference assumptions.

For preferred-label checks, group by resource and normalized language tag, count distinct literals, and flag counts above one. Check the untagged case explicitly under the selected RDF/SKOS profile. For lexical overlap, compare RDF literal identity, not just lowercased strings. Search normalization and semantic integrity use different equality rules.

## Test meaningful transformations

After migration, compare concept counts, mapping counts, language distributions, and source-to-IRI correspondence. Validate RDF lists for one first/rest chain, termination, and the intended sequence. Exercise a label rename, a concept split, and a new parent relation. Ensure historical indexed documents still resolve.

Keep errors attached to source locations and target IRIs. An automated fix must preserve a review trail: choosing one of two preferred labels changes editorial meaning. Report exactly which parser, shape set, entailment regime, and sample size were used. The [SKOS Reference](https://www.w3.org/TR/skos-reference/) defines integrity; [SPARQL 1.1](https://www.w3.org/TR/sparql11-query/#propertypaths) defines query paths. Neither guarantees that an editorial vocabulary is useful.
