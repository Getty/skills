# ACME failure isolation, rate limits and recovery

**Read when:** orders fail, renewals loop, or automation is exhausting CA limits.

## Diagnose the failed stage

| Evidence | Likely layer | Next discriminating check |
|---|---|---|
| Directory/account request fails | Outbound HTTPS, proxy, account or CA availability | Verify CA endpoint trust and structured ACME error |
| Authorization invalid | DNS/HTTP/ALPN proof or policy | Reproduce the CA-visible response, not only local solver state |
| CAA error | Issuance authorization/DNSSEC | Query relevant authoritative records and validate delegation |
| CSR/order mismatch | Finalization | Compare exact requested identifiers and CSR SANs |
| Certificate issued, service wrong | Deployment | Live fingerprint, all replicas, reload and chain |
| Repeated new accounts/orders | State/coordination | Persistent storage, concurrent jobs, retries and deployment IDs |

Keep account/order URLs and structured error types, but redact authorization secrets and credentials. Record retry time, affected identifiers, solver and observable DNS/HTTP state.

## Limits are policies, not a sleep loop

Read the CA's current limit documentation instead of embedding numeric limits in this skill. Limits may apply to accounts, addresses, registered domains, exact identifier sets and failed authorizations. Reissuing with a slightly different SAN set is not an appropriate way to evade an operational failure.

At the review snapshot, Let's Encrypt recognizes ARI-coordinated replacement orders for rate-limit exemption under its documented conditions. Its older exact-identifier renewal recognition has different exemptions and can still hit limits. Merely scheduling a command named `renew` does not prove the request qualified for ARI treatment.

Respect Retry-After and use bounded exponential backoff with jitter for retryable failures. Stop repeatedly retrying terminal invalid authorizations until the cause is fixed. Route tests to staging early rather than after production capacity is exhausted.

## CA outage and account recovery

A second CA is only a useful contingency when account setup, DNS authorization, CAA policy, client trust, issuance profiles, deployment and testing already support it. Emergency CA switching can introduce an incompatible chain or violate a client's pinning policy.

Protect and back up ACME account state. Account-key rollover, lost-account recovery and certificate revocation are different operations. Identify which authorization paths remain valid after an account or DNS credential compromise, and revoke access to those paths as part of containment.

## Staging boundaries

Never install a public CA's staging roots into production trust to make a test certificate look valid. Use a separate test environment and explicit temporary trust inputs. Pebble can accelerate ACME integration testing, but does not replace tests against the real CA's staging policies, network perspectives and rate behavior.

## Primary references

- **LE-LIMITS** — [Let’s Encrypt rate limits](https://letsencrypt.org/docs/rate-limits/).
- **LE-STAGING** — [Let’s Encrypt staging environment](https://letsencrypt.org/docs/staging-environment/).
- **RFC8555** — [Automated Certificate Management Environment](https://www.rfc-editor.org/rfc/rfc8555.html).
- **RFC9773** — [ACME Renewal Information](https://www.rfc-editor.org/rfc/rfc9773.html).
- **LE-CAA** — [Let’s Encrypt CAA processing](https://letsencrypt.org/docs/caa/).
- **LE-PEBBLE** — [Pebble as an ACME development test server](https://letsencrypt.org/2025/04/30/pebbleacmeimplementation).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
