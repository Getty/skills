# Terms and modeling patterns

## Verify exact identifiers

The examples below come from the official FIBO source. They are navigation aids, not a promise that every release uses the same terms. Inspect the chosen release's definitions and imports before generating production assertions.

| Meaning | Verified term IRI |
|---|---|
| Business entity | `https://spec.edmcouncil.org/fibo/ontology/BE/LegalEntities/LegalPersons/BusinessEntity` |
| Financial instrument | `https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/FinancialInstruments/FinancialInstrument` |
| Security | `https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/FinancialInstruments/Security` |
| Issuer role | `https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/FinancialInstruments/Issuer` |
| Listing | `https://spec.edmcouncil.org/fibo/ontology/SEC/Securities/SecuritiesListings/Listing` |
| ISIN identifier class | `https://spec.edmcouncil.org/fibo/ontology/SEC/Securities/SecuritiesIdentification/InternationalSecuritiesIdentificationNumber` |
| Ticker identifier class | `https://spec.edmcouncil.org/fibo/ontology/SEC/Securities/SecuritiesIdentification/TickerSymbol` |

Sources: [legal persons](https://github.com/edmcouncil/fibo/blob/master/BE/LegalEntities/LegalPersons.rdf), [financial instruments](https://github.com/edmcouncil/fibo/blob/master/FBC/FinancialInstruments/FinancialInstruments.rdf), [listings](https://github.com/edmcouncil/fibo/blob/master/SEC/Securities/SecuritiesListings.rdf), [identification](https://github.com/edmcouncil/fibo/blob/master/SEC/Securities/SecuritiesIdentification.rdf).

## Keep entity and role separate

In the checked baseline, legal entity and legal person vocabulary is reused from OMG Commons, including `https://www.omg.org/spec/Commons/Organizations/LegalEntity` and `.../LegalPerson`. Do not manufacture older FIBO equivalents from memory. FIBO's [LegalPersons source](https://github.com/edmcouncil/fibo/blob/master/BE/LegalEntities/LegalPersons.rdf) imports and references Commons terms.

Model an issuer as a role with a bearer when following the FIBO pattern. The checked financial-instrument ontology relates issuer roles to instruments and uses Commons `RolesAndCompositions/isPlayedBy`. A company can play different roles in different relationships; an issuer, guarantor, investor, custodian, and parent need not be the same party. A corporate group name is insufficient evidence for all of them. See the [Issuer axioms](https://github.com/edmcouncil/fibo/blob/master/FBC/FinancialInstruments/FinancialInstruments.rdf).

Create an identity for the durable entity and a separate role occurrence where the model requires one. Preserve the role's scope through its instrument or agreement relationships. Add local time and evidence structures only with documented semantics; do not pretend a generic date property establishes the whole validity interval.

## Separate instrument, issue, offering, and listing

Use the source definition to determine whether an input describes contractual terms, an issued instrument, an offering, or an exchange-specific catalog entry. “Security” is broader than “exchange-listed share.” Do not classify a security as listed merely because it has an identifier or appears in a vendor database.

The checked [listing ontology](https://github.com/edmcouncil/fibo/blob/master/SEC/Securities/SecuritiesListings.rdf) includes `ListedSecurity`, `Listing`, `isListedVia`, `lists`, and `isTradedOn`; inspect their domains, ranges, inverse relationships, and restrictions together. An exchange's security page and a market-data observation are not automatically the listing object itself. Read the accompanying offering restrictions before choosing a simplified relationship.

For a multi-venue security, preserve a shared instrument identity and distinguish listing records, venue identifiers, local symbols, quote currencies, and validity periods as the source requires. Model a depositary receipt separately from its underlying shares unless authoritative evidence supports the exact relationship. Economic exposure does not establish identity.

## Treat identifiers as identifiers

The identification ontology distinguishes security identifiers and listed-security identifiers. This supports an essential modeling check: what does the identifier designate, under which scheme, authority, and period? A literal ticker lacks enough context for global identity. An ISIN does not identify the issuer itself.

Keep identifier values, schemes, and assignment evidence available even if the application also uses a compact IRI. Do not infer legal ownership from an identification relationship. When resolving two records, document the evidence for identity separately from the vocabulary used to describe their type.

## Preserve qualified relationships

A statement that entity A owns entity B loses information if ownership concerns a specific interest, percentage, voting right, or interval. A statement that a loan has a rate loses information if the rate resets against an index with a spread and schedule. Begin with the business proposition and identify the participating objects before choosing predicates.

Use a local assertion record when the evidence concerns a claim about a relationship rather than an unqualified timeless fact. Retain source, observation time, effective time, and confidence as distinct attributes where relevant. This is an application modeling recommendation, not a claim that FIBO mandates one universal provenance design.
