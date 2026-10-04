# Evaluation and release checks

Define support in terms of user-visible behavior. Use an isolated Hermes home/profile with synthetic identifiers and nonproduction credentials where real services are required.

## Acceptance matrix

| Area | Required evidence for the claim |
| --- | --- |
| Native plugin | Real discovery, enablement, registration, invocation, disable/reload |
| Tool | Valid input, malformed input, bounds, refused action, external error, cancellation |
| Hook/middleware | Actual firing order, return semantics, chaining, exception before/after execution |
| Profile isolation | Two profiles in one process with distinct state, credentials, and sessions |
| Gateway | Real ingress through authorization, correct session route, reply target and thread |
| Channel interaction | Authorized/unauthorized actor, stale/duplicate callback, API failure |
| Desktop | Actual renderer load, contribution, API operation, disposal, connection switch |
| Dashboard | Bundle/manifest discovery, render, scoped route, refresh/rescan |
| MCP | Handshake, actual names, filters, denied plugin access, disconnect/reload |
| Provider | Selection, current wire/ABC contract, no-credential path, failure/recovery |
| Persistence | Process restart, interrupted write, idempotency, migration/rollback |
| Distribution | Exact package content, dependency admission, immutable revision, no hidden runtime updater |

Do not run every possible permutation. Select the tests that establish the proposed support claim and resolve concrete risks.

## Forward-use scenarios

Use realistic requests with the skill, without supplying an expected solution:

- “Create a text-metrics tool that also works as a gateway slash command.”
- “A Telegram button should run an approved operation for one team topic.”
- “Show job status in Desktop while work originates in a separate cron process.”
- “Package a memory backend for two profiles served by one gateway.”
- “Use a configured MCP server from a plugin without copying its credentials.”
- “Wrap provider requests for tracing while preserving streaming and retries.”

Assess whether the result chooses the correct extension surface, finds the current contract, maintains identity and permission boundaries, and states missing evidence.

## Verification levels

**Structural** means manifests/links/syntax parse. **Contract** means the real host imports/registers/invokes the extension correctly. **Integration** means the actual channel/backend/UI or service works. **Operational** means restart, concurrency, monitoring, and rollback are exercised.

Use those labels in release notes and support matrices. A fake PluginContext is useful for deterministic code checks but cannot prove Hermes dispatch semantics. A screenshot cannot prove backend authorization.

The official [plugin guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins) describes behavior-oriented plugin fixtures, and the [catalog policy](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission) adds admission requirements. Treat these as host checks, not a replacement for the feature's own tests.

## Stop criteria

Finish once all required user behaviors pass, critical negative cases are covered, and remaining limitations are explicit. Do not broaden testing indefinitely after the requested support claim is established.

