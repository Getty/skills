# Validation report

**Documentation snapshot: 2026-10-10.** Executed at **2026-10-10T06:38:23.495762+00:00**.

## Result

The final full local run recorded **108 PASS, 0 FAIL, 0 SKIP**. These are concrete assertions across offline validation, loopback connections, two compiled example programs and a local reverse proxy; they are not 108 independent products or a formal security certification.

[Machine-readable results](results.json) include every expected/observed outcome. [Environment](environment.json) records exact builds; [fixture manifest](fixture-manifest.json) contains public certificate metadata only. Private keys and compiled programs were generated in a temporary directory and removed.

| Test group | Executed assertions |
|---|---:|
| OpenSSL offline path validation | 31 |
| Local safety | 3 |
| Inspection tool | 5 |
| Python loopback TLS/mTLS | 23 |
| Secure probe CLI | 3 |
| Compile examples | 2 |
| External runtime loopback | 37 |
| NGINX verified upstream | 4 |

## Three complementary evidence layers

**1. Standards and policy review.** The 103-source register covers IETF PKIX/TLS/ACME standards, CA/Browser Forum requirements, root-program policies and CA announcements. Effective dates and scopes are recorded separately. See [the source register](../sources/SOURCES.md) and [policy calendar](../references/public-pki/policy-calendar.md).

**2. Implementation review.** Commands, trust-store differences, name/purpose checks, renewal behavior and deployment examples were checked against primary implementation documentation. A per-claim evidence map identifies the source and the remaining gap in [CLAIMS.md](../sources/CLAIMS.md). Review is not execution, and a current documentation page may describe a newer runtime than the test environment.

**3. Executed experiments.** The laboratory exercises both acceptance and intentional rejection. Python/OpenSSL, OpenSSL CLI, curl and Perl can share the same crypto backend; they are not represented as four independent implementations. Node reports its own linked version. Go's crypto/x509 path and Java JSSE provide additional implementation paths, but no majority-vote proof of correctness is claimed.

## Runtime snapshot

| Component | Executed build |
|---|---|
| Python | 3.13.5 |
| Python / CLI OpenSSL | 3.5.5 |
| Python cryptography | 46.0.4 |
| curl | 8.10.1 |
| Go | 1.23.2 |
| Node.js | 22.16.0 |
| Java / javac | 21.0.12.1 |
| Perl IO::Socket::SSL / Net::SSLeay | 2.089 / 1.94 |
| NGINX | 1.26.3 |

These are observed versions, not recommendations to install these particular releases or claims that they are newest. Java documentation in the references is for Java 25; the example execution was Java 21. Consult the JSON for full provider/build information.

## Review and rerun history

The first full run passed all 108 assertions. After bounding additional example response parsing, a repeat run reported 107 passes and one failure: the missing-client-certificate rejection arrived at the client as `ConnectionResetError` rather than a TLS exception. The controlled server explicitly recorded `PEER_DID_NOT_RETURN_A_CERTIFICATE`.

The harness was corrected to require the expected server-side verification failure for negative mTLS cases and to accept the corresponding TLS-alert or transport-reset presentation. It does not accept an arbitrary connection failure as evidence of correct verification. The final complete rerun passed all 108 assertions. This was a test-observation race/transport presentation issue, not a reason to weaken certificate verification.

## Structural and syntax review

[validate_package.py](../tools/validate_package.py) checks entry-point size, relative Markdown file links, registered per-reference sources, fence balance, JSON/Python syntax, shell/Node/Perl syntax, staging YAML consistency, report accounting, absence of private-key/compiled artifacts, and package checksums when present. It does not fetch remote URLs or validate Markdown fragments, Kubernetes CRD schemas or semantic correctness of every prose claim.

**Structural result:** 16 non-integrity checks passed with no failures or skips; [machine-readable structural results](structure-checks.json) are included. A separate final SHA256SUMS check verifies integrity and complete file coverage after packaging inputs are finalized.

The shell hook is syntax-checked only. The Kubernetes example is parsed and checked locally, not applied to a cluster. NGINX has stronger evidence: actual secure front-end requests return 200 for a valid upstream and 502 with an upstream-name error for the wrong-name fixture.

## What was not executed

No production ACME enrollment, real DNS challenge, external TLS scan, root-store mutation, browser CT policy, live OCSP service, root-program inclusion, HSM ceremony, OpenBao/step-ca/SPIRE deployment, database, mail server, mobile device, Windows/macOS trust workflow, ECH, PQC, QUIC or DTLS was tested. Those sections are referenced design/diagnostic guidance with explicit implementation verification steps.

The CRL tests concern a local leaf CRL, not every revocation mechanism. The URI authorization rule is not a complete SPIFFE verifier. The NGINX configuration was exercised with substituted loopback paths, names and ports, not deployed unchanged to production. The `.test` certificates are not public-Web-PKI-compliant enrollment outputs.

## Reproduce and extend

From the package root run `python labs/run_lab.py --output /tmp/ssl-pki-results-new`, using a new output path. A minimal host may skip optional runtimes; compare both counts and versions, not only exit status. Run `python tools/validate_package.py` separately for structure.

For a production target, extend the matrix with its real OS/root store, runtime/application, chain selection, network path, refresh behavior, revocation policy and explicit authorization. Recheck dated rules immediately before use. Passing this package's lab does not establish that an arbitrary production configuration is secure.
