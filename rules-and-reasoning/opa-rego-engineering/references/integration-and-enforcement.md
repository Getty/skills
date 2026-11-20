# Integration and enforcement

## Choose a boundary

A local service offers a shared endpoint to multiple application languages. An
embedded SDK lets the application own lifecycle and data loading. Wasm needs a
compatible host and built-in contract. Compare real update behavior, latency, and
failure domains instead of declaring one approach universally best.

Identify the enforcement point. Evaluating policy returns data; the caller must
block or permit the actual operation. Keep that check close enough to resource
use that a concurrent change does not invalidate the decision.

## Consume the Data API correctly

For `data.workspace.authz.allow`, use the corresponding `/v1/data/...` path and
wrap request facts under `input`. The response contains `result` when defined.
An HTTP success without `result` differs from `result: false`. API errors, malformed
responses, and timeouts are separate outcomes. The envelope also differs from
`opa eval --format=json`. [REST API](https://www.openpolicyagent.org/docs/rest-api).

For Boolean permission require the JSON Boolean true, not 1, `"true"`, a nonempty
object, or HTTP 200. For a structured result validate the object and its `allow`
field. The bundled helper handles only saved Boolean responses and cannot attest
to TLS identity, HTTP status, freshness, or provenance.

## Preserve identity and resource meaning

Normalize method/path/action mappings. Test encoding, duplicate slashes, proxy
headers, aliases, and case sensitivity if relevant. Authorize the same canonical
resource that the application later reads or modifies. Avoid checking one tenant's
metadata while acting on another object through an unchecked identifier.

Bind a decision to the relevant resource version or transaction. When ownership
can change concurrently, recheck or use an appropriate consistency mechanism before
commit. A policy engine does not remove time-of-check/time-of-use problems.

## Handle failure deliberately

Set bounded timeouts and an explicit response to missing entrypoints, unavailable
services, stale policy, and stale identity data. Preserve denial versus technical
failure in diagnostics. Do not retry beyond the caller's time budget or create an
availability failure through unbounded policy-service retries.

Protect policy/data management separately from evaluation. An actor who can modify
trusted data or replace rules can change decisions without exploiting a logical
bug. Apply deployment authentication, authorization, and transport controls.
[Security guidance](https://www.openpolicyagent.org/docs/security).

Log a correlation ID and the policy/data revision needed for reproduction, with
sensitive fields redacted. If a cached true answer is used, document its cache key,
lifetime, and invalidation on revocation or resource changes. Cache compilation
separately from decisions: their validity periods need not resemble each other.
