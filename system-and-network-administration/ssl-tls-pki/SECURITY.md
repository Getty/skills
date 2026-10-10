# Security and operational boundaries

All material is a technical reference and a starting point for a reviewed deployment. No example is a universal production hardening profile.

Run active probes only against authorized endpoints, with agreed limits. The lab binds only loopback and generates disposable keys; its CA must never enter an OS, browser, corporate or production trust store. The general diagnostic tool contacts exactly the endpoint selected by the operator; it is not an asset-discovery scanner.

Never upload private keys, PKCS#12 bundles, CA state, recovery shares, DNS API tokens, ACME account keys, TLS session tickets, or traffic secrets to support chats. Public certificates can still expose internal names and topology. Redact incident artifacts accordingly. Packet captures and SSLKEYLOGFILE output are restricted evidence, not ordinary logs.

A trust-store modification can authorize interception. Confirm the root fingerprint through an authenticated independent channel, scope the installation, identify the owner and removal path, and obtain change approval. Do not distribute issuer private keys as part of a trust bundle.

Do not use disabled verification, arbitrary certificate acceptance callbacks, insecure registry settings, or global crypto-policy downgrades as a repair. A tightly isolated diagnostic exception must never be copied into application defaults; the included tools deliberately provide no such switch.

Before changing a CA or deployed credentials, verify backup recoverability, rollback eligibility, configuration syntax, file ownership, restart/reload behavior, and monitoring. A compromised certificate or key is not an eligible rollback target. Root and intermediate compromise requires a wider response than ordinary renewal.

The scripts do not implement a production CA, ACME server, complete browser validator, OCSP client, or SPIFFE verifier. Their boundaries are documented in [labs/README.md](labs/README.md). Inspect [validation/REPORT.md](validation/REPORT.md) for the exact execution scope.
