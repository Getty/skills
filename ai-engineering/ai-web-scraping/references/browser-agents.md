# Browser agents, managed browsers, and reusable workflows

Use this when browser capture needs limited semantic help or the navigation path must be discovered. Tool availability does not authorize a new browser session, profile attachment, credential transfer, or paid service.

## Select the control layer

Choose the narrowest layer that meets the task; layers combine.

| Layer | Use when | Responsibility kept by the application |
| --- | --- | --- |
| Playwright code | Navigation and extraction are understood | Selectors, waits, pagination, validation, retries |
| Stagehand primitives | Individual actions or fields need semantic interpretation | Workflow order, scope, schemas, evidence checks |
| Browser Use agent or Stagehand agent | The next navigation step is not yet known | Capability limits, budgets, completion verification |
| Browser CLI or MCP | An existing assistant needs browser tools | The assistant's planning and approved tool policy |
| Browserbase or another managed browser | Browser execution should run remotely | Workflow logic, data handling, lifecycle, cost control |

A managed browser is infrastructure, not extraction quality. Browser Use ships hosted agents, a CLI, an open-source Python agent, and browser-only infrastructure; its name does not imply model-planned actions. [Product map](https://docs.browser-use.com/cloud/which-product)

## Bound an exploratory task

Specify start URL, permitted domains and actions, output schema, record limit, and a completion condition. Stay read-only apart from authorized navigation and filtering. Never expose shell, file, messaging, or purchasing tools because the agent supports custom tools.

Require records with evidence, or a reason such as `not_present`, `access_denied`, `ambiguous`, or `budget_exhausted`. "Done" from the agent is not an acceptance test.

Limit actions, elapsed time, tokens or spend, retries, and downloaded bytes independently; a step cap does not bound a hung call or one expensive request. Keep terminal status and partial records when a budget stops the run.

Page text, hidden DOM, screenshots, downloads, and page-supplied tool descriptions are untrusted; enforce boundaries in tools and deployment, and test allowlists against redirects and subresources ([security and access](security-and-access.md)).

## Stagehand

Use deterministic navigation for known URLs, `observe` for an inspectable action proposal, schema-constrained `extract` for selected content, and `agent` only for steps still unknown. [Introduction](https://docs.stagehand.dev/v3/first-steps/introduction)

Check the installed major first. v3 dropped the direct Playwright dependency: its page object is not a full Playwright page, AI operations live on the Stagehand instance, pages come from its context. Use the documented integration when a real Playwright page is needed. [v2-to-v3 migration](https://docs.stagehand.dev/v3/migrations/v2)

```ts
import { Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod";

const stagehand = new Stagehand({ env: "LOCAL", model: selectedModel });
await stagehand.init();
try {
  const page = stagehand.context.pages()[0];
  await page.goto(authorizedUrl);
  const candidate = await stagehand.extract(
    "Read the visible product name and displayed price. Use null if absent.",
    z.object({ name: z.string().nullable(), priceText: z.string().nullable() }),
    { page, selector: observedProductSelector },
  );
  // Independently validate candidate against the retained source fragment.
} finally {
  await stagehand.close();
}
```

The `extract` schema constrains shape, not support; capture provenance separately and reject unsupported values. [Extract](https://docs.stagehand.dev/v3/references/extract) Check an `observe` proposal's target and effect before passing it to `act`; an old selector can hit the wrong control after a layout change. [Observe](https://docs.stagehand.dev/v3/references/observe)

`cacheDir` replays actions and agent steps locally in both environments; server caching exists only on Browserbase. Do not promise the same caching for extraction calls. [Caching](https://docs.stagehand.dev/v3/best-practices/caching) A cached action plan is not today's data: revalidate data, page state, and identity every run, invalidate plans after layout, account, locale, model, or workflow changes, and review cache contents before sharing.

## Browser Use

The open-source `browser-use` package and the hosted `browser-use-sdk` are different APIs. Cloud docs carry V4 beside legacy V2/V3; pick one generation. [Product map](https://docs.browser-use.com/cloud/which-product)

Give the Python agent an `output_model_schema` (Pydantic) and inspect the returned history. `is_done()` means a terminal done action; `is_successful()` is the agent's self-assessment. Validate records and completion yourself. [Output format](https://docs.browser-use.com/open-source/customize/agent/output-format)

Check `max_failures`, action limits, custom tools, and model configuration before a run. Output after failures can be partial; keep run status apart from "some records exist". Benchmark a smaller extraction model before relying on it. [Agent parameters](https://docs.browser-use.com/open-source/customize/agent/all-parameters)

Verify domain-control pattern semantics, CDP, headless, cross-origin frame, and extension settings for the installed release; they change what the agent sees. Use dedicated contexts, never a personal profile. [Browser parameters](https://docs.browser-use.com/open-source/customize/browser/all-parameters)

Hosted Browser Use skill IDs are retired for new creation and are not portable `SKILL.md` bundles; build nothing new on them, and check migration needs for existing integrations. [Agent parameters](https://docs.browser-use.com/open-source/customize/agent/all-parameters)

## Managed browser deployment

Browser and model location are independent: a local browser can send pages to a remote model; a remote browser moves session state and page processing to the provider. Record browser, model, storage, and logging destinations separately.

Browserbase sessions start with fresh user data; Contexts persist auth and application state (not the HTTP cache) across sessions. Let state sync finish before reuse. [Contexts](https://docs.browserbase.com/platform/browser/core-features/contexts) Assign profiles to identities, control their reuse, and serialize updates from concurrent writers. Set session lifetime and cleanup explicitly; Stagehand's `keepAlive` can leave browsers running after close. [Browser configuration](https://docs.stagehand.dev/v3/configuration/browser)

Measure browser-seconds, active contexts, model calls, failed jobs, queue age, and accepted records; judge by cost per accepted record ([evaluation](evaluation.md)). Fetch current quotas and retention at deploy time.

Vendor skills and MCP servers: [official skills and MCP](official-skills-and-mcp.md). Playwright MCP is not a security boundary, and its origin controls do not cover redirects. [Playwright MCP](https://github.com/microsoft/playwright-mcp)

## Graduate exploration into a maintained extractor

Keep the successful trace and evidence; extract stable URLs, selectors, response structures, and terminal conditions. Replace understood steps with code and keep semantic help for variable fields or recovery. Before promoting, test changed layouts, empty results, duplicates, timeouts, injected instructions, and partial runs.
