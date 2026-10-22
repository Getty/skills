# Jurisdiction adapters

## Reuse EU reasoning without exporting German law

EU regulations generally apply directly, but opening clauses, national enforcement, sanctions and procedural rules can matter. Directives require examination of national implementation. EEA incorporation and timing require separate verification. Switzerland and the United Kingdom need separate regimes; an English interface or English contract does not make English law the baseline.

Identify the establishment of each relevant actor, where customers are habitually resident, countries actively targeted, affected-person locations, sector regulators and cross-border data flows. Geolocation is an imperfect signal, not a legal classification engine.

For consumer contracts, assess Rome I Article 6 and its conditions: a choice-of-law clause does not simply remove otherwise applicable mandatory consumer protection. VAT place-of-supply and GDPR establishment questions are different tests. Do not reuse one 'country' field for all legal purposes.

## German adapter included by this collection

The specialist references identify BDSG, TDDDG, UWG, BGB/EGBGB, PAngV, DDG, BFSG/BFSGV, BSIG, KI-MIG, UrhG, GeschGehG, UStG/AO/HGB and relevant youth/workplace rules. The list identifies areas to evaluate; it is not an assertion that every provision applies to every platform.

Retain distinctions such as Widerruf, Kündigung, Löschung, Sperrung, Auftragsverarbeitung, gemeinsame Verantwortlichkeit and Geschäftsgeheimnis. Use national-law citations in their official format and provide a brief English meaning. Do not translate different legal acts into a shared ambiguous 'cancel' event.

## Adapter for another Member State

Create a separate versioned adapter with:

1. Jurisdiction and territorial assumptions; language and official source portals.
2. National GDPR opening-clause rules: DPO thresholds, employment, children and procedural details.
3. ePrivacy implementation, marketing channels and regulator positions.
4. Consumer-law transposition, renewal/cancellation/withdrawal interfaces, ADR and mandatory disclosures.
5. Accessibility implementation and responsible authority.
6. NIS2 implementation, registration/reporting rules and competent CSIRT/authority.
7. AI Act authority allocation and procedural law.
8. National copyright, employment, youth/media and sector-specific dependencies.
9. Tax, invoice, retention, payment and local accounting requirements.
10. Sources, checked dates, unresolved conflicts, expert review and next refresh.

A missing adapter blocks reliance on that country's national exemptions. It need not block work on EU-wide security or data minimisation controls whose applicability is established. Use a targeted decision: what can safely proceed and what cannot yet be claimed.

## Interface localisation

Localise disclosure language, time and date formatting, pricing presentation, supported contact methods and accessible labels. Preserve the legal version accepted by each customer and the rendered interface version. A single English privacy notice may be insufficient for a market's intended users; assess clarity and accessibility rather than asserting a universal translation rule.

Store `governing_law`, `consumer_habitual_residence`, `market_target`, `vat_location`, `data_subject_location` and `data_hosting_region` as distinct concepts where actually necessary. Collect only evidence proportionate to the relevant obligation.
