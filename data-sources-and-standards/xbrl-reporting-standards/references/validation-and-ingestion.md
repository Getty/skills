# Validation and ingestion workflow

## Validate in layers

1. Inspect the file set and package metadata. Detect missing components, unsafe paths, and accidental mixtures of reporting periods or taxonomy versions.
2. Parse the relevant syntax. Resolve references through a controlled package or cache and retain retrieval evidence.
3. Perform XBRL structural and semantic validation with the declared taxonomy set.
4. Validate dimensional combinations, datatypes, period types, and units.
5. Run supported calculation, formula, and filing-profile checks.
6. Compare reported facts with the visible report and the underlying business records available for review.
7. Record findings with rule identifier, severity, affected fact, source location, and correction rationale.

Do not label a generic XML-schema pass as full XBRL validation. Do not describe checks as executed when only inspection or reasoning was performed. Distinguish a missing dependency, an unsupported validation feature, a technical error, and a business concern.

## Handle duplicate facts semantically

Repeated facts are common in Inline XBRL, where the same information appears in several report locations. Compare fact aspects rather than document-local `contextRef` strings. Use the relevant specification's equality and duplicate definitions. The [XBRL duplicate-facts guidance](https://www.xbrl.org/WGN/xbrl-duplicates/WGN-2025-01-14/xbrl-duplicates-2025-01-14.html) distinguishes complete duplicates, numerically consistent duplicates, inconsistent duplicates, and multilingual alternatives.

For numeric duplicates, differing reported values may be consistent at different stated accuracies. Use the prescribed accuracy intervals and edge rules, not approximate floating-point equality. Do not sum duplicate occurrences. Preserve their locations even when an analytical view selects a representative value. Reject or flag conflicts according to the filing profile rather than silently selecting the largest, latest-in-file, or most precise value.

A storage design should retain an occurrence identity and report provenance in addition to semantic aspects. Otherwise, inconsistent duplicates can overwrite each other before anyone sees the conflict. A canonical analytical fact and its original occurrences are related records with different purposes.

## Interpret calculation results

Calculation relationships test particular numerical relationships; they are not a complete accounting audit. A missing calculation network does not prove a report balances, and a pass does not prove that every fact was classified correctly. Presentation order alone never establishes summation.

Check whether the processor and profile use legacy calculation behavior or [Calculations 1.1](https://specifications.xbrl.org/spec-group-index-calculations-2.html). Duplicate and rounding behavior can differ. If formula rules or other validation assertions are provided, record their version and execution status. Do not equate a processor's default options with the recipient's required rules.

## Preserve a reliable ingestion record

Retain the original package, report identifier, submission or publication time, entity identifier scheme, taxonomy entry points, resolved dependencies, processor version, validation results, and source locations. Preserve extension concepts and their definitions even when building a normalized analytical model.

Keep restatements and amended filings distinct from prior reports. A newly filed comparative fact for an old period does not automatically replace the originally reported fact for every analytical purpose. Define whether a query asks for originally reported, latest restated, or currently accepted values.

## Compare concepts with context

A matching label is a search aid, not proof of semantic equivalence. Check accounting framework, reporting scope, taxonomy version, extension definition, dimensions, units, and period. For example, total revenue and revenue for one discontinued operation can share a familiar word but answer different questions.

When mapping an extension to a common analytical metric, record the mapping rationale and whether it is exact, broader, narrower, or conditional. Preserve the original concept. Avoid creating a false sense of comparability by flattening every monetary fact into a label-value pair.

## Use targeted counterexamples

Check zero versus nil, quarter versus year-to-date, a date-only instant, a typed dimension, a default member, two context IDs with the same meaning, duplicate facts with conflicting values, scale expressed in thousands, a negative transformed number, and a restated prior period. These cases directly test common failure modes.

Finish with a concise evidence report: what was validated, which versions were used, material errors, unresolved limitations, and the effect of any corrections. A clean technical report should still state the scope of its checks rather than imply factual or regulatory assurance beyond the work performed.
