# HTTP retrieval and crawl policy

Read when implementing URL discovery, robots handling, response classification, retries, HTTP caching or crawl termination.

## Bound the frontier

Define seeds, permitted origins and paths, and caps for pages, depth, bytes, time, concurrency and requests. Track discovered, queued, attempted, accepted, rejected and deferred URLs separately, each with its discovery source and admission reason.

Normalize only distinctions known to be irrelevant: parameter order, repeated parameters, signed URLs, trailing slashes, language routes and state-driving fragments can matter. Treat canonical links, sitemap entries, alternate-language links and model-proposed URLs as hints that pass scope and destination checks again. Cap calendars, search combinations, sort routes, session parameters and other unbounded URL spaces with explicit rules.

## Apply robots rules

Use a maintained Robots Exclusion Protocol implementation, match the crawler's declared product token, and keep the fetched policy with its retrieval time. The most specific path rule wins; allow wins ties. Robots grants neither authentication nor a content licence. [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)

| Robots fetch result | Handling |
|---|---|
| Success | Apply the parseable rules. |
| HTTP 4xx | File unavailable: access permitted; other access and rate limits stay in force. |
| HTTP 5xx or network failure | Unreachable: assume disallow, subject to the RFC's cached-policy provisions. |
| Redirect | Follow at least five hops, possibly across authorities, checking every destination. |

Refresh cached rules within 24 hours, apart from the RFC's unreachable exception. Never treat a blocked policy fetch as a permissive file. `Crawl-delay` is not in RFC 9309: support it explicitly or not at all. A robots 429 is no reason to ignore server throttling.

## Classify responses before extraction

Keep HTTP status, final URL, content type and content acceptance as separate fields. Detect sign-in pages, challenges, error documents and empty application shells behind a 200 before a model sees them.

- **Accepted:** validate media type, decoding, body limits and expected page structure.
- **Redirect:** check the destination and extend the redirect chain.
- **Authentication or denial:** switch to the authorized access path; never retry it indefinitely as a transient failure.
- **Missing:** record it, and whether a known entity needs review.
- **Rate limited:** defer per server guidance and run budget.
- **Transient failure:** bounded retries; keep the final failure class.
- **Unexpected or partial:** quarantine or reroute; never count it as a complete record set.

## Bound retries

Honor `Retry-After`, which is seconds or an HTTP date ([RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html)); otherwise back off with jitter. Cap attempts, cumulative delay and total job time, and persist long retry deadlines instead of sleeping in a worker. Count retries, redirects, robots fetches and browser-generated requests against the budgets. Never cache a 429; RFC 6585 fixes no counting identity or window. [RFC 6585](https://www.rfc-editor.org/rfc/rfc6585.html)

Schedule per origin under a global limit and reduce load when the site signals pressure. A retry never changes identity, account or scope. Keep failed attempts in the metrics.

## HTTP caching

Keep the HTTP cache apart from the evidence archive: the cache follows response directives and `Vary`, retention follows the project's access rules. [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html) Use conditional GET (`If-None-Match`, `If-Modified-Since`) when a stored body and validator exist. A 304 refers to the retained body: update its metadata, and if the body is gone, never fabricate a snapshot. Cache keys and isolation: [operations and costs](operations-and-costs.md).

## Prove the stopping condition

Record page or cursor identity, entity count, new-entity count and next cursor per page. Stop on a documented terminal condition, a repeated cursor, a cycle or a budget boundary, and record which fired. Persist frontier state so a resume skips accepted work. Deduplicate entities separately from URLs: several URLs can describe one entity, one URL can hold many.

Report scope, attempted and usable pages, exclusions, unresolved failures and termination reason. Queue exhaustion proves only that the observed frontier is done; full coverage needs an independently known inventory.
