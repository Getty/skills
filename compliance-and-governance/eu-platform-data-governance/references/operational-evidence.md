# Operational evidence and monitoring

Sources: D1, D8, D11. These are recommended operational mechanisms supporting accountability; a chosen review cadence is not a statutory deadline.

## Make a record useful to an independent reviewer

Capture control ID, applicable obligation/source, exact scope, owner, system/configuration version, observation date, method, result, limitations, evidence path and next trigger. Distinguish a contract commitment, a configured setting, a supplier attestation, a synthetic test and a production completion record. They answer different questions.

Do not manufacture evidence from an expected behaviour or a green dashboard. A deletion job returning success for one tenant cannot prove all stores, vendors or historic backups are covered. A provider flag screenshot cannot prove the service never creates other logs.

## Minimal monitoring set

| Monitor | Useful signal | Response |
| --- | --- | --- |
| Retention | Expired records, unenforced classes, unexpected indefinite policies | Investigate owner/configuration; prioritise sensitive exposure |
| Erasure/restriction | Failures, retries, stale derivatives, restore recreation | Reconcile and report partial completion accurately |
| Provider routes | Unapproved endpoints, fallback recipients, region/support changes | Stop affected unapproved route via authorised controls |
| Reuse | Customer data reaching unapproved training/evaluation jobs | Contain and reopen purpose/role/incident review |
| Supplier changes | Contract/subprocessor notices and certification changes | Reassess affected processing and customer obligations |
| Evidence freshness | Controls without a version/date/owner | Collect actual evidence; avoid broad legal clearance |

Use metadata and aggregated counters where sufficient. The monitoring system should not become a second unrestricted copy of all customer prompts.

## Verification scenarios

Test representative complex paths, not just the happy-path database delete:

- Delete a synthetic source document after it has been embedded, summarised, cached and sent to a batch job. Verify all affected paths and document provider limitations.
- Restrict a subject while an asynchronous retry is pending; ensure the retry does not reintroduce processing.
- Restore an old snapshot containing a previously erased fixture; confirm suppression before user access.
- Revoke a tenant/document permission and query by semantic similarity, exact ID and shared link.
- Change a model fallback and detect a new data recipient before production data flows.
- Expire a supplier approval in the registry and verify that the release gate reports a concrete gap, rather than inventing a legal invalidity finding.

Use deterministic synthetic canaries for access and lifecycle tests. A privacy model-extraction evaluation may be probabilistic: report sample size, attack assumptions, model version and uncertainty. Do not represent absence of detected extraction as proof of anonymity.

## Protect and retire evidence

Separate public configuration/code proof from confidential contracts, risk assessments and incident details. Apply least privilege, integrity/version history and a purposeful retention schedule. Redact credentials and unnecessary personal information in tickets and CI logs. Avoid recording personal payloads merely to prove that personal payloads were deleted.

Conclude with actual findings, scope limits, residual questions and next required action. Once the affected controls are sufficiently verified, stop optional testing and proceed with the authorised workflow.
