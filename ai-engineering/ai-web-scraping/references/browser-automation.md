# Browser capture and bounded navigation

Use this when the data depends on JavaScript, an authorized session, or bounded UI interaction. Nothing here authorizes installing another browser, attaching to a personal profile, exporting cookies, or bypassing the host's browser integration.

## Capture contract

Fix before opening the browser:

- Authorized origins, start URLs, account context, allowed interactions.
- Page state: locale, query, filters, sort, variant, date range.
- Ready or explicitly empty state; record identity field.
- Limits on pages, actions, runtime, retries, downloads, concurrent contexts.
- Evidence: requested/final URL, capture time, HTTP status, the response or DOM fragment used, extraction version.

Screenshot, rendered DOM, network response, and accessibility snapshot are different representations; keep the one the extractor used. Playwright returns HTTP 404 and 500 responses without throwing, so check response and page state after every navigation. [Page API](https://playwright.dev/docs/api/class-page)

## Readiness and extraction

Wait for a site-specific condition: results container ready, loading marker gone, relevant response arrived, or explicit empty-state message. Let a legitimate empty result satisfy readiness; waiting for the first row turns zero results into a timeout. Actionability checks make an action executable, not the dataset complete. [Auto-waiting](https://playwright.dev/docs/actionability)

Locate by observed role, label, or stable attribute, scoped to the container. Use `.first()` only when first-item semantics are the task. Re-resolve locators after rerenders. [Locators](https://playwright.dev/docs/locators)

`locator.all()` does not wait for a dynamic list; wait for the state first, then extract a bounded batch in one operation, keeping raw displayed values. [Locator API](https://playwright.dev/docs/api/class-locator#locator-all)

Never use `networkidle` (Playwright discourages it) or a fixed sleep as the only completion condition: background traffic prevents quiescence, and quiescence can precede the interaction. [Load states](https://playwright.dev/docs/api/class-page#page-wait-for-load-state)

A click that succeeds but changes nothing usually hit an unhydrated control; verify the resulting state instead of retrying blindly, which can execute it twice. [Hydration](https://playwright.dev/docs/navigations#hydration)

## Observed response data

When an authorized action loads structured data, extract that response instead of reparsing rendered text. Confirm it belongs to the intended operation; seeing a request does not permit enumerating other private endpoints.

Register the response wait before the action, matching observed origin, path, method, and distinguishing parameters rather than a substring. [Network events](https://playwright.dev/docs/network#network-events) Selectors and endpoint come from inspection:

```ts
const [response] = await Promise.all([
  page.waitForResponse(r => {
    const u = new URL(r.url());
    // Also match the observed cursor/page/filter parameters when applicable.
    return u.origin === expectedOrigin
      && u.pathname === observedCatalogPath
      && r.request().method() === "GET";
  }, { timeout: 15_000 }),
  page.getByRole("button", { name: "Next", exact: true }).click(),
]);
if (!response.ok()) throw new Error(`Catalog HTTP ${response.status()}`);
const payload: unknown = await response.json();
// Validate the payload schema and requested page/cursor before accepting records.
```

Keep non-2xx responses in the predicate and fail on them; filtering them out turns an HTTP error into a misleading timeout. Archive only permitted content, with credentials redacted from request metadata.

Service workers can hide requests from interception. When events are missing, compare with service workers blocked, if permitted, and record that choice. [Service workers](https://playwright.dev/docs/network#missing-network-events-and-service-workers)

## Pagination and virtualized lists

Run each collection as a state machine:

1. Capture query, sort, filters, page/cursor, and stable record IDs.
2. Validate and persist the batch idempotently before advancing.
3. Register the next-state wait, advance once, verify progress.
4. Stop on an observed terminal signal or a budget.
5. Report the reason and whether completeness was established.

Track cursors, page identities, and record IDs separately. A repeated cursor is a loop, not the end; a new URL with identical IDs is a broken paginator. Deduplicate overlap without collapsing variants or historical versions.

Virtualized lists drop old rows from the DOM: scroll the actual container and collect each batch as it appears, never once at the bottom. A constant row count or scroll height does not prove completion; prefer an authorized response stream or export.

Record `end_signal`, `budget_exhausted`, `no_progress`, or `error` as termination reason, and label the last three partial unless independent evidence proves completeness. Compare with a published total only for the same filters, variants, permissions, and period. For changing feeds, use a time boundary or stable sort if offered.

## Frames, shadow DOM, and visual content

Select frames with a frame locator (page-level calls hit the main frame) and record the frame URL with its evidence; a top-level snapshot omits embedded documents. [Frames](https://playwright.dev/docs/frames)

Locators pierce open shadow roots; XPath does not, and closed roots are unsupported. Check this before calling an empty result missing data. [Shadow DOM](https://playwright.dev/docs/locators#locate-in-shadow-dom)

For canvas, image tables, or charts, look for a textual or structured source first. Use OCR/vision only when needed, keeping coordinates, viewport, scale, and uncertainty; never turn a chart estimate into an exact value. Distinguish occluded, not rendered, and absent.

## Sessions and downloads

Use one context per identity and job, reusing only authorized state. Playwright storage state holds impersonation-capable cookies and headers: keep it out of repositories and diagnostics. It does not capture session storage. [Authentication](https://playwright.dev/docs/auth)

Register the download wait before the triggering action and save the file to a controlled path before closing the context; Playwright deletes context-managed downloads on close. Treat suggested filenames as untrusted; verify type, size, and parseability. Never execute downloads. [Downloads](https://playwright.dev/docs/downloads)

A downloaded file is a new extraction input with its own source URL, timestamp, content hash, and link to the interaction.

## Failure diagnosis

| Symptom | Inspect next |
| --- | --- |
| Empty rows | Ready/empty state, selected frame, filters, session, response status |
| Repeated rows | Cursor movement, response matching, stable IDs, paginator loops |
| Click without change | Hydration, overlay, wrong duplicate label, expected state |
| Missing requests | Service worker, cache, late listener, incorrect endpoint predicate |
| Lost file | Unawaited download, context cleanup, incorrect persistence path |
| Wrong values | Locale, variant, hidden stale markup, personalized session, OCR |

Retry transient transport failures within budget; fix a proven selector or state assumption before retrying a structural failure. Report login walls and denials as acquisition failures, never as extractor input.
