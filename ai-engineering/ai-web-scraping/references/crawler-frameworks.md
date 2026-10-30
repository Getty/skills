# Parsers and maintained crawler frameworks

Select the installed language and release explicitly. Framework defaults never replace the task's scope, load, or data-quality requirements.

## Compose the stages

Separate discovery, scheduling, fetching, rendering, parsing, normalization, semantic extraction, and acceptance, each with a small input/output contract. Persist enough intermediate evidence to reproduce a parser bug without contacting the site again.

Extract stable structure deterministically. Let an LLM propose parsers, classify templates, or work a bounded exception queue, and mark those uses so a maintainer can see which records depend on model inference.

## Use parsing libraries deliberately

**Beautiful Soup:** choose the parser explicitly and keep it identical across environments; malformed HTML yields different trees with different parsers. Scope queries to each entity container; never collect independent global lists and zip them. [Parser guidance](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

**selectolax:** current docs center `selectolax.lexbor.LexborHTMLParser`; check old examples that use other imports. Benchmark the whole extraction job, not tree construction, and keep fixtures for malformed markup. [selectolax](https://selectolax.readthedocs.io/en/latest/)

**Trafilatura:** main-text extraction after acquisition. Configure comments, tables, metadata, links, and output format for the task. `favor_precision` and `favor_recall` trade cleaning differently; `fast` skips fallback work. `extract` can return `None`; handle it. A [CLI](https://trafilatura.readthedocs.io/en/stable/usage-cli.html) exists for process-based integration. [API](https://trafilatura.readthedocs.io/en/latest/corefunctions.html)

Run a content extractor on a corpus sample before applying it everywhere: an article heuristic can discard a short reference or product table that matters. Compare required content against the input before enabling deduplication or aggressive pruning.

None of these parsers runs JavaScript. Feed them rendered HTML or an authorized data response when the initial document lacks the fields.

## Build recurring jobs with Scrapy

Use Scrapy for maintained spider rules, middleware, item pipelines, and job control. Keep selectors, normalization, and acceptance rules separate; give each item a stable entity key, its source URL, and the retrieval timestamp.

Set behavior explicitly instead of relying on scaffold defaults. A low-load starting configuration:

```python
ROBOTSTXT_OBEY = True
AUTOTHROTTLE_ENABLED = True
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 1.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
```

These are starting assumptions, not a site's permission or an optimum; tune them to the budget and observed responses. AutoThrottle adjusts slot delays from latency within the concurrency/delay settings and is disabled by default; a target concurrency is not a hard cap. [AutoThrottle](https://docs.scrapy.org/en/latest/topics/autothrottle.html)

Set `ROBOTSTXT_OBEY` deliberately: library defaults and generated-project settings differ. If behavior deviates from the configured policy, inspect custom middleware and request overrides. [Settings](https://docs.scrapy.org/en/latest/topics/settings.html), [RobotsTxtMiddleware](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html)

For resume, give each job a unique `JOBDIR` and resume with the same Scrapy version from a cleanly stopped state. Never share it between workers or accept one from an untrusted writer; persisted request state is not inert data. Expired cookies can invalidate otherwise usable queue state. [Jobs](https://docs.scrapy.org/en/latest/topics/jobs.html)

Resumed acquisition is not exactly-once output: make storage idempotent and reconcile item keys after restart ([operations](operations-and-costs.md)). For browser-required pages, render through a release-compatible adapter with separately bounded browser concurrency.

## Choose Crawlee's execution mode

Crawlee has HTTP and browser crawler families; the Python quick start documents `BeautifulSoupCrawler`, `ParselCrawler`, and `PlaywrightCrawler`. Use HTTP where the evidence is in the response and rendering only where needed. Keep handlers small so switching acquisition mode leaves the output contract intact. [Python quick start](https://crawlee.dev/python/docs/quick-start)

JavaScript and Python Crawlee differ in class names, constructor arguments, and features, and docs under `/next/` may describe another release. Verify experimental or adaptive crawlers against the installed release before depending on them.

Set concurrency and throughput limits deliberately. JavaScript Crawlee caps work with `maxConcurrency` and `maxRequestsPerMinute` and autoscales within them on local resources; local capacity says nothing about what the target accepts. Coordinate per origin when several workers share a target. [Scaling crawlers](https://crawlee.dev/js/docs/guides/scaling-crawlers)

Persist queues and datasets per the storage backend and test restart with a small interrupted job. Count retries, browser subrequests, and model calls separately from pages; a page limit caps neither total work nor provider charges.

## Validate Scrapling's adaptive matches

Scrapling bundles acquisition, parsing, and spiders; pick HTTP or browser fetching from observed page behavior. Adaptive parsing is opt-in with its own state; inspect per-request and class-wide settings before sharing a fetcher across jobs. [Fetcher selection](https://scrapling.readthedocs.io/en/latest/fetching/choosing.html)

Adaptive matching stores element properties and searches for similar elements when the original selector fails. It is a non-LLM mechanism, and its docs discuss wrong matches. Before accepting a recovered node, validate entity identifiers, labels, nearby qualifiers, and value types. Record each recovery as an event, keep before/after fixtures, and version the approved selector change. A similarity score must never swap a recommended item's price in for the requested item's price; model-generated repairs get the same checks. [Adaptive parsing](https://scrapling.readthedocs.io/en/latest/parsing/adaptive.html)

## Connect AI without blocking acquisition

Put model work behind a bounded queue with its own concurrency and cost limits, and store the evidence identifier before enqueueing. When inference slows or a provider fails, apply backpressure or hold pending work; never buffer without bound or refetch pages. Key fetch and extraction caches separately, as in [operations](operations-and-costs.md).

## Keep a maintainable result contract

Return acquisition, extraction, and validation status separately, distinguishing absent fields from failed parsing and from forbidden or unavailable pages. Keep failed records in a review queue with short diagnostics and evidence links. Monitor required-field presence, duplicate keys, page-family drift, and unsupported values. Test the parser against frozen HTML before spending another live crawl on the same problem.
