# Facts, contexts, units, and accuracy

## Interpret a fact as a contextual statement

An XBRL fact associates a value with a taxonomy concept. In XML, item facts refer to a context and, for numeric items, a unit as applicable; taxonomy declarations identify datatype and period type. The [XBRL 2.1 specification](https://specifications.xbrl.org/work-product-index-group-base-spec-base-spec.html) defines these components.

For an original example, “Revenue is 123,000 EUR” is incomplete until the reporting entity, duration, and relevant segment or consolidation scope are known. The same label can occur for different concepts, and the same concept can have many facts across periods and dimensions. A human table's position is useful evidence, not a substitute for the encoded context.

Use an interpretation record such as:

| Component | Example meaning | Comparison rule |
|---|---|---|
| Concept | A particular revenue concept | Compare expanded name and definition |
| Entity | Identifier under a declared scheme | Compare scheme and value together |
| Period | A year, quarter, or instant | Compare exact boundaries and period kind |
| Dimensions | A specified segment or product | Resolve members and defaults |
| Unit | EUR, shares, or a ratio | Compare semantic measures |
| Value and accuracy | 123000 rounded to thousands | Compare value with declared accuracy |
| Language | English text where applicable | Preserve language when it affects identity |

## Treat dates carefully

An instant concept represents a value at a point in time; a duration concept spans a period. A quarter-to-date and year-to-date amount ending on the same date are different facts. An opening balance and closing balance require the appropriate instant, not a guessed duration.

For date-only XML periods, `startDate` means the start of the day, while `endDate` and `instant` mean the end of the day. Consequently, a duration from `2025-01-01` through `2025-12-31` maps to boundaries `2025-01-01T00:00:00/2026-01-01T00:00:00` in the corresponding OIM representation. Follow the [xBRL-XML mappings](https://www.xbrl.org/Specification/xbrl-xml/REC-2021-10-13+errata-2023-04-19/xbrl-xml-REC-2021-10-13+corrected-errata-2023-04-19.html); do not shift every date indiscriminately.

Preserve explicit times and timezone information. Do not add a timezone merely because the reporting entity has a headquarters address. Document any normalization used for analytics.

## Separate unit, scale, and accuracy

A unit describes the measurement: currency, shares, pure numbers, or a compound expression. A displayed heading such as “EUR millions” does not change the underlying currency measure into a new currency. Inline XBRL scaling determines how the displayed number becomes the actual numeric value.

`decimals` describes reported decimal-place accuracy; negative values represent rounding to powers of ten. `precision` describes significant-digit accuracy under the applicable rules. Neither attribute is a display-format instruction. A numeric value `123000` with `decimals="-3"` communicates accuracy to thousands. Read the [precision, decimals, and units guidance](https://www.xbrl.org/WGN/precision-decimals-units/WGN-2017-01-11/precision-decimals-units-WGN-2017-01-11.html) before implementing numerical comparisons.

Do not convert financial amounts through binary floating point when decimal fidelity is required. Preserve the reported value and accuracy before computing derived values. Any currency conversion is an additional analytical operation requiring a rate, date, and policy; it is not an XBRL normalization.

## Preserve signs and absence

A debit or credit balance attribute describes a concept's normal accounting balance; it is not an instruction to negate every reported fact. Inspect concept meaning and calculation weights. Inline sign and transformation attributes affect extracted values independently of visual typography.

Distinguish zero from nil and both from a missing fact. A nil assertion is explicitly present; an absent assertion might be out of scope, omitted, unavailable, or invalid under a profile. Do not infer zero from a blank table cell or an unreported dimension combination. For text facts, preserve empty values and whitespace according to the datatype and transformation rules instead of treating every empty-looking string alike.
