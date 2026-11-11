# Resolution, validation, and evidence

## Separate validation layers

Use a staged result rather than one boolean:

| Layer | Question | Possible result |
|---|---|---|
| Lexical | Does the string have the right form? | Well formed or malformed |
| Check digit | Does the checksum agree? | Passed, failed, or not applicable |
| Assignment | Does the authority recognize it? | Assigned, unconfirmed, or not found |
| Lifecycle | What is its status at the relevant time? | Current, historical, terminated, or uncertain |
| Subject match | Is it the object the user intended? | Confirmed, candidate, conflicting, or unresolved |
| Relationship | Does the requested crosswalk hold? | Evidence-supported or unestablished |

A valid checksum only detects some transcription errors. It cannot confirm assignment, existence, ownership, trading permission, or the intended entity. A real identifier can still be attached to the wrong record.

## Normalize conservatively

Preserve the raw input before normalization. Trim surrounding transport whitespace and apply uppercase where the scheme requires it. Keep leading zeros. Reject unexpected Unicode lookalikes rather than silently replacing them. Avoid stripping all punctuation from ticker symbols. Store identifiers as strings, never as numbers that can lose zeros or switch to scientific notation.

Record every repair proposal separately. If a check digit fails, offer a possible correction only as a candidate requiring authoritative lookup. Do not substitute a generated identifier into the source data without evidence.

## Apply check-digit procedures correctly

For an LEI structural check, expand letters using `A=10` through `Z=35`, preserving the original character order, and compute the resulting decimal number modulo 97. A conforming complete code has remainder 1 under ISO 7064 MOD 97-10, identified in the [LEI Regulatory Oversight Committee overview](https://www.leiroc.org/lei.htm). Implement the remainder incrementally to avoid large-integer limitations. Do not apply the IBAN step of moving initial characters to the end. Check the current [GLEIF technical materials](https://www.gleif.org/en/lei-data/access-and-use-lei-data/level-1-data-lei-cdf-3-1-format) when implementing a complete validator.

For an ISIN, expand alphabetic characters to decimal values and perform the Luhn check over the resulting digit string. Starting at the rightmost check digit, leave it unchanged and double every second digit to its left; sum the decimal digits of those results and require divisibility by 10. Validate the full format first. The algorithm must operate after alphabetic expansion, since expansion changes digit positions. ANNA describes this as the [modulus-10 Double-Add-Double check](https://anna-web.org/identifiers/). Confirm edge cases against authoritative examples before shipping code.

MICs, CFIs, FISNs, and tickers require their own syntax or vocabulary checks; do not apply LEI or ISIN algorithms to them. A six-letter CFI candidate needs valid code combinations, not merely six alphabetic characters.

## Match with explicit evidence

For an entity, compare registration authority, local registration identifier, legal jurisdiction, name, and relevant lifecycle facts. For an instrument, compare authoritative identifier assignment and terms. For a listing, add market, symbol, currency, and time. Keep the strongest evidence separate from convenient corroborating attributes.

Use official mapping files where appropriate. GLEIF and ANNA publish [ISIN-to-LEI relationships](https://www.gleif.org/en/lei-data/lei-mapping/download-isin-to-lei-relationship-files) connecting instruments and issuers. Treat their coverage and direction as documented; do not assume every ISIN or instrument type appears. A missing mapping can mean incomplete coverage rather than no issuer.

Classify conflicts before resolving them: source lag, different dates, different granularity, a corporate event, incorrect identifier, or genuine uncertainty. Preserve competing assertions when evidence is insufficient. A high fuzzy-match score should not erase contradictory registration or instrument data.

## Evaluate a matching process

Review a sample of accepted matches and difficult rejected cases. Include parent/subsidiary names, shared addresses, legal-name changes, non-ASCII names, multiple share classes, terminated instruments, reused symbols, and venue changes. Measure false merges separately from missed matches because their consequences differ.

Retain a concise resolution record containing input, normalized value, scheme, candidate subject, source, lookup date, validity interval if known, match rationale, status, and remaining uncertainty. For bulk refreshes, retain removed and changed mappings rather than replacing the full history without explanation.

## Check use rights

Separate the standard, the identifier value, reference metadata, and a vendor's assembled dataset. Access to a public lookup page does not automatically authorize bulk extraction or redistribution of all linked data. GLEIF's CC0 publication is explicit; evaluate other authorities' and providers' terms independently. Explain any data unavailable under the user's current access without inventing substitute records.
