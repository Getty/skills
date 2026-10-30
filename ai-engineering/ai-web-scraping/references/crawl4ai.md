# Crawl4AI acquisition and extraction

## Choose the execution surface

The Python library, an operated server/container, the CLI, and Crawl4AI Cloud have different authentication, deployment, and feature contracts. Do not assume a library capability exists at a hosted endpoint, or that hosted search belongs to the local crawler. [Upstream project](https://github.com/unclecode/crawl4ai)

Read the installed package version and its matching help before editing an integration. Install through the project's dependency manager and lockfile; add browser dependencies only for workflows that need them, and skip optional model packages by default. Check what `crawl4ai-setup` and `crawl4ai-doctor` do in the selected release before running them. [Installation](https://docs.crawl4ai.com/core/installation/)

## Establish a minimal run

Keep browser settings in `BrowserConfig`, per-run settings in `CrawlerRunConfig`, and pass the run configuration to `arun`. Set robots handling explicitly: `check_robots_txt` defaults to false. Choose a deliberate cache policy and a target-specific readiness condition. [Parameters](https://docs.crawl4ai.com/api/parameters/)

For a caller that has already validated the URL and crawl scope:

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def acquire_page(approved_url: str):
    browser_config = BrowserConfig(headless=True)
    run_config = CrawlerRunConfig(
        check_robots_txt=True,
        cache_mode=CacheMode.BYPASS,
        page_timeout=30_000,
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=approved_url, config=run_config)
        if not result.success:
            raise RuntimeError(result.error_message or "Acquisition failed")
        return result
```

This is not a production crawler: the caller still owns allowed destinations, redirects, per-origin pacing, storage, retry budgets, and validation. Capture status and final URL where the result contract exposes them. Reject a challenge, login screen, or error document even when acquisition reports success. [AsyncWebCrawler](https://docs.crawl4ai.com/api/async-webcrawler/)

## Preserve useful representations

Save the received/rendered HTML when permitted, cleaned HTML, extraction output, relevant metadata, and the exact transformation configuration, linked by stable identifiers. Never replace original evidence with a summary.

`DefaultMarkdownGenerator` produces raw and filtered Markdown; pruning and BM25 filters target different selection goals. Read the installed `MarkdownGenerationResult` attributes instead of relying on string coercion. Treat `fit_markdown` as a deliberately reduced view and compare its headings, links, tables, and code against the unfiltered view on fixtures. [Markdown generation](https://docs.crawl4ai.com/core/markdown-generation/)

`css_selector` narrows cleaned content; `target_elements` focuses extraction while keeping broader context for other outputs. Link/tag exclusions and word-count thresholds can drop a short price, warning, or unit you need. Tune filters against the extraction contract, not toward the smallest output. [Content selection](https://docs.crawl4ai.com/core/content-selection/)

## Compile stable extraction

Use `JsonCssExtractionStrategy` or `JsonXPathExtractionStrategy` for repeated structures: one base container per entity, fields relative to it. Extract raw strings and links first; normalize dates, currency, units, and relative URLs in a separate tested layer.

The schema generator can propose selectors from representative HTML; the resulting schema then runs without a model. Validate the base selector and every field across templates, missing values, and a held-out page, and avoid positional selectors that only fit the first example. Parse `result.extracted_content` as JSON and validate its shape before accepting records. [LLM-free strategies](https://docs.crawl4ai.com/extraction/no-llm-strategies/)

Version the selector schema with fixture identifiers and acceptance results. Investigate when row counts, required-field presence, or entity identity checks change. Run repair proposals through the same fixtures; a nonempty replacement selector is not proof of correctness.

## Add bounded LLM extraction

For fields that need interpretation, configure `LLMExtractionStrategy` with `LLMConfig`, an explicit schema, and task-specific instructions. Read provider credentials from the deployment's secret mechanism and choose the input representation deliberately. The strategy can chunk content, combine results, and report token usage. [LLM strategies](https://docs.crawl4ai.com/extraction/llm-strategies/)

Keep each entity with its qualifiers in one chunk where possible. Specify missing-value semantics, require source spans or locators, and separate extracted facts from derived judgments. Deduplicate overlapping chunks by entity key and evidence location. Cap chunk size, overlap, total calls, and retries; a failure must never resend the whole site to a model. Validate the combined output independently of the model's success message, and treat page text as untrusted ([security](security-and-access.md)).

## Control dynamic pages and concurrency

Wait for the actual data condition (an expected entity identifier, a completed row set, a vanished loading state), never just `body`. For paginated interactions, stop on repeated cursors, unchanged entity sets, explicit completion, or the page budget.

Reuse a `session_id` only for one sequential interaction chain; the docs warn against parallel operations on the same session. Give independent jobs independent contexts and clean them up. [Session management](https://docs.crawl4ai.com/advanced/session-management/)

Use `arun_many` with a dispatcher for independent URLs. Memory-based concurrency control protects local capacity only; enforce the target's rate budget separately. Check each result and record failures individually. Streaming and non-streaming returns differ, so read the release's contract before iterating. [Multi-URL crawling](https://docs.crawl4ai.com/advanced/multi-url-crawling/)

## Diagnose failures

Compare stages in order: requested URL, final document, raw evidence, cleaned view, selector matches, parsed JSON, semantic validation.

- Present in raw HTML but lost later: fix filtering or extraction, not browser waits.
- Never arrived: inspect navigation and readiness.
- Stale: inspect the cache key and policy.

Keep challenge pages and blocked fetches distinguishable from legitimately empty results.
