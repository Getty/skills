# LEI, GLEIF, and relationship records

## Understand the identifier

An LEI is a 20-character alphanumeric identifier defined by ISO 17442. Eligibility extends beyond ordinary incorporated companies and includes specified other forms and international branches. Do not use LEI as a universal identifier for natural persons. Check the precise entity category and rules rather than inferring legal form from the code. See [ISO 17442-1](https://www.iso.org/standard/78829.html) and [GLEIF's overview](https://www.gleif.org/en/organizational-identity/lei-vlei/the-legal-entity-identifier-lei).

Treat the code as an opaque identifier for business reasoning. Its characters are not a reliable source of domicile, ownership, industry, or current managing issuer. A transferred LEI registration does not acquire a new identity merely because a different issuing organization manages it.

## Read the record at the right level

Level 1 reference data includes entity names, addresses, jurisdiction, registration information, and lifecycle data. Registration metadata describes the LEI record and its maintenance. Inspect both; do not collapse them into one “active” flag. The [LEI-CDF 3.1 specification](https://www.gleif.org/en/lei-data/access-and-use-lei-data/level-1-data-lei-cdf-3-1-format) defines these fields and status values.

For example, `LAPSED` indicates a registration not renewed by its renewal date under the stated criteria. It does not by itself mean the entity ceased business. `DUPLICATE`, `ANNULLED`, and `RETIRED` have different meanings. Follow the current format's successor and legal-entity-event information when resolving a corporate change; avoid treating deprecated status values as the entire lifecycle model.

Construct an entity comparison from authoritative registration identifiers and jurisdiction as well as names. Legal names can change. Transliteration and alternative names can help a search without proving a match. Addresses can be shared, historical, or administrative.

## Interpret Level 2 precisely

GLEIF's core parent relationships identify direct and ultimate **accounting consolidating parents**. The relationship definition and applicable accounting framework matter. They are not a comprehensive shareholding graph or a universal beneficial-owner register. See [Level 2 scope](https://www.gleif.org/en/lei-data/access-and-use-lei-data/level-2-data-who-owns-whom).

Read the direction of each relationship. In the [RR-CDF format](https://www.gleif.org/en/lei-data/access-and-use-lei-data/level-2-data-relationship-record-rr-cdf-2-1-format), `IS_DIRECTLY_CONSOLIDATED_BY` and `IS_ULTIMATELY_CONSOLIDATED_BY` run from the child toward the relevant parent. Other relationship types, including international-branch and fund-related relationships, have their own definitions. Do not turn every row into a generic `owns` edge.

A missing parent relationship is not proof of independence. Examine the [reporting-exceptions data](https://www.gleif.org/en/lei-data/access-and-use-lei-data/level-2-data-reporting-exceptions-2-1-format). Preserve the exception reason and whether it concerns direct or ultimate parent reporting. Do not replace an exception with a guessed parent or a null that hides the explanation.

## Choose an access method

Use interactive search for a small investigation, the [GLEIF API](https://www.gleif.org/en/lei-data/gleif-api) for targeted automated lookup, and documented bulk or delta files for larger refreshes. Check pagination, filters, response relationships, and current API documentation rather than inventing query parameters. Capture retrieval timestamps and retain the unmodified authoritative record where permitted.

Prefer the current authoritative data over an old cached name match. For historical questions, seek historical records or dated files and state the available temporal resolution. Do not assume today's parent relationship describes every earlier period.

## Preserve evidence and rights

GLEIF publishes LEI data under [CC0 terms](https://www.gleif.org/en/meta/lei-data-terms-of-use). Keep provenance even when attribution is not a license requirement, because auditability and correction still matter. Check service conditions, availability, and any third-party enrichment separately. Open LEI data does not confer rights to redistribute unrelated vendor datasets joined to it.

A useful result reports the code, entity name, relevant registry evidence, entity and registration statuses, lookup date, and exact relationship interpretation. State a candidate match as a candidate until the evidence resolves it.
