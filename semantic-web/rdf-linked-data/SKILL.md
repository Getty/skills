---
name: rdf-linked-data
description: "Use when modeling, parsing, publishing or debugging RDF — triples, IRIs, blank nodes, literals and datatypes, RDFS, Turtle, TriG, N-Triples, N-Quads, named graphs, Linked Data, RDF 1.1 vs 1.2."
---

# RDF and Linked Data

Use RDF to express statements with globally identifiable terms and to exchange graph-shaped information across independently designed systems. Explain the data model before selecting a file format or database. Keep four concerns visible: what a statement means, how identifiers are assigned, which graph contains it, and how the statement is serialized.

Use the RDF 1.1 Recommendations as the interoperability baseline unless the task explicitly selects RDF 1.2 and the participating tools support the required features. Each RDF 1.2 document carries its own publication status; read it from the document and do not describe the entire family as a completed Recommendation. Consult [sources and versions](references/sources.md) for the links.

## Navigate the reference material

Read the relevant reference directly; none requires another installed skill.

- [Data model and identity](references/data-model.md): triples, graphs, datasets, term identity, blank nodes, literals, lists, and information that RDF does not supply automatically.
- [Vocabularies and entailment](references/vocabularies-entailment.md): RDFS classes and properties, domain/range inference, vocabulary reuse, datatypes, and reasoning boundaries.
- [Serializations and conversion](references/serializations.md): complete original examples, media types, parsing choices, graph-preserving conversion, and RDF 1.2 compatibility.
- [Linked Data publication](references/linked-data-publication.md): identifier design, dereferencing, content negotiation, descriptions, linking, and lifecycle decisions.
- [Inspection and interoperability](references/inspection-interoperability.md): a practical workflow for importing, comparing, merging, debugging, and checking RDF artifacts.
- [Sources and versions](references/sources.md): primary specifications and their roles, with a dated status snapshot.

## Establish the task

Identify whether the requested deliverable is an explanation, vocabulary, instance dataset, conversion, publication plan, or diagnosis. For an explanation, use a small concrete example and describe the meaning of each term. For a data task, inspect a representative sample and the consuming system before choosing assumptions.

Record the expected RDF version, serialization, base IRI, encoding, graph arrangement, datatype policy, and any entailment regime. Ask a question only if a material choice cannot be inferred; otherwise state the assumption and proceed. An input named `.rdf`, `.ttl`, or `.owl` is evidence about format, not proof of it.

## Model the intended information

1. Give reusable entities stable IRIs. Keep labels and external identifiers as data; a label is not identity.
2. Choose predicates whose definitions match the intended relation. Reuse authoritative terms after checking their meaning and version.
3. Use literals for values and IRIs for links. Preserve datatype and language information, including lexical distinctions needed by the task.
4. Use blank nodes for unnamed structure when a stable external identity is unnecessary. Do not use a parser-generated blank-node label as a durable record key.
5. Introduce an explicit relation or observation node when time, participants, quantities, or evidence belong to a relationship. Do not overload one binary predicate with incompatible meanings.
6. Choose a graph/dataset layout deliberately. A named graph name does not automatically establish its source, author, truth, access policy, or time interval.

## Process with explicit semantics

Parse using an RDF-aware parser and an explicit format. Preserve the base IRI and dataset boundaries. Compare graphs by their RDF terms and blank-node structure, not serialized order. A graph is a set of triples, so repeated identical statements are not separate observations.

Distinguish syntax acceptance, well-formed literal values, vocabulary conformance, entailment, and application validation. RDFS domain and range axioms can add types; they do not reject records with unexpected types or missing fields. Use an explicit validation contract if required values, cardinalities, or closed records matter.

Keep asserted data separate from derived statements when traceability matters. State whether query answers include only explicit triples or also consequences of a specified reasoning regime. Do not infer source reliability or legal identity merely because two datasets use the same IRI.

## Verify and deliver

Perform checks proportional to the operation: parse a new artifact, inspect a few expanded terms, compare before/after graphs for a conversion, and verify named-graph membership for a dataset. For a merge, check blank-node scoping and identifier collisions. For publication, check both the identifier and the returned representation.

Deliver the requested artifact or explanation together with the assumptions that affect meaning. Report observed validation separately from untested support. Explain any dropped graph boundaries, changed identifiers, datatype coercion, unsupported RDF 1.2 features, or external retrieval dependencies. Avoid claiming that a successful parse establishes semantic correctness.
