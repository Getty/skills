# Hierarchies, mappings, and collections

## Keep direct links and reachability distinct

For `child skos:broader parent`, the object is broader than the subject. `skos:narrower` is its inverse. SKOS's customary use keeps immediate hierarchical links in these properties. The properties themselves are not transitive. Given child-to-parent and parent-to-root links, SKOS entails child-to-root through `skos:broaderTransitive`, not an additional `skos:broader` edge.

Do not silently expand direct links into all ancestors when building a tree widget or exporting an editorial crosswalk. The extra edges erase which parent assignments were asserted. Keep a direct-edge view and a separately described closure. A hierarchy can contain several parents and alternative paths. If a consumer requires a tree, select a documented projection and report omitted parents.

SKOS does not formally prohibit hierarchy cycles. An acyclicity requirement is a useful local policy for many taxonomies; classify it accordingly. A traversal implementation must still track visited nodes and bound expansion. Do not rely on a promised tree to prevent infinite traversal of imported data.

Use `skos:related` for associative links. It is symmetric and disjoint with hierarchical reachability through `skos:broaderTransitive`. Therefore an associative relation can conflict with an indirect ancestor relation, even if the same pair has no direct broader edge. Check both hierarchy directions because of symmetry and inverse relations.

## Select cross-scheme relationships by meaning

| Predicate | Interpretation and consequence |
| --- | --- |
| `skos:exactMatch` | Strong retrieval interchangeability; symmetric and transitive; implies close match |
| `skos:closeMatch` | Suitable interchangeability in some retrieval contexts; symmetric, not transitive |
| `skos:broadMatch` | Target is broader; specializes `skos:broader` |
| `skos:narrowMatch` | Target is narrower; inverse of broad match |
| `skos:relatedMatch` | Associative mapping; symmetric; specializes `skos:related` |

Prefer mapping properties for alignments between schemes. Their use does not enforce different schemes as a formal membership constraint. Preserve source and target scheme versions, the mapping author, rationale, review state, and relevant usage context outside the bare link if they matter.

Do not use `skos:exactMatch` as a generic “probably the same thing” link. Its closure can join a large network, and it is disjoint with broad and related mappings between the same pair; inverse relations extend the consequence to narrow mappings. Inspect definitions, granularity, temporal scope, and intended retrieval tasks before acceptance. Symmetry and transitivity can also entail self-matches; these are not automatically SKOS integrity violations.

Do not convert exact match into `owl:sameAs`. OWL identity can propagate every applicable property, whereas SKOS mappings support concept alignment. There is also no general SKOS rule that chains an exact match with a broad match to produce a new broad match. Such expansion must be named as an application rule and reviewed for false positives.

## Group without creating a new subject

Use `skos:Collection` for a meaningful grouping, such as concepts selected for a menu or editorial task. Use `skos:member` for concepts or nested collections. Membership does not itself introduce hierarchical, associative, or scheme-membership relations.

Use `skos:OrderedCollection` with `skos:memberList` when order is part of the grouping. RDF list members also entail ordinary collection members. Preserve list sequence and terminate lists properly; serialization order of ordinary triples is irrelevant. A collection is disjoint from both a concept and a concept scheme. Do not turn a menu heading into a broader concept unless it actually has the intended subject meaning.

Synthetic Turtle example:

```turtle
@prefix ex: <https://example.org/vocab/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

ex:transport a skos:Concept .
ex:rail a skos:Concept ; skos:broader ex:transport .
ex:water a skos:Concept ; skos:broader ex:transport .
ex:menu a skos:OrderedCollection ;
    skos:memberList ( ex:water ex:rail ) .
```

This creates two direct child concepts and a presentation order. It does not assert that water transport is broader than rail transport, or that the collection is a new topic.

Use the [SKOS semantic-relations](https://www.w3.org/TR/skos-reference/#semantic-relations), [mapping](https://www.w3.org/TR/skos-reference/#mapping), and [collection](https://www.w3.org/TR/skos-reference/#collections) sections to resolve entailments. The editorial acceptance and traversal recommendations are implementation guidance.
