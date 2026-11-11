# Primary sources and freshness

Use the sources below for definitions and technical authority; treat workflow advice and invented examples in this skill as original synthesis.

| Source | Use |
|---|---|
| [EDM FIBO home](https://spec.edmcouncil.org/fibo) | Purpose, governance, formats, and official navigation |
| [Official FIBO repository](https://github.com/edmcouncil/fibo) | Actual ontology files, domain inventory, history, and license notices |
| [Release notes](https://spec.edmcouncil.org/fibo/release-notes) | Release-specific changes; check freshness against the chosen artifact |
| [Ontology tree](https://spec.edmcouncil.org/fibo/ontology/master/latest/tree.html) | Locate modules; moving publication, not an immutable pin |
| [Legal persons](https://github.com/edmcouncil/fibo/blob/master/BE/LegalEntities/LegalPersons.rdf) | Business entities and reuse of Commons legal concepts |
| [Financial instruments](https://github.com/edmcouncil/fibo/blob/master/FBC/FinancialInstruments/FinancialInstruments.rdf) | Instruments, securities, issuer role, and restrictions |
| [Securities listings](https://github.com/edmcouncil/fibo/blob/master/SEC/Securities/SecuritiesListings.rdf) | Listing terms and relationship axioms |
| [Securities identification](https://github.com/edmcouncil/fibo/blob/master/SEC/Securities/SecuritiesIdentification.rdf) | Identifier classes and scopes |
| [Securities issuance](https://github.com/edmcouncil/fibo/blob/master/SEC/Securities/SecuritiesIssuance.rdf) | Offerings, underwriting, and issuance terminology |
| [Import catalog](https://github.com/edmcouncil/fibo/blob/master/catalog-v001.xml) | Logical-IRI to artifact resolution |
| [OMG FIBO BE 1.1](https://www.omg.org/spec/EDMC-FIBO/BE/1.1/About-BE) | A specific adopted OMG domain publication |
| [OWL 2 primer](https://www.w3.org/TR/owl2-primer/) | Modeling and open-world interpretation |
| [OWL 2 structure](https://www.w3.org/TR/owl2-syntax/) | Ontology identifiers, imports, and axiom forms |
| [OWL 2 direct semantics](https://www.w3.org/TR/owl2-direct-semantics/) | Logical consequences of identity and equivalence |
| [SHACL Recommendation](https://www.w3.org/TR/shacl/) | Explicit RDF data validation |

The RDF sources were inspected directly from the official repository; some ontology URLs present a JavaScript viewer rather than machine-readable content. The inspected master commit was `33a92cd34285d532c158da97bb42add089f135d3`. Replace `master` in repository links with that commit when reconstructing the exact inspection, or select a newer appropriate release deliberately. Do not conflate successful web navigation with successful ontology loading.
