# AI engineering skills

Building and running systems on top of models — serving them, feeding them data,
measuring what comes out. A skill belongs here when the model is the subject of the
engineering work. Skills that only use a model elsewhere stay in their own domain:
the agent harnesses in [claude](../claude/README.md), [codex](../codex/README.md) and
[hermes-agent](../hermes-agent/README.md), AI law in
[compliance-and-governance](../compliance-and-governance/README.md), vector storage in
[databases](../databases/README.md), GPU nodes in
[system-and-network-administration](../system-and-network-administration/README.md).

## [ai-web-scraping](ai-web-scraping/SKILL.md)

Turning websites into datasets or RAG corpora with the smallest pipeline that meets
the data contract. Acquisition (HTTP, browser, response capture, OCR) and extraction
(structured data, selectors, schema-constrained LLM) are chosen separately, and a
model's job is bounded: propose selectors once, interpret prose, or drive an
exceptional navigation — repeated structure runs on tested rules.

Every record carries explicit field states (`observed`, `absent`, `explicit_null`,
`unparseable`, `conflict`) and evidence bound to a hashed snapshot and its record
region, so a quote borrowed from the neighbouring product fails. References cover
Crawl4AI, Firecrawl, Scrapy, Crawlee, Scrapling, Playwright, Stagehand and browser-use,
plus crawl policy (RFC 9309 robots, retries, caching), prompt injection and SSRF,
evaluation against gold sets, and cost per accepted record. Ships an offline evidence
validator and evaluator with synthetic fixtures; no network or model calls.

**Load when** scraping, crawling or extracting from websites — especially with an LLM
in the loop — or when a scraper returns empty, partial, duplicated or invented records.

## [vllm-operator](vllm-operator/SKILL.md)

Planning, installing, running, measuring and tuning vLLM on affordable hardware —
consumer GPUs, small workstations, DGX Spark, small rented GPU servers (1-4 GPUs).
`SKILL.md` is a router and workflow: it points at the matching one of 28 numbered
references (engine fundamentals, memory capacity, prefix/KV caching and offload,
scheduling under load, benchmarking, metrics and tracing, quantization, multi-GPU,
deployment security, troubleshooting, recipes) instead of dumping them into context.
Ships measurement scripts (capacity, cost, bench sweep, stream probe, metrics
inventory), config templates (nginx, Prometheus, OTel, KV offload) and experiment
templates. Optimises correct answers within a latency budget per euro, not headline
tokens/s, and refuses to invent GPU benchmark numbers.

**Load when** serving an LLM with vLLM, sizing GPU memory or context, diagnosing TTFT/ITL
or OOM, or deciding on multi-GPU.
