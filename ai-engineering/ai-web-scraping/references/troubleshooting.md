# Troubleshooting

Diagnose the earliest stage that diverges from the expected evidence. Reproduce on a retained snapshot and change one factor at a time. Never drop rejected pages or fields to improve success statistics.

| Symptom | Inspect | Next action |
| --- | --- | --- |
| HTTP 200 but empty dataset | Body, title, content type, selected region | Tell shell, consent/login page, error document and real empty result apart |
| Data visible in browser but absent from HTML | Relevant responses and rendered DOM | Use the authorized data response or an explicit render/readiness step |
| Browser click succeeds but data is old | Response timing, selected filter, stable IDs | Wait for a concrete new-state predicate; verify the postcondition |
| Only the first page was collected | Frontier, next cursor, totals, stop reason | Add bounded pagination and repeat-state detection |
| Row count changes while scrolling | IDs captured over time, DOM recycling | Collect incrementally or use authorized response records |
| Markdown loses prices or footnotes | Raw/DOM versus transformed view | Adjust filtering or extract record regions and tables directly |
| Valid JSON contains wrong facts | Snapshot, field evidence, entity boundary | Separate schema validation from semantic checks; quarantine unsupported data |
| Same quote validates for wrong product | Record region and source identity | Bind boundaries in trusted code; evaluate entity ownership |
| Missing values become zero or false | Normalizer, defaults, coercion | Keep explicit states and strict types |
| Duplicate or merged variants | Identity rules, URL parameters, locale/view | Keep source variants separate; revise entity keys |
| Costs climb unexpectedly | Attempts, model tokens, browser lifetime | Bound retries; look for duplicate jobs and missing cache keys |
| Old results despite successful calls | Source timestamp, cache key, freshness option | Fetch under the right freshness policy; keep snapshot identity |
| Selector repair returns plausible wrong data | Before/after plan, held-out fixtures | Reject the repair until field and entity checks pass |
| New SDK rejects copied example | Installed version, SDK/REST/MCP contract | Use matching docs and a minimal adapter smoke test |
| Robots or access check is unavailable | Status, retries, cache, redirect policy | Apply the crawl policy; keep an explicit failure state |
| Worker cannot resume safely | Queue state, output/checkpoint transaction | Use idempotent persistence and compatible framework versions |
| Source changed but output did not | Snapshot hash versus extractor version | Check source freshness, prepared-view cache, extraction cache |
| Healthy service produces no useful records | End-to-end canary, rejected output | Check the whole acquisition-to-acceptance path, not liveness |

## Inspection order

1. Job, source URL, locale/session, expected record.
2. The exact snapshot and representation the extractor used.
3. Access/status, content type, size, render completion.
4. Whether required information survived cleanup and chunking.
5. Extraction reproduced with the recorded plan, model, prompt and schema version.
6. Type, normalization, evidence, entity and completeness failures, each separately.
7. Deduplication and storage, only once the record is known correct.

For a model comparison freeze snapshots, schema and budget, and record retries and rejected outputs; changing model and source together makes the result uninterpretable.

## Escalate on evidence

Escalate to browser rendering when content is absent from the fetched representation, to model interpretation when tested parsing rules cannot carry the semantics, and to vision when the information exists only visually. Keep the original failure artifact at each step. An access challenge is its own outcome: use an authorized API, export or approved user-assisted session, never stealth, identity rotation or a bypass ([security and access](security-and-access.md)).

## Report what remains

Name the unresolved stage, the evidence behind the diagnosis, what was verified and which records are affected. Separate a workaround from a measured fix. Never claim "all pages scraped" when the only evidence is an empty queue.
