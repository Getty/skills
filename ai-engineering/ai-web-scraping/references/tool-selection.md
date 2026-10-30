# Select the acquisition and extraction stack

## Separate the decisions

Choose how to obtain evidence independently from how to interpret it: a browser can feed a deterministic parser, a plain HTTP response can feed a model, and a model can author a selector once without running on every page.

Identify the requested output first: source documents, a URL inventory, typed records, historical changes, or answers. Readable Markdown suits a knowledge corpus but does not prove that every variant, table cell, footnote, or pagination branch was captured.

Prefer an authorized first-party API, export, feed, or dataset when it holds the needed fields under a usable contract. Examine representative HTML and embedded structured data before adding rendering. Keep the original evidence even when another representation is easier to process.

Select on measured requirements (cost, field accuracy, coverage, reproducibility, maintenance, data location, operator effort), never on popularity, stars, or "scrapes any site" claims.

## Choose an acquisition layer

| Candidate | Useful starting point | Main implementation responsibility |
|---|---|---|
| HTTP client plus Beautiful Soup/selectolax | Static pages, JSON responses, embedded data | Scheduling, redirects, response limits, retries, provenance |
| Trafilatura after fetching | Article or documentation body extraction | Check that cleaning retains required tables and metadata |
| Scrapy | Large recurring crawls with explicit rules | Spider rules, middleware, entity keys, output validation |
| Crawlee | HTTP and browser crawling in a shared framework | Match language/release APIs; configure queues, limits, sessions |
| Crawl4AI | Browser acquisition, Markdown, selector or LLM extraction | Preserve evidence, define scopes and extraction checks |
| Scrapling | Python acquisition and adaptive element matching | Validate recovered selectors and maintain page fixtures |
| Playwright | Precise interactive acquisition | Readiness, pagination, contexts, resource and action limits |
| Firecrawl | Service/API workflow for scrape, map, crawl and JSON extraction | Verify cloud/self-host capabilities, response accounting and cost |
| Stagehand or browser-use | Exploration or variable navigation needing model judgment | Constrain actions, measure success and convert stable steps to code |
| Apify Actors | An existing task-specific implementation fits the source | Review Actor provenance, schema, version, charges and failures |
| ScrapeGraphAI | Model-driven graph extraction from pages or local documents | Separate local library from managed API, bound model work and validate evidence |
| Jina Reader | Convert URLs or documents into readable content | Check content retention, freshness, data flow and separate structured extraction |
| Zyte API | Managed acquisition and standard/custom structured extraction | Match extraction source, record type, model version and response contract |

These tools occupy different layers; combining them often beats picking one. Details: [Crawl4AI](crawl4ai.md), [Firecrawl](firecrawl.md), [crawler frameworks](crawler-frameworks.md), [browser agents](browser-agents.md), [official skills and MCP](official-skills-and-mcp.md).

## Additional adapters

**ScrapeGraphAI:** the self-operated `scrapegraphai` Python library (`SmartScraperGraph`-style pipelines over web or local documents with your chosen model) is distinct from the managed-service clients `scrapegraph-py` and `scrapegraph-js`, which call a separate service. Check package identity before borrowing examples. Review generated scripts as code with fixture tests; a graph's successful execution is neither verified evidence nor site coverage. Check telemetry and model destinations against project policy. [Library and service comparison](https://github.com/ScrapeGraphAI/Scrapegraph-ai)

**Jina Reader:** use Reader to obtain readable representations of a URL or PDF, then apply the field contract separately. Reader, Search, and embedding/reranking are distinct endpoints. Inspect current authentication, output-format, cache, and target-selection options; a URL prefix is not a crawl configuration. Retain source URLs and times, test table/metadata retention, and send private content only under an established processing arrangement. [API reference](https://docs.jina.ai/), [Reader API](https://r.jina.ai/docs)

**Zyte:** keep HTTP/browser acquisition apart from automatic extraction. Select the record type and an explicit extraction source (extraction from supplied HTML is also documented); defaults and source options vary, so match current API support. Record provider model versions in the observation manifest where exposed, replay fixtures around upgrades, and evaluate semantic quality and provenance as for a local model. [Automatic extraction](https://docs.zyte.com/zyte-api/usage/extract), [API contract](https://docs.zyte.com/zyte-api/usage/reference.html)

## Decide where AI helps

Assign AI the bounded roles in [architecture](architecture-and-planning.md#choose-what-ai-should-do). Do not label a heuristic matcher an LLM: Scrapling's adaptive relocation is non-LLM similarity ([crawler frameworks](crawler-frameworks.md#validate-scraplings-adaptive-matches)).

## Run a representative pilot

Build a small corpus with the failure modes production will meet: different templates, missing fields, multirow tables, locale differences, pagination, unavailable items, an intentionally changed layout, and a page with instruction-like text that must stay data.

Run the same frozen evidence through every candidate extractor. Run any live acquisition comparison separately, and only when live access is authorized; otherwise site changes masquerade as extractor differences. Measure with the stage metrics in [evaluation](evaluation.md), keeping acquisition failures apart from extraction failures and counting failed attempts in cost.

Set explicit acceptance thresholds and compare error types directly: a cheap extractor that merges two products fails a different requirement than an expensive one that misses an optional description. Never compress all behavior into one percentage.

## Select a starting architecture

- **Recurring structured catalog:** explicit frontier, HTTP or browser acquisition as required, selectors, typed validation, a small exception queue; model extraction only for the fields or templates that justify it.
- **Documentation corpus:** scope discovery, content-preserving extraction, URL and content deduplication, revision metadata. Test code blocks, headings, and tables before tuning token-reduction filters.
- **Short interactive task:** the available browser integration with a finite action budget. For a maintained workflow, save the observed path as code and keep an agent fallback bound by the same success criteria.
- **Service-backed:** evaluate one page, a known URL batch, and a partial-failure job before scaling. A successful API request does not prove site coverage; Firecrawl's [Map](https://docs.firecrawl.dev/features/map), for example, is approximate URL mapping, not a recursive crawl.

## Record the decision

Save source families, required schema, acquisition and extraction methods, version constraints, data destinations, throughput budget, evaluation results, unresolved coverage, fallback trigger, and rollback conditions. Justify any browser or model with observed evidence, and label untested suggestions apart from measured results. Keep each rejected alternative to one line: which requirement it failed and what result would reopen it.

Reuse the project's runtime and deployment conventions; add a platform only when the pilot shows a benefit. Local execution, a local model, a self-hosted API, and a remote browser are separate choices; document each boundary.
