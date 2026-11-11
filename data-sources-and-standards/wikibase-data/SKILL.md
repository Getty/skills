---
name: wikibase-data
description: "Use when reading, exporting or ingesting Wikidata or Wikibase data — entity JSON, API, dumps, RDF, statements, ranks, snaks, qualifiers, references, truthy triples, redirects, deletions, update streams, reconciliation."
---

# Wikidata and Wikibase Data

## Start from the representation and the question

Explain Wikidata as a knowledge base built on Wikibase's statement model. Distinguish the general Wikibase software and data model from Wikidata's particular repository, property meanings, community conventions, and public services. A property ID in another Wikibase installation does not inherit the meaning of the same ID in Wikidata.

Ask what must be preserved: a few display fields, a reproducible entity snapshot, every statement with context, an RDF projection, or a continuously maintained subset. Identify the exact representation before writing code: API envelope, canonical entity JSON, compressed JSON dump, full RDF, truthy RDF, or change notification. Never call a lossy direct-value export a complete statement import.

Use this skill independently of database or graph products. Choose storage and tooling only after inspecting the user's environment and required semantics.

## Navigate by task

| Need | Read |
| --- | --- |
| Explain entities, terms, statements, ranks, snaks, and ordering | [Data model and JSON](references/data-model-and-json.md) |
| Preserve values or distinguish full RDF and truthy data | [Typed values and RDF](references/typed-values-and-rdf.md) |
| Choose an API, query, linked-data request, or dump | [Acquisition and snapshots](references/acquisition-and-snapshots.md) |
| Maintain a changing corpus, redirects, or deletions | [Updates and reconciliation](references/updates-and-reconciliation.md) |
| Build a subset, map semantics, or verify an importer | [Filtering, mapping, and validation](references/filtering-mapping-and-validation.md) |
| Recheck current contracts, policies, and limitations | [Primary sources](references/sources.md) |

## Work through a faithful pipeline

1. **Record the source contract.** Capture repository, endpoint or dump URL, representation, acquisition time, supplied revision, dump identity, format version, and filtering options. Keep parser and application-mapping versions separate. Preserve original bytes or a durable source object when replay matters.
2. **Acquire proportionately.** Use documented entity access for identified entities, bounded queries for discovery, and dumps for large reproducible corpora. Inspect current endpoint limits, supported parameters, and caching behavior. Use a descriptive User-Agent, bounded retries, and server-directed backoff.
3. **Preserve identity and structure.** Key entities by repository plus full ID. Retain statement IDs as opaque identifiers, all source ranks, qualifier occurrences, reference groups, explicit order arrays, multilingual terms, and supported entity-type structures. Do not replace missing source identifiers with fabricated upstream metadata.
4. **Interpret values without loss.** Keep concrete value, unknown value, and explicit no value distinct. Preserve exact quantity decimals, bounds, units, calendar, time precision, coordinate globe and precision, language tags, and full entity IDs. Retain raw unsupported structures for future interpretation when the source envelope is otherwise valid.
5. **Build declared projections.** Separate source statements from accepted application facts. Name rank-selection, property filtering, identity matching, and ontology mappings as versioned policies. Preserve a route from every simplified value back to its source statement and snapshot.
6. **Maintain and reconcile.** Choose metadata-triggered entity refresh or a verified RDF update stream. Establish a baseline and overlap strategy that fits the available retention window. Apply updates idempotently, preserve lifecycle changes, and reconcile after gaps, export-version changes, or uncertain outcomes.
7. **Verify representative cases.** Exercise all ranks and snak types, repeated qualifiers, separate reference groups, large decimals, imprecise dates, unknown types, redirects, deletion, replay, and out-of-order updates. Report the actual scope of verification.

## Preserve the important distinctions

Treat rank as source curation metadata. Best-rank selection is per entity/property: preferred statements when present, otherwise normal statements; deprecated statements are excluded from the truthy convenience view. Multiple best-ranked values can remain. “Truthy” is an export term, not a guarantee of verified truth or timeless applicability.

Keep source references as grouped statements about evidence. A cited URL is not proof that it supports the claim, and several reference groups are not one synthetic source. Qualifiers can carry essential scope, including time, method, or quantity; removing them changes how a statement can be interpreted.

Treat P31 and P279 according to their actual source semantics. Do not mechanically turn the entire repository into a consistent OWL ontology. Names, aliases, website URLs, and external identifiers are evidence for identity assessment; they do not independently warrant `owl:sameAs`.

Keep finite retention visible in update plans. A recent-change notification usually identifies a change and its metadata; it is not the entity's complete new content or a ready-to-apply RDF patch. A dedicated RDF update stream has a different schema and lifecycle semantics, including shared data and reconciliation operations.

## Deliver an inspectable result

Provide the acquisition contract, preserved structures, deliberate losses, mapping rules, and recovery procedure. For code, include meaningful sample inputs and observed results, not assumptions about hardware or unrun full-dump performance. For explanations, use small synthetic examples and clearly identify live source claims. State whether validation covered parsing, semantics, replay, endpoint behavior, and production-scale operation.
