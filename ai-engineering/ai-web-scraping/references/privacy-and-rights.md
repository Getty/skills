# Privacy, source rights and reuse

Read when a collection touches personal data, restricted material, a reusable or published dataset, or training material. This file holds the engineering checkpoints. For the legal assessment load `eu-platform-privacy` (GDPR, BDSG) and `eu-ai-data-ip` (copyright, TDM exception, database rights, scraping for AI). Reuse an established project policy instead of restarting approval for every ordinary page.

## Name the processing

State what is collected, why, for whom, for how long, and whether the output is private analysis, a published dataset, a search index or training material; the same URLs can feed materially different uses.

Technical access is not reuse permission: a successful request, an open page, an API endpoint or permissive robots rules settle no privacy, copyright, contract or database-right question. Record source terms and licences with their retrieval time when reuse depends on them. An authenticated session covers its authorized purpose, not an export of everything visible; prefer an approved export or licensed dataset.

## Build privacy into the pipeline

Public visibility does not remove GDPR questions; tie personal-data collection to its approved purpose and legal basis.

| Pipeline area | Engineering decision |
|---|---|
| Discovery | Exclude irrelevant sources and categories before fetching. |
| Extraction | Collect only needed fields; no identity enrichment without a defined purpose. |
| Model processing | Use approved providers, regions, retention settings and processor arrangements. |
| Evidence | Restrict access to raw snapshots, traces, screenshots and diagnostics. |
| Storage | Apply retention to raw, normalized, indexed, cached and backup copies. |
| Correction or deletion | Keep lineage so affected derived records can be found. |
| Publication | Review which fields and passages may be redistributed. |

Keep incidental personal data out of prompts and logs. Use synthetic records for public examples and fixtures, never a real person's details. For sensitive categories, systematic profiling, large-scale personal data or unclear reuse, name the open issue and route it to the project's privacy review; similar datasets existing elsewhere is no legal conclusion.

## Handle rights signals

Splitting a collection into small requests does not answer the database-right question. Store needed facts, short evidentiary fragments and source references rather than republishing whole pages; keep complete snapshots for reproducibility under separate access and retention rules.

Record terms, licence statements, access restrictions and machine-readable reservations together with what each restricts (crawling, training, redistribution, account access) instead of one unexplained `allowed` flag.

If a material condition is unresolved, state the concrete uncertainty and continue preparatory work on synthetic or approved data. Skip speculative warnings for unrelated tasks. Apply an established policy consistently and record changes that need a new assessment.

## Keep a decision record

Record purpose, approved source scope, collection date range, policies, recipients, retention and unresolved exclusions, linked to snapshots and derived artifacts so corrections stay feasible. Keep no personal data merely to prove a check happened. Report excluded sources and omitted fields so downstream users know the dataset's limits.
