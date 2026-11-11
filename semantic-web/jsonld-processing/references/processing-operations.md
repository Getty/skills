# Processing operations and their guarantees

## Expansion

Expand a document to remove compact aliases and many context-driven shortcuts. Inspect full predicate/class IRIs, node identifiers, arrays, and explicit value objects. Expansion is the most useful first diagnostic for an unexpected graph.

Do not call expanded JSON-LD a canonical representation. Property ordering, blank-node labels, node organization, and processing options can still differ. Expansion can discard unmapped terms and null values according to the standard; a successful call therefore does not prove preservation of every JSON key.

## Compaction

Compact expanded information using a selected context. The processor chooses terms and compact structures based on that context and algorithm rules. Equivalent contexts can produce different JSON layouts. Arrays may compact to scalars unless containers or options retain arrays.

Treat compacted output as an interface representation. If downstream code expects fixed keys, singleton arrays, or embedded objects, define and verify those requirements explicitly. Compaction is not arbitrary schema transformation: it does not compute new domain facts or guarantee the exact tree shape of the original input.

## Flattening

Flatten to organize descriptions into node objects keyed conceptually by their identifiers and graph membership. This reduces the need to traverse arbitrary nesting and can simplify indexing or merging. It does not mean concatenating all named graphs into the default graph.

Flattening may introduce or expose blank-node identifiers. Their spelling is processor-local, not a stable identity scheme. Named graphs and list structures still need correct interpretation. Use the flattening API's context option if a compacted flattened form is desired, and verify the resulting layout against the consumer's expectations.

## Framing

Frame when an application needs a tree-oriented view over a graph. A frame describes matching and embedding preferences. Options such as embedding behavior, explicit property selection, and whether all specified conditions must match affect the result. Frame an original small dataset before committing to a public response shape.

A frame can omit unrelated nodes or properties, and defaults can affect presented values. Therefore a framed result is not automatically a complete export or a validation result. A record's absence may reflect frame matching rather than absence from the source graph. Do not use framing defaults to manufacture evidence that a source supplied a value.

## Conversion to and from RDF

Use the standard conversion algorithms when exchanging with RDF tools. Set the relevant options, including handling of generalized RDF or text direction where supported. Standard RDF 1.1 requires IRI predicates; a generalized-RDF option can permit structures that ordinary RDF stores cannot accept.

Converting to RDF discards JSON presentation choices: key order, aliases, nesting choices, and some indexes are not graph statements. Empty graph containers may lack a representation in a quad stream. Converting back does not reconstruct those original choices without an additional application contract.

Native JSON numeric handling and typed-literal normalization can affect lexical round trips. Lists, `rdf:JSON`, language/direction handling, blank nodes, and graph names deserve targeted examples if used. A dataset-aware comparison is stronger than comparing one merged graph.

## Select an invariant

| Goal | Suitable check |
| --- | --- |
| Preserve an API's exact field layout | JSON-level structural comparison |
| Verify context mappings | Inspect expanded terms and values |
| Preserve RDF information | Compare datasets including graph membership and blank-node structure |
| Produce deterministic cryptographic input | Apply a specified canonicalization and cryptographic suite |
| Check required domain data | Run an explicit validation contract |

Do not substitute one row's check for another. A graph-equivalent result may break an API client, while a JSON-looking equivalent may silently change IRIs.

The [Processing Algorithms and API](https://www.w3.org/TR/json-ld11-api/) defines the transformations; [Framing](https://www.w3.org/TR/json-ld11-framing/) defines its separate view-building operation. Consult the exact processor release for API names rather than assuming identical interfaces across implementations.
