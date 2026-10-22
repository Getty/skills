# Security verification and release evidence

## Select meaningful tests

Choose tests from the threat model and material change. Use synthetic tenants and canary secrets. Test only systems and scopes actually authorized. A test against production, third-party infrastructure, or real customer data may need a different authorization than an ordinary local test; do not silently broaden scope.

Map each test to a control ID, requirement/source, environment, version, preconditions, expected invariant, actual result, evidence reference, and reviewer. Distinguish automated checks from manual judgment. These tests support risk-based duties under SEC-GDPR, SEC-BSIG-CONTROLS, SEC-NIS-IR or SEC-CRA where applicable; no finite suite certifies legal compliance.

| Change/risk | Test | Release-relevant evidence |
|---|---|---|
| New tenant objects | Use another tenant's identifiers across API, retrieval, export and attachments | Authorization denial before data reaches model/output |
| Revoked user | Retry old token, cached result, delayed job, existing signed link | Current access policy enforced; explicit expiry model |
| New tool | Model proposes unauthorized destination/operation | Deterministic denial; no side effect; safe audit event |
| RAG ingestion | Malicious instructions in document/tool output | No change in authority or external disclosure |
| Renderer | Generated HTML/URL/attachment with unsafe sink | Encoding/CSP/resource policy blocks execution/exfiltration |
| Provider fallback | Primary unavailable | Approved destination/settings, no unnoticed data transfer |
| Build/update | Tampered artifact or invalid signature | Rejection and safe recovery |
| Secrets | Synthetic key appears in input/error | Redaction and restricted exposure; no observability leak |
| Availability | Resource exhaustion/cancel/provider outage | Quota, circuit breaker, cleanup and observed recovery |
| Backup | Restore into isolated environment | Integrity, permissions, keys and deletion/suppression reapplied |
| Incident | Out-of-hours synthetic threshold event | Correct owner, qualified clocks, draft route, no live fake filing |

## Evaluate findings honestly

Use separate fields for legal applicability, implementation status, evidence status, and risk. `not_applicable` requires positive scope evidence; `not_tested` is not a pass. `verified` refers to a specified observation, not a claim about every environment.

Assess severity using exploitability, impact on people, tenant reach, privileges, persistence, and available containment. A numerical CVSS score is an input, not the entire business/legal risk assessment. Include uncertainty and evidence that could change the result. Record false positives and normal-workflow failures in AI control tests.

## Gate decisions

- `ready_for_owner_decision`: scoped controls have adequate current evidence; residual risks and owners are explicit.
- `restricted_release`: the affected feature is safely disabled or isolated and the release cannot bypass the restriction.
- `blocked_for_remediation`: an applicable prerequisite or material uncontrolled exposure prevents the proposed action.
- `pending_scope_or_legal_review`: a consequential fact/interpretation remains unresolved; identify the narrow decision and owner.

These are internal decision labels. The agent cannot waive law, sign a declaration, or approve its own unapproved exception. Use the actual governance authority and preserve prior user authorization for reversible fixes. Do not stop unrelated authorized work because one feature is blocked.

## Evidence freshness

Attach tests to commit and deployment configuration. A model, tool schema, access policy, feature flag, provider, region, parser, or logging change can invalidate prior evidence. Define expiry by risk and change triggers; do not invent a statutory uniform monthly review. Track decisions affected by a stale source or test.

Protect evidence as potentially sensitive. Use hashes, redacted logs and restricted links instead of customer content in public CI artifacts. Preserve enough context to reproduce a failure without redistributing harmful material or real credentials. Clearly label synthetic examples and simulated regulator notices.

## Report pattern

Lead with the concrete proposed action and current conclusion. Then explain the requirement, observed finding, practical impact, fix, owner and verification. Example: “Hold the new public-share feature: the download endpoint accepts another tenant's object identifier; test SEC-TEN-04 reproduced disclosure on build X. Enforce object authorization and retest share-link revocation before enabling the flag.” Avoid “the platform is noncompliant” when evidence only supports a feature-specific finding.
