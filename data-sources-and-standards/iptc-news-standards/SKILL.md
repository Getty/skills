---
name: iptc-news-standards
description: "Use when creating, converting, ingesting or validating IPTC news data — NewsML-G2, ninjs, NewsCodes, Media Topics, RightsML, item revisions, corrections, cancellation, embargo, taxonomy mapping, claim extraction."
---

# IPTC News Standards and Data

## Explain the standards by their jobs

Use NewsML-G2 for structured XML news exchange, including management metadata, content, packages, concepts, and editorial planning. Use ninjs for versioned JSON news objects. Use NewsCodes for controlled values and Media Topics for subject classification. Use RightsML when a machine-readable rights-expression contract is needed. Keep the content's subject matter and any extracted world claims distinct from the metadata describing its publication.

Start with the actual feed, sample item, or target interoperability contract. Identify format, standard version, conformance/profile, provider, item identity, item revision, content representations, and lifecycle expectations. Do not assume every publisher uses the newest approved standard or that all IPTC formats share field names.

Use this skill independently. Select storage, processing tools, and domain mappings to fit the requested application after defining the format contract.

## Navigate by question

| Need | Read |
| --- | --- |
| Choose a standard, version, or conversion strategy | [Standards and version selection](references/standards-and-version-selection.md) |
| Parse or author NewsML-G2 XML | [NewsML-G2](references/newsml-g2.md) |
| Parse or author ninjs JSON | [ninjs](references/ninjs.md) |
| Resolve codes, classify subjects, or retain rights metadata | [Vocabularies and rights](references/vocabularies-and-rights.md) |
| Handle revisions, corrections, cancellation, or extracted claims | [Lifecycle and claims](references/lifecycle-and-claims.md) |
| Verify exact specifications and current publication status | [Sources and limits](references/sources.md) |

## Follow the workflow

1. **Establish the source contract.** Retain original XML/JSON and relevant payloads or durable references. Record receipt time, source URL, checksum, provider identity, format version, schema checksum, and profile. Distinguish the schema version from the publisher's item revision.
2. **Validate structure safely.** Use the matching official XSD or JSON Schema dialect and local pinned dependencies. Parse XML without uncontrolled external-entity resolution. Decide explicitly how supported extensions and unsupported versions are handled. A successful parse is not full standards conformance.
3. **Preserve item identity and structure.** Keep managed item identity separate from transport-message identity, content URL, package membership, rendition identity, and extracted event identity. Preserve alternative representations and their relationships instead of concatenating everything into one text field.
4. **Interpret management metadata.** Process item versions, publication status, corrections, updates, and embargoes before exposing content. Handle out-of-order delivery and retransmission using the provider's documented version contract. Retain source, creator, provider, credit, and rights roles separately.
5. **Resolve controlled values.** Resolve NewsML-G2 QCodes through the applicable catalog and retain the original code, resolved concept URI, catalog identity, and vocabulary release. Keep unresolved values visible; do not infer a concept URI from an English label.
6. **Convert or enrich explicitly.** Map each field's meaning, multiplicity, language, scope, and lifecycle behavior. Preserve extensions where permitted and report losses. Keep publisher classifications separate from machine-generated assignments and extraction results.
7. **Verify important cases.** Exercise a normal item, correction, withheld/canceled item, embargo, out-of-order revision, package or association, multilingual text, unresolved code, and provider extension. For extraction, include negation, attributed claims, and planned versus completed events.

## Keep lifecycle and rights semantics clear

NewsML-G2's `usable`, `withheld`, and `canceled` states have defined recipient behavior; canceled is a terminal item state in its processing model. An embargo adds another publication condition, and an empty embargo element is not the same as no embargo. Follow the exact source version rather than flattening these states into a generic boolean.

Publication status does not independently grant copyright or usage permission. Preserve rights holders, notices, usage terms, applicable rights expressions, their targets, and any rendition-specific restrictions. The license of an IPTC schema or taxonomy does not license the news content exchanged with it.

A correction signal indicates a correction but does not by itself identify every earlier version affected. A canceled item must be handled according to its publication contract, while analysis of the underlying world claims requires separate evidence. Do not continue displaying superseded extracted assertions as if their source had remained unchanged.

## Maintain evidence boundaries

A Media Topics assignment classifies subject matter; it does not assert a formal class membership for every entity mentioned. A provider's organization/person metadata is not proof of a relationship between those participants. Planned coverage, an event's status, a published story, and a reported claim have different identities and timelines.

For each extracted claim retain source item/revision, span or structural locator, extraction method/version, participants, attribution, modality, negation, time, and original numeric/unit expressions. Keep source reliability, classification confidence, extraction confidence, and accepted fact status separate.

## Deliver a reviewable result

Provide the schema/version decision, source-to-target mapping, examples, lifecycle rules, retained provenance, and conversion-loss report. State exactly which schemas and samples were validated and which business rules remain provider-specific. Recheck primary sources for newly approved releases; approval announcements and downloadable release packages can be out of sync.
