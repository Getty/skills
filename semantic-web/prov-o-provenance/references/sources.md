# Authoritative sources and limits

The core documents below are the W3C publications of 30 April 2013. Distinguish Recommendations from Working Group Notes. Check linked errata when exact behavior matters.

| Source | Use |
| --- | --- |
| [PROV Overview](https://www.w3.org/TR/prov-overview/) | Family map and normative status; Working Group Note |
| [PROV-DM](https://www.w3.org/TR/2013/REC-prov-dm-20130430/) | Normative conceptual data model: entity, activity, agent, influence, bundles, and alternate views |
| [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) | Normative RDF/OWL vocabulary, qualified patterns, and domain/range details |
| [PROV Constraints](https://www.w3.org/TR/2013/REC-prov-constraints-20130430/) | Normative inferences, normalization, validity, uniqueness, typing, and event-order constraints |
| [PROV Primer](https://www.w3.org/TR/prov-primer/) | Explanatory examples; Working Group Note |
| [PROV-N](https://www.w3.org/TR/prov-n/) | Recommendation defining the provenance notation |
| [PROV-XML](https://www.w3.org/TR/prov-xml/) | XML mapping and schemas; Working Group Note |
| [PROV-AQ](https://www.w3.org/TR/prov-aq/) | Access and discovery mechanisms; Working Group Note |
| [PROV-Links](https://www.w3.org/TR/prov-links/) | Linking descriptions across bundles; Working Group Note |
| [PROV-Dictionary](https://www.w3.org/TR/prov-dictionary/) | Optional keyed-collection extension; Working Group Note |
| [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/) | Graph queries and property paths |

Do not use early Working Draft property names when the Recommendation supplies a different term. For example, use the final `prov:qualifiedDelegation` pattern rather than obsolete draft responsibility terminology. Treat the `http://www.w3.org/ns/prov#` namespace as the vocabulary identity even when documentation is fetched over HTTPS.

The bundled guidance is original synthesis with synthetic examples. It offers practical capture and modeling choices without prescribing storage or a particular validator. Syntax-valid examples are not a full conformance suite. Tooling may implement only a subset of the PROV family, and validation of a closed application profile may impose requirements absent from the standard.

No standard source here provides a universal trust score, confidence semantics, rights grant, or automatic guarantee that recorded history is true. Evaluate those claims through separate evidence and explicitly defined policies.
