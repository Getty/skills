# Certificate Transparency and public visibility

**Read when:** assessing public-name disclosure, suspicious issuance, or browser CT errors.

## Purpose and limits

Certificate Transparency makes public certificate issuance observable through append-only logging and associated cryptographic evidence. An SCT is a log's signed promise under the relevant protocol; it is not a CA signature, a proof that the website is harmless, or a revocation response. Browser CT acceptance rules depend on the browser's policy and accepted log lists.

RFC 9162 describes CT v2 as an Experimental protocol and obsoletes RFC 6962 as a document. That does not establish that every deployed log or browser has migrated to CT v2. Operational log APIs and deployment choices must be checked separately; Static CT APIs are another reason not to assume that an old RFC 6962 polling script covers the current ecosystem.

## Privacy and naming

Publicly issued names can become visible in public logs. Treat this as an architectural property, not a bug to hide with a firewall. Do not put personal identifiers, customer secrets or sensitive internal role names into public SANs. A wildcard changes the visible naming granularity but expands the key's impersonation scope; it is not a universal privacy fix.

For internal services, decide whether an owned public namespace plus public certificates is acceptable or whether a private trust domain is preferable. Private issuance avoids mandatory public logging only when the selected private infrastructure actually keeps the material private; do not automatically submit internal certificates to public diagnostic services.

## Monitoring workflow

Inventory owned registrable domains and delegated zones. Compare newly observed certificate names, issuers and keys with deployment records. Classify unexpected entries: approved CDN issuance, forgotten automation, preissuance artifacts, an expired project, or possible unauthorized issuance. Preserve the certificate/precertificate and log evidence before escalating to the issuer.

An alert does not itself prove key theft. Conversely, the absence of an alert is not evidence that no unauthorized certificate exists: monitors have coverage and latency limits. Define response ownership and test alerts with an authorized issuance.

## CT-specific failure diagnosis

First reproduce the browser's actual error and version. Verify normal chain and name checks independently. Then examine the SCTs, certificate dates, relevant log qualification/disqualification timelines and the browser's policy. A generic OpenSSL success is not a reproduction of Chrome's CT policy enforcement.

Keep log-monitor code separate from certificate renewal. A monitoring outage should not silently disable issuance verification, and a CA renewal success should not be mistaken for proof that the deployed browser population accepts the returned CT evidence.

## Primary references

- **RFC9162** — [Certificate Transparency v2 — Experimental](https://datatracker.ietf.org/doc/html/rfc9162).
- **CHROME-CT** — [Chrome Certificate Transparency policy](https://googlechrome.github.io/CertificateTransparency/ct_policy.html).
- **CHROME-ROOT** — [Chrome Root Program policy](https://googlechrome.github.io/chromerootprogram/crp/policy/).
- **LE-CHAINS** — [Let’s Encrypt roots and intermediates](https://letsencrypt.org/certificates/).

- **LE-CT-STATIC** — [Let’s Encrypt transition from RFC 6962 logs to Static CT APIs](https://letsencrypt.org/2025/08/14/rfc-6962-logs-eol).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
