# Inspecting and interoperating with RDF

## Start from observable artifacts

Capture the input bytes or immutable source reference, declared format, base IRI, retrieval metadata, and tool version. Inspect a small portion before assuming that a file contains a single graph, a dataset, or a complete vocabulary. Check encoding and whether compressed input needs decompression before parsing.

Parse into an appropriate graph or dataset API. Preserve literal lexical forms if exact source reconstruction matters; some libraries normalize recognized datatype values when constructing literals. Parser success is evidence of syntactic acceptance by that implementation, not proof that every term is useful or every datatype value is valid.

For initial inspection, count triples, named graphs, predicates, classes, blank nodes, and datatype/language usage. These counts are diagnostics rather than universal quality scores. A graph with no explicit types may still be legitimate, and a graph with many types may still have incorrect identity modeling.

## Diagnose common discrepancies

| Symptom | Investigate |
| --- | --- |
| Same-looking entities do not join | Different expanded IRIs, source keys, case, base IRIs, or literal-versus-IRI objects |
| Triple counts shrink after import | Duplicate statements, graph-union policy, rejected input, literal normalization |
| Types appear unexpectedly | Domain/range rules, subclass closure, equality inference, store defaults |
| Records disappear from a query | Named-graph selection, default-graph policy, unsupported datatypes, optional-pattern filters |
| Round-trip text changes | Prefix allocation, statement order, blank-node labels, escaping, lexical normalization |
| A graph digest changes | Serialization choices, blank nodes, dataset selection, canonicalization version |

Reduce a discrepancy to a small graph that preserves the behavior. Avoid replacing every IRI or value if the problem involves namespace expansion, lexical form, or datatype comparison. Keep one expected statement and one counterexample in the reproduction.

## Merge without manufacturing identity

Standardize blank nodes apart when combining independent sources. A label `_:x` in two separately parsed documents does not make the nodes identical. Do not standardize apart nodes that were deliberately shared within a dataset. If the library exposes only per-graph parsing, verify its blank-node allocation policy before reconstructing a dataset.

Keep graph names distinct from source file paths unless the publication model intentionally equates them. Decide whether equal IRIs from different sources are accepted as the same resource, tracked as conflicting claims, or mapped through a resolution layer. Preserve source graphs when later attribution or rollback matters.

Treat duplicate values, statement multiplicity, and occurrence counts as separate concerns. If the source system records repeated list entries or repeated events, map those occurrences explicitly before collapsing data into a set of triples.

## Compare at the correct level

Use byte equality for an unchanged file, RDF graph isomorphism for graph-preserving transformations, and dataset-aware comparison for graph partitions. Semantic equivalence under RDFS or OWL is a different question: two non-isomorphic graphs can have the same relevant consequences under a chosen theory.

Canonicalization establishes a deterministic representation under its algorithm's assumptions. It does not verify factual correctness, collapse different IRIs that happen to identify the same thing, or compute all OWL consequences. Keep the digest algorithm, canonicalization version, graph selection, and source digest in a reproducibility record.

## Report evidence proportionately

For a simple conversion, parsing both outputs and comparing structure may be enough. For a migration, additionally compare representative queries, graph counts, datatype edge cases, and blank-node connections. For semantic changes, check intended and forbidden entailments using the actual reasoning configuration.

Report unsupported features precisely: for example, “named graphs were merged into one output graph” or “this parser accepts RDF 1.1 only.” Avoid generic claims of full RDF support when only one syntax or feature subset was exercised. Consult [RDF Test Cases](https://www.w3.org/TR/rdf11-testcases/) and the [RDF Dataset Canonicalization Recommendation](https://www.w3.org/TR/rdf-canon/) for the respective conformance boundaries.
