# Dated policy calendar: current versus announced

**Read when:** using a remembered certificate lifetime, EKU rule, ACME profile or TLS standard.

## Snapshot: 2026-10-10

These dates are scoped to their issuing policy. Recheck the linked primary sources before an implementation or migration. A maximum allowed lifetime is not a promise that a particular CA offers it. Limits tied to an issuance date do not automatically shorten every previously issued certificate.

### Public TLS subscriber certificates: CA/Browser Forum

| Certificate issued | Maximum validity | Maximum domain/IP validation-data reuse |
|---|---:|---:|
| Immediately before 2026-03-15 | 398 days | 398 days |
| 2026-03-15 through 2027-03-14 | 200 days | 200 days |
| 2027-03-15 through 2029-03-14 | 100 days | 100 days |
| From 2029-03-15 | 47 days | 10 days |

These are maxima, not recommended target durations; the requirements also give shorter SHOULD-level values and precise day calculations. Organization/subject identity reuse is a separate rule. This table is not a universal constraint on private-PKI client certificates.

### Let's Encrypt service policy

| Item | Status at the snapshot |
|---|---|
| `classic` default lifetime | 90 days |
| `tlsserver` profile | 45 days |
| `shortlived` profile | 160 hours; supports DNS and public IP identifiers |
| New clientAuth certificates | No longer available through any profile after 2026-07-08 |
| OCSP service | Ended 2025-08-06 |
| Default 64-day staging certificates | Announced for 2026-10-14; still future |
| Default 64-day production certificates | Announced for 2027-02-10; still future |
| Default 45-day production certificates | Announced for 2028-02-16; still future |

Profile availability is discovered from the selected ACME directory. Do not infer production availability from staging. DNS-PERSIST-01 was announced as an implementation/draft effort; this package does not assert general availability.

### Root-program and standards distinctions

Chrome's root-program policy distinguishes new subordinate disclosure requirements from leaf issuance requirements. The serverAuth-only requirement for new subscriber certificates has a **2027-03-15** effective date; the **2026-06-15** subordinate rule is not that same deadline. Let's Encrypt stopped clientAuth earlier under its own service timeline.

Mozilla Root Store Policy 3.1 took effect on **2026-07-01**. TLS engineering references also changed in July 2026: RFC 9846 revises TLS 1.3, RFC 9851 freezes TLS 1.2 features, RFC 9852 addresses new TLS-using protocols, and RFC 10015 updates obsolete TLS/DTLS 1.2 key-exchange guidance.

## Update protocol

Record retrieval date, document version, actual effective date, affected purpose and operator action. Read amendments and official implementation announcements. A blog publication date is not an effective date, and a draft is not an implemented feature. Preserve these distinctions in any generated answer or configuration.

## Primary references

- **CABF-BR** — [CA/Browser Forum TLS Baseline Requirements — current HTML](https://cabforum.org/working-groups/server/baseline-requirements/requirements/).
- **CABF-SC081** — [Ballot SC081v3: validity and validation-data reuse schedule](https://cabforum.org/2025/04/11/ballot-sc081v3-introduce-schedule-of-reducing-validity-and-data-reuse-periods/).
- **LE-PROFILES** — [Let’s Encrypt certificate profiles](https://letsencrypt.org/docs/profiles/).
- **LE-64D** — [64-day certificates: announcement on 2026-10-07](https://letsencrypt.org/2026/10/07/64-day-certs).
- **LE-45D** — [Let’s Encrypt planned 45-day default lifetimes](https://letsencrypt.org/2025/12/02/from-90-to-45).
- **LE-CLIENTAUTH** — [End of TLS client-authentication certificate support](https://letsencrypt.org/2025/05/14/ending-tls-client-authentication).
- **LE-OCSP** — [Let’s Encrypt OCSP end of life](https://letsencrypt.org/2025/08/06/ocsp-service-has-reached-end-of-life).
- **LE-PERSIST** — [DNS-PERSIST-01 announcement](https://letsencrypt.org/2026/02/18/dns-persist-01).
- **CHROME-ROOT** — [Chrome Root Program policy](https://googlechrome.github.io/chromerootprogram/crp/policy/).
- **MOZILLA-ROOT** — [Mozilla Root Store Policy](https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/policy/).
- **RFC9846** — [TLS 1.3 — July 2026 revision](https://datatracker.ietf.org/doc/html/rfc9846).
- **RFC9851** — [TLS 1.2 feature freeze](https://datatracker.ietf.org/doc/html/rfc9851).
- **RFC9852** — [New protocols using TLS must require TLS 1.3](https://www.rfc-editor.org/rfc/rfc9852.html).
- **RFC10015** — [Deprecating obsolete key exchange methods in TLS 1.2 and DTLS 1.2](https://datatracker.ietf.org/doc/html/rfc10015).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
