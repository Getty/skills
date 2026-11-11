# Mapping and extension workflow

## Begin with the source meaning

Inventory each source field or relationship as a proposition. Record its subject, object or value, units, scope, timing, and source authority. Ask what a null means and whether the record is a current state, event, estimate, or assertion. A field named `issuer` may contain a legal name, a role identifier, a parent-company label, or a vendor key. These require different mappings.

Construct a crosswalk with columns for source element, source definition, representative values, target term IRI, mapping strength, transformation, lost information, and evidence. Treat unresolved meaning as an explicit result. Do not convert ambiguity into a guessed ontology term simply to fill every cell.

## Select mapping strength

| Mapping choice | Appropriate use | Required caution |
|---|---|---|
| Documented correspondence | Shared terminology or a tentative alignment | State the differences and scope |
| Subclass or subproperty | Every source member or relationship satisfies the broader target | Check inherited restrictions and direction |
| Equivalent class or property | Meanings coincide under the intended interpretation | Review both directions of entailment |
| Instance typing | A particular item satisfies a class definition | Preserve the evidence for classification |
| Instance identity | Two IRIs denote the same thing | Assess all consequences of `owl:sameAs` |
| Transformation | The source represents a target through a conversion or decomposition | Record reversible and lossy steps |

OWL equivalence and identity change logical conclusions. They are not confidence scores. See [OWL 2 semantics](https://www.w3.org/TR/owl2-direct-semantics/) for the formal commitments. Use an ordinary mapping record instead when you mean “likely related,” “close in business usage,” or “equivalent only for this report.”

## Decompose overloaded records

Consider a fictional row containing company name, ISIN, ticker, exchange, and last price. Design at least the distinctions the question requires: an entity; an instrument; an identifier assignment; a venue or listing; and a dated price observation. Do not make one individual both the company and its shares because the source presents them on one row.

Preserve source keys and their namespaces. Record the resolution evidence connecting each part. If two rows carry the same issuer but different instruments, merge neither instrument automatically. If two venues quote the same instrument, avoid generating duplicate issuers merely because the symbols differ.

Make a mapping trace readable in business language: “This source column identifies the bearer of an issuer role; this other column identifies the instrument.” A reviewer should be able to assess that statement without knowing RDF syntax.

## Extend without redefining upstream terms

Create local classes or properties in a namespace controlled for the application or organization. Import the upstream ontologies and add only justified axioms. Use a broader verified FIBO class when a narrower local category is needed. If the relation is not safely a subclass, document a mapping rather than asserting one.

Write a local definition that identifies distinguishing conditions. Include positive, boundary, and negative examples. Avoid defining a local class solely through a source system's field name. If a category is jurisdiction-specific, put the relevant qualification in its definition and data model.

Keep application validation rules separate from ontology definitions. A system may require every issuer record to include an LEI even though the broader domain model permits issuers without one. Express that requirement as a profile or validation rule; do not alter the global meaning of issuer.

## Preserve information through exchange

For a semantic export, specify the supported subset and how identifiers, datatypes, language tags, blank nodes, role occurrences, and qualified relationships are represented. If exporting to a simpler table or JSON object, state which distinctions are flattened and retain keys for reconstruction.

For a round trip, check meaning rather than byte equality. Reordered triples and different local blank-node labels need not change the graph. Dropped role scopes, units, or source evidence do. Establish invariant questions such as “Which entity bears this issuer role?” and compare answers before and after conversion.

## Review the proposal

Deliver a mapping with unresolved cases and evidence, not just generated triples. Include the chosen release, transformation assumptions, confidence where appropriate, validation results, and examples of rejected matches. Obtain domain review when classification depends on substantive legal or accounting interpretation. A syntactically valid ontology cannot supply missing business facts.
