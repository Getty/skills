# Evaluate extraction quality and completeness

Read this when comparing methods, accepting a scraper, diagnosing silent data loss, or changing a model, prompt, selector, or cleaning step.

## Establish an independent target

Define entity identity, required fields, permitted normalization, acceptable uncertainty, and intended use. Build a small gold set from saved snapshots, labeled by a reviewer who has not seen candidate output; keep disagreements instead of forcing one answer.

Hold out a set covering the deployment's templates, domains, locales, page lengths, and collection times; a random split of near-identical pages hides layout dependence. Version labeled snapshots.

Record the expected page or entity inventory where known, otherwise the observed boundary: seeds, discovered URLs, filters, depth, stop conditions. Exhausting a self-built queue proves nothing about site coverage.

## Measure the stages separately

| Measure | Definition and limitation |
|---|---|
| Discovery recall | Expected in-scope URLs discovered / known expected inventory. Unknown without an inventory. |
| Retrieval yield | Usable snapshots / attempted in-scope URLs. Report denied, failed, empty, and challenge responses separately. |
| Entity precision | Correctly matched unique predicted entities / all unique predicted entities. |
| Entity recall | Correctly matched gold entities / all gold entities. |
| Field precision | Correct supplied field values / supplied field values. Values on wrong entities count as errors. |
| Field recall | Correct recovered required gold values / required gold values. Missing entities contribute missed fields. |
| State accuracy | Correct classification of `observed`, `absent`, `explicit_null`, `unparseable`, `conflict`. |
| Evidence integrity | Claims with valid snapshot references and matching record-local spans / claims requiring evidence. |
| Semantic support | Claims whose evidence supports their meaning and entity association. Needs independent assessment. |
| Cost per accepted record | Total collection, model, retry, validation, and review cost / accepted records. |

A zero denominator is undefined, never perfect. Report counts beside percentages, broken down per field and per template so easy cases cannot hide a critical failure.

Fix entity matching rules before scoring, preferring stable source IDs; document fuzzy thresholds and review ambiguous matches. A candidate never picks its matching rules after seeing the labels.

## Evaluate interpretation, not just output shape

Normalize predictions and gold identically, deciding in advance which punctuation, whitespace, unit, or date-form differences count as equal. Never normalize away tax inclusion, time zone, currency, or old versus current price.

Schema validity constrains syntax, not interpretation. Check provider completion signals: Claude, for example, documents refusal and output-limit cases that return output outside the schema. [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

Use model self-reported confidence as a threshold only after calibration against labels. Test an LLM judge against human labels; a judge sharing the extractor's assumptions repeats its errors.

## Include failure-oriented fixtures

- Adjacent records with different prices; evidence from the wrong record must fail association.
- Real zero and false values next to absent and explicit-null fields.
- A price range, a crossed-out amount, a variant price, an ambiguous currency symbol.
- Contradictions that stay `conflict` until a documented rule resolves them.
- Duplicates across pagination, repeated next-page tokens, an unfinished inventory.
- A layout change with unchanged facts.
- Instructions embedded in content, metadata, or an image; assert at the application boundary that they change neither extraction nor tool actions ([security and access](security-and-access.md)).
- Output mutations: wrong hashes, quotes, or spans; unexpected properties; duplicate keys; nonfinite numbers; wrong types.

The bundled offline fixtures prove deterministic contract behavior only, not model accuracy, browser reliability, or live-site access.

## Compare methods fairly

Run selectors, structured-source extraction, LLM extraction, and hybrids on the same snapshots and labels, cleaning and chunking included. Count failed attempts, repairs, retries, and rejected records in cost and latency. Report wall time, tokens, browser time, requests, peak resources, and review effort at equal concurrency, and decide on cost per accepted record plus error categories.

## Set release and monitoring gates

Derive thresholds from the intended use; a research inventory tolerates more unresolved optional fields than a billing import. State which failures reject a record, quarantine a page, pause a domain, or stop the run.

On an update, rerun relevant held-out cases and inspect changed outputs. In production, monitor entity counts, unresolved-state rates, schema failures, extraction-method changes, and request error classes, and sample across templates and unresolved cases. A sudden jump in success rate or completeness is a drift signal too.
