---
name: xbrl-reporting-standards
description: "Use when reading, producing, converting or validating XBRL reports and taxonomies — XBRL 2.1, Dimensions, Inline XBRL, OIM, xBRL-JSON, xBRL-CSV, facts, contexts, units, DTS, SEC and ESEF filings."
---

# XBRL Reporting Standards

## Establish the reporting model

Treat XBRL as a family of standards for structured business reporting. A taxonomy defines reportable concepts and relationships; a report supplies facts with the context necessary to interpret them. XBRL is not confined to financial statements, and a tagged value is not meaningful without its concept, reporting entity, period, dimensions, and applicable unit or language. Use the [XBRL International specifications index](https://specifications.xbrl.org/specifications.html) to identify authoritative documents and their status.

Separate three questions: whether a document follows an XBRL specification, whether it follows a filing program's profile, and whether its reported business information is correct. Success at one level does not establish the others. Keep the skill independent of any regulator, accounting framework, implementation language, or data platform.

## Navigate the references

- Read [facts and contexts](references/facts-and-contexts.md) for concept identity, periods, units, accuracy, signs, nil values, and semantic comparison.
- Read [taxonomies and dimensions](references/taxonomies-and-dimensions.md) for DTS discovery, linkbases, explicit and typed dimensions, defaults, and extension decisions.
- Read [Inline XBRL and OIM](references/inline-and-oim.md) for syntax selection, extraction, transformations, JSON and CSV representations, and conversion limits.
- Read [validation and ingestion](references/validation-and-ingestion.md) for layered validation, duplicate handling, provenance, numerical checks, and a repeatable processing workflow.
- Read [filing profiles](references/filing-profiles.md) for SEC and ESEF boundaries, current-rule lookup, package selection, and version manifests.
- Read [primary sources](references/sources.md) for direct specification links, observed versions, and freshness checks.

## Follow the working sequence

1. **Identify the artifact and objective.** Establish whether the input is an XML instance, Inline XBRL document set, taxonomy, xBRL-JSON report, xBRL-CSV report, or package. Identify the reporting period and intended recipient when they matter. Decide whether the task is explanation, extraction, authoring, validation, conversion, or comparison.
2. **Resolve the reporting environment.** Select the taxonomy entry point, exact version, required extensions, specification versions, and filing profile. Distinguish a Recommendation from a working draft or candidate document. Keep a reproducible record of package remappings and retrieved dependencies.
3. **Load the complete model.** Resolve the discoverable taxonomy set, namespaces, concepts, contexts, units, relationships, and dimensions using an XBRL-aware processor. A generic XML parser or spreadsheet import can assist inspection but does not establish conformance.
4. **Interpret facts before flattening.** Preserve concept expanded names, entity scheme and identifier, exact periods, dimension values, unit, language where applicable, accuracy, nil state, and source location. Keep every source occurrence until duplicate analysis is complete.
5. **Apply the correct validation layers.** Check document syntax, XBRL rules, dimensions, applicable calculation and formula rules, and filing-program requirements. Inspect visible Inline XBRL presentation and extracted facts together. Distinguish an unsupported check from a passed check.
6. **Transform or analyze deliberately.** Define compatibility and loss criteria before moving between formats or combining reports. Retain extensions and provenance. Do not sum repeated fact occurrences or merge facts merely because their labels and values look alike.
7. **Deliver the result with its limits.** Provide the relevant facts or corrected artifact, selected versions, findings by rule and severity, and any unresolved taxonomy or interpretation issues. State whether validation was executed or the result was a conceptual review.

## Apply interpretation rules

Use namespace URI plus local name for concept identity; a prefix is only an abbreviation. Treat context and unit IDs as document-local references. Read default dimensional members through the taxonomy instead of treating an omitted XML dimension as an unknown value automatically.

Keep displayed scale separate from numeric accuracy. Treat nil, zero, an empty string, and a missing fact separately. Apply period conventions carefully when converting date-only XML contexts into OIM timestamps. Preserve consistent and inconsistent duplicates as distinct categories until the required policy determines their treatment.

For a live filing, verify the recipient's current accepted taxonomies, technical guide, rules, and effective dates. Do not infer universal legal obligations from XBRL itself, or assume the newest international specification is already accepted by every filing system.
