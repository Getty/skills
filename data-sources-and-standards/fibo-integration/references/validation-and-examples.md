# Validation and original examples

## Read the example as a partial assertion graph

This invented example demonstrates the checked issuer-role pattern. It is deliberately partial: it does not supply every fact implied by the imported ontology, nor claim to be a complete reporting profile.

```turtle
@prefix ex: <https://example.org/demo/> .
@prefix fin: <https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/FinancialInstruments/> .
@prefix rel: <https://spec.edmcouncil.org/fibo/ontology/FND/Relations/Relations/> .
@prefix org: <https://www.omg.org/spec/Commons/Organizations/> .
@prefix role: <https://www.omg.org/spec/Commons/RolesAndCompositions/> .

ex:NorthHarbor a org:LegalEntity .
ex:IssuerRoleA a fin:Issuer ;
    role:isPlayedBy ex:NorthHarbor .
ex:BondA a fin:Security ;
    rel:isIssuedBy ex:IssuerRoleA .
```

The class and property locations follow the [financial-instrument source](https://github.com/edmcouncil/fibo/blob/master/FBC/FinancialInstruments/FinancialInstruments.rdf). Prefixes are abbreviations; their declarations do not import the referenced ontologies. A complete executable setup must separately load the selected import closure.

An illustrative query over the explicit assertions is:

```sparql
PREFIX fin: <https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/FinancialInstruments/>
PREFIX rel: <https://spec.edmcouncil.org/fibo/ontology/FND/Relations/Relations/>
PREFIX role: <https://www.omg.org/spec/Commons/RolesAndCompositions/>
SELECT ?instrument ?entity WHERE {
  ?instrument a fin:Security ; rel:isIssuedBy ?issuerRole .
  ?issuerRole role:isPlayedBy ?entity .
}
```

Specify whether queries include inferred types. A query requiring an explicit type can miss instances known only through subclass entailment. Conversely, adding a reasoner can reveal consequences of strong mappings that were invisible in a simple triple-store query.

## Separate logical and operational checks

OWL uses an open-world interpretation: missing assertions do not generally prove their negation. It also does not impose a global unique-name assumption. Consequently, a minimum-cardinality restriction need not generate a missing-field error, and two identifiers need not denote distinct individuals merely because their strings differ. Read the [OWL 2 primer](https://www.w3.org/TR/owl2-primer/) for these interpretation rules.

Use separate checks for separate questions:

1. **Syntax:** Can the RDF document be parsed without changing identifiers or datatypes?
2. **Resolution:** Are every required ontology and external dependency present?
3. **Logical consistency:** Can the axioms and assertions be jointly satisfied? Are relevant classes satisfiable?
4. **Data contract:** Are required evidence, identifiers, values, and cardinalities present under the application's rules?
5. **Business correctness:** Do source records justify the roles, relationships, and classifications?
6. **Fitness for use:** Do the competency questions yield the expected answers with the declared entailment regime?

A [SHACL](https://www.w3.org/TR/shacl/) shape can express graph validation expectations, but it does not replace the source evidence or automatically reproduce all OWL reasoning. Declare how inference is applied before validation.

## Use counterexamples

Test a company and a similarly named subsidiary; an issuer and a guarantor; an instrument and an underlying instrument; one security with multiple listings; two identifiers from different schemes with the same lexical value; a historical ownership assertion; and an unresolved identity match. These cases expose mistaken merges that a clean positive example may conceal.

For an OWL consistency problem, isolate a small set of responsible axioms and assertions. Explain whether the issue originates in the source data, mapping, local extension, version combination, or upstream ontology. Do not “fix” the problem by deleting disjointness or changing domains until the business meaning has been examined.

## Define acceptance evidence

A useful handover includes the exact version manifest, term inventory, original sample assertions, expected query results, unresolved mappings, and a record of logical and data validation outcomes. Record assumptions about time, identity, and completeness. State limitations precisely: an unverified identity, missing dependency, or unsupported entailment mode is more informative than a blanket claim that the model is validated.
