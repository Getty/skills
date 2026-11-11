---
name: financial-identifiers
description: "Use when selecting, validating, looking up or reconciling financial identifiers — LEI and GLEIF, ISIN, MIC, CFI, FISN, tickers, entity vs instrument vs listing, checksums, lifecycle changes, licensing."
---

# Financial Identifiers

## Establish what is being identified

Start with the object, then choose the identifier. A legal entity, a financial instrument, a market, a listing, and a classification are different things. LEI addresses entity identity; ISIN addresses instrument identity; MIC identifies markets and related facilities; CFI classifies instruments; FISN supplies a standardized short description. A ticker must be interpreted within the relevant market or provider and time. Read [selection and boundaries](references/selection-and-boundaries.md) before designing a crosswalk.

Use this skill as a standalone standards guide. Do not assume a particular asset class, jurisdiction, application, programming language, or database. Separate stable structural knowledge from current registry facts and rules that depend on a filing or trading context.

## Navigate the references

- Read [selection and boundaries](references/selection-and-boundaries.md) for a comparison of schemes and common identity mistakes.
- Read [LEI and relationships](references/lei-and-relationships.md) for GLEIF records, statuses, parent relationships, exceptions, and lookup methods.
- Read [ISIN, CFI, and FISN](references/instrument-identifiers.md) for instrument identification, classification, names, assignment, and corporate-action considerations.
- Read [MIC and tickers](references/markets-and-tickers.md) for operating versus segment MICs, listing context, historical mapping, and venue distinctions.
- Read [resolution and validation](references/resolution-and-validation.md) for a repeatable matching workflow, checksum procedures, evidence records, and quality checks.
- Read [primary sources](references/sources.md) for registration authorities, dated version observations, and current-check guidance.

## Follow the resolution workflow

1. **Define the question and date.** Decide whether the user needs a definition, a format check, a current lookup, a historical mapping, or assignment guidance. Identify whether “company” means a legal entity, group, fund, branch, issuer, or brand. Identify the instrument and listing granularity.
2. **Preserve the input.** Retain the original value, its asserted scheme, provider, jurisdiction or venue, and observation date. Apply only scheme-appropriate normalization. Keep leading zeros and meaningful ticker punctuation.
3. **Check structure.** Validate length, character repertoire, and checksum where the scheme defines one. Label the result as structural validity. Never claim that a check digit proves an identifier was assigned or that it denotes the intended subject.
4. **Consult the authority.** Use GLEIF for LEI records, the ISO 10383 registration authority for MICs, and ANNA or the responsible numbering agency for instrument reference data. Use official issuer or venue records to establish the requested relationship. Inspect current terms before bulk retrieval or redistribution.
5. **Compare the subject.** Check legal name, registration authority identifier, jurisdiction, instrument terms, market segment, and relevant dates. Account for aliases, transliteration, parent/subsidiary differences, share classes, and corporate actions. Prefer a documented match over a name similarity score.
6. **Preserve relationship meaning.** Record whether a mapping means issuer-of, listed-on, parent-of under an accounting framework, or same-entity. Keep direction, date, source, and uncertainty. Do not present a cross-type relationship as identifier equivalence.
7. **Return an assessable result.** State the resolved object, identifier scheme and value, authoritative source, lookup date, relevant status, and remaining ambiguity. For bulk work, provide the matching policy and counts by outcome, including unresolved cases.

## Apply guardrails to interpretation

Treat LEI registration status separately from entity status. Treat an ISIN's prefix separately from the issuer's domicile, trading currency, and listing venue. Treat a MIC's publication date separately from the effective date of its changes. Treat a CFI or FISN as descriptive data rather than a unique replacement for an ISIN.

Do not fill an unknown identifier by manufacturing a code that passes a checksum. Do not infer universal regulatory obligations from the existence of an international standard. Recheck the relevant authority and jurisdiction before stating required identifiers, current statuses, API behavior, fee arrangements, or redistribution rights.
