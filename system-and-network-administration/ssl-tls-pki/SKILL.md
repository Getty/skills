---
name: ssl-tls-pki
description: Design, deploy, audit, operate, and debug SSL/TLS, public Web PKI, private certificate authorities, ACME/Let's Encrypt, mTLS, certificate chains, trust stores, and TLS clients across operating systems and runtimes. Use for HTTPS, STARTTLS, QUIC/DTLS boundaries, certificate renewal, CA rotation, client interoperability, and TLS incident analysis.
---

# SSL, TLS & PKI Engineering

## Contract

Treat “SSL” as the user's umbrella term, not a request to enable obsolete SSL protocols. Identify the actual transport, authentication purpose, implementation, and trust boundary before prescribing a fix. Distinguish standards, root-program policy, CA service policy, application behavior, and local operational choices.

This is a modular skill, not a single exhaustive prompt. Read only the branches needed from [CONTENTS.md](CONTENTS.md). Read [SECURITY.md](SECURITY.md) before commands affecting trust, keys, or production. The reference snapshot is **2026-10-10**; recheck dated claims in [the policy calendar](references/public-pki/policy-calendar.md) and [claim ledger](sources/CLAIMS.md).

## Workflow

1. **Inventory:** topology, endpoint/reference identity, client/server builds and TLS backends, trust stores, time, certificate purpose, DNS, proxies, owners, and approved test scope. Record unknowns rather than inventing them.
2. **Model:** draw every TLS hop; label termination, re-encryption, peer verification, enrollment, trust distribution, and authorization. A trusted client certificate is not an authorization policy.
3. **Select:** public CA, private PKI, workload identity, or a different protocol; document the compatibility and operational constraints.
4. **Design:** issuer hierarchy, profiles, enrollment authorization, key custody, revocation, renewal/deployment, monitoring, root rotation, and recovery. Separate bootstrap from steady-state operation.
5. **Implement:** use maintained libraries and explicit identity verification. Never solve a failure by disabling verification, globally lowering security levels, or installing a root obtained from an unauthenticated peer.
6. **Test:** positive and negative paths with the *real consuming client*. Check the live certificate on every termination point, not merely a file or controller status. Use [acceptance tests](references/operations/acceptance-tests.md).
7. **Operate:** stage changes, preserve authorized rollback, measure deployment convergence, and rehearse issuer outage and compromise.
8. **Report:** explain evidence, residual uncertainty, versions, changes, rollback, and which tests were actually executed.

## Routing

| Need | Start here |
|---|---|
| Explain certificates, handshakes, names, chains | [Foundations](references/foundations/scope-and-terminology.md) |
| International public trust and current rules | [Web PKI governance](references/public-pki/global-web-pki.md) |
| Let's Encrypt and automated issuance | [ACME state machine](references/acme/protocol-state-machine.md) |
| Build a private SSL infrastructure | [Trust-domain architecture](references/private-pki/architecture.md) |
| Reverse proxy, database, registry, email | [Deployment map](references/deployment/termination-and-proxies.md) |
| Browser, OS, language-specific failures | [Client capability matrix](references/clients/capability-matrix.md) |
| Diagnose a failing connection | [Incident runbook](references/debugging/incident-runbook.md) |
| Verify assumptions experimentally | [Local lab](labs/README.md) and [validation report](validation/REPORT.md) |

## Required output for substantial tasks

Produce a scoped topology and trust model; a decision record; version-specific changes; positive/negative acceptance criteria; lifecycle and incident procedures; and primary-source references. Mark architecture proposals as proposals and unexecuted commands as unexecuted. For debugging, maintain **hypothesis → evidence → smallest fix → retest**.

## Integration

Use alongside the relevant networking, DNS, reverse-proxy, Docker, Kubernetes, PostgreSQL, OpenBao, application-runtime, or observability skill when available. No companion skill is required to read this package. Never silently convert this skill into a CA product installer or a production root ceremony.
