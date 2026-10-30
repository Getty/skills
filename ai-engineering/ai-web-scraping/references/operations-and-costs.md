# Operations and costs

## Bound each stage

Give discovery, HTTP, rendering, model extraction, validation and storage separate queues when their resource profiles differ; small jobs keep the boundaries logical in one process. Limit per-origin rate, global requests, browser slots, tokens, bytes, retries, time and cost independently; a page cap bounds nothing else.

Apply backpressure when downstream stages cannot drain. When a budget expires, keep the frontier and label the run partial. Never raise concurrency to offset rising block rates. Keep browser and model concurrency and identities apart, close resources reliably and watch browser memory. Framework throttles need project upper bounds: [crawler frameworks](crawler-frameworks.md).

## Persist and resume

Track `discovered`, `admitted`, `fetched`, `extracted`, `accepted`, `rejected`, `retry_due` and `terminal_failure` with stage-local reasons and attempts. Retry only the failed stage while its inputs remain usable.

Build idempotency keys from source identity, snapshot or version, extraction-contract version and relevant view dimensions. Store stable entities apart from observations; never merge variants only because they share a canonical URL. Move output and checkpoint atomically where possible, use uniqueness constraints for at-least-once execution, and keep rejected output separate.

After a provider timeout, keep the job ID and check its completion before creating another paid job; client timeout, server failure and unknown completion are different states.

## Cache and refresh

| Cache | Key dimensions | Invalidate on |
| --- | --- | --- |
| Acquisition | URL, relevant headers, identity, locale/view | Freshness and HTTP validators |
| Prepared view | Snapshot hash, transform version and options | Transform change |
| Extraction | View hash, schema, plan, prompt, model, normalizer | Contract or extractor change |

Never share an entry across identities, tenants or materially different locale and currency contexts; the same URL or byte hash does not imply the same business meaning. A cache hit can be too old for a current-price request, so keep source-fetch time and observation time apart. Validators and 304: [HTTP and crawl policy](http-and-crawl-policy.md).

Prioritize refresh by sitemaps, feeds and measured change rates, then verify the content; a sitemap index's `lastmod` describes the listed sitemap, not its pages. [Sitemap protocol](https://www.sitemaps.org/protocol.html) Distinguish confirmed removal, changed access, timeout and absence from a listing. Define how many observations confirm a deletion before tombstoning, then propagate it under policy.

## Measure cost and quality together

`total cost = requests + browser time + model input/output + retries + storage + review`

`cost per accepted unique record = total cost / accepted unique records`

Report cost per record as undefined when nothing passes. Include failures, retries, provider minimums, credits and retained sessions; separate setup from recurring marginal cost. Look up current pricing instead of embedding a price table.

In a cheap-first cascade (embedded JSON, known-template selectors, then model interpretation of prose), measure routing recall and inspect rejected samples; cheap processing that silently loses data is no improvement. Optimize tokens only after correctness: keep complete record regions, drop duplication, cache unchanged views. Test smaller or local models on the actual contract before switching; self-hosting or model size alone proves no performance, privacy or saving.

Track quotas, latency percentiles, queue age and spend; set a hard budget and deadline before scaling. Never turn a one-off job into recurring paid monitoring unasked.

## Deploy and upgrade

Local services: specify resources, browser installation, egress, credentials, retention, recovery and cancellation. Hosted services: verify capabilities, processing location, retention, quotas and API generation. List model hosting and browser hosting separately in the data-flow inventory.

Pin application, parser, browser and adapter versions after a smoke test; keep canaries per template, locale and major failure class. Replay snapshots after extractor changes and run bounded live canaries after acquisition changes. Compare counts, missingness, evidence errors, latency and cost before rollout; keep a known-good version for rollback. Contract changes need an explicit migration.

Emit structured stage/reason metrics; redact credentials, signed URLs and unneeded personal data, and keep raw evidence in controlled artifacts, not logs. Alert on empty pages, repeated cursors, missing fields, unknown templates, truncation and rising cost per accepted record. A green health endpoint proves no useful data.
