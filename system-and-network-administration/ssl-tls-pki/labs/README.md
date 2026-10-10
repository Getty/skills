# Disposable TLS / PKI laboratory

**Read before running:** [SECURITY.md](../SECURITY.md). Nothing here is a production CA or an OS trust installer.

## What the runner does

The runner generates fresh keys/certificates in a private temporary directory, executes offline path validation and loopback TLS requests, runs available client examples, then removes all temporary keys and processes. The output directory contains only public fixture metadata, exact runtime versions and test outcomes. Names use `.test`; servers bind only `127.0.0.1` on ephemeral ports. No public ACME orders, external target scans, DNS mutations or system trust changes occur.

The current suite has 108 tests when all documented runtimes are available. It covers paths, names, SAN/CN differences, IP SANs, EKU, dates, constraints, cross-signing, trust overlap, CRLs, TLS 1.2/1.3, HTTP/1.1 ALPN, mTLS authentication/authorization, secure inspection/probe tools and authenticated NGINX upstreams. The negative fixtures are deliberately unsafe certificates; they must not escape the lab trust domain.

## Requirements and execution

Use Python 3.11+ with `cryptography >=42` and OpenSSL CLI 3.0+. The tested Python dependency is recorded in [requirements.txt](requirements.txt); it is a reproducibility pin, not a claim that it will remain the newest release. The tested OS and all runtime versions are in [environment.json](../validation/environment.json).

An isolated environment can be prepared with:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r labs/requirements.txt
python labs/run_lab.py --output /tmp/ssl-pki-results-01
```

The package-install step may use the network; **the lab itself does not need internet access**. The output path must not already exist, and its parent must exist. Do not run as root merely to avoid a permission error. No low ports or system-level service registration are needed.

curl, Node.js, Perl with IO::Socket::SSL/Net::SSLeay, Go, Java/Javac and NGINX add the corresponding tests. Missing optional runtimes are recorded as `SKIP`, not silently counted as passing. Go is compiled with downloads disabled; Java and Go binaries remain in the temporary directory. The suite is developed for Linux; it is not a Windows/macOS harness. It may take longer on an uncached Go toolchain.

Exit status is zero only when no executed test fails. Read `results.json`, including failure diagnostics and limitations. A test failure does not authorize disabling verification. Client-authentication alerts can surface as a reset; those cases require the corresponding server-side certificate-verifier error, not an arbitrary transport failure.

## Inspect a fixture manually

The generator only creates a **new** directory and refuses overwrite:

```sh
python labs/generate_pki.py /tmp/ssl-pki-manual
python tools/inspect_cert.py /tmp/ssl-pki-manual/server.fullchain.pem
```

`inspect_cert.py` parses public metadata; it does not establish trust. In another terminal, an intentionally local test server can be started with the generated material:

```sh
openssl s_server -accept 127.0.0.1:8443 \
  -cert /tmp/ssl-pki-manual/server.pem \
  -cert_chain /tmp/ssl-pki-manual/intermediate.pem \
  -key /tmp/ssl-pki-manual/server.key \
  -min_protocol TLSv1.2 -www
```

The OpenSSL flags above were checked against the bundled environment, but this interactive invocation is not an additional counted integration test. From a separate terminal:

```sh
python tools/tls_probe.py --connect-host 127.0.0.1 --port 8443 \
  --name api.svc.test --cafile /tmp/ssl-pki-manual/root.pem --http
```

Stop the manual server when finished and remove the explicitly chosen temporary directory after verifying its path. The automatic runner handles its own cleanup. Neither workflow asks you to add the root to global trust.

## What the fixtures demonstrate

Two roots and issuing intermediates allow trust-overlap and cross-signing experiments. The same issuer key is cross-signed only to demonstrate path construction. Leaf fixtures exercise good and bad DNS/IP identities, wildcards, CN conflicts, missing SANs, validity, purposes, RSA versus EC keys and unknown critical extensions. Other fixtures violate CA/path/name constraints or supply fresh/stale CRLs.

Client URIs resemble SPIFFE IDs solely to make identity/authorization separation concrete. The server uses an exact allowlist after certificate verification; it does **not** implement complete SPIFFE X.509-SVID validation. Keys are randomly regenerated and dates are relative to execution, so runs are behaviorally reproducible, not byte-for-byte identical.

## Boundaries

No production ACME, browser CT/revocation enforcement, HSM, OpenBao cluster, step-ca enrollment, SPIRE workload attestation, live database, mobile OS, ECH, PQC, QUIC, DTLS or e-mail server is exercised. Those references remain documentary guidance. NGINX tests use the included template after local identity/path/port substitutions. See [the validation report](../validation/REPORT.md), not merely the total pass count.
