# Chains, path building, roots and cross-signing

**Read when:** one client works while another reports an unknown issuer, or a CA hierarchy is changing.

## A transmitted list is not a validated path

A TLS server normally sends its leaf and the intermediate certificates needed to reach an anchor the client already trusts. Sending a root does not install that root in the client. Conversely, a server that omits an intermediate may accidentally work on a browser with a cached or fetched copy and fail in a fresh container.

`openssl s_client -showcerts` reports what the peer sent. It does not mean OpenSSL built or accepted that exact chain. Save the transmitted list separately from the path accepted by the target verifier.

## Treat the hierarchy as a graph

Cross-signing can create multiple certificates for the same subject/public key under different issuers. A self-signed root and a cross-certificate are different signed objects even when their keys match. Path builders may prefer different routes depending on local anchors, intermediate caches, algorithm policy and validity.

An issuer's display name is a hint, not cryptographic proof. Authority/subject key identifiers help locate candidates; actual validation checks the signature and all applicable constraints. Never choose a chain solely because its top certificate has a familiar Common Name.

## Reproducible path analysis

1. Export the exact leaf and transmitted intermediates; record SHA-256 certificate fingerprints and capture time.
2. Inventory the target client's anchors and any configured intermediate cache/AIA fetching. Do not assume the CLI and browser share them.
3. Verify the leaf with intermediates supplied as **untrusted chain-building material**, not as newly trusted roots.
4. Check the selected path's validity, CA constraints, purpose, algorithms and service identity. Then compare the live endpoint against that offline result.
5. Repeat with a clean trust environment representative of the failing client and with each supported alternate chain.

Example from the disposable lab:

```sh
openssl verify -x509_strict -purpose sslserver \
  -verify_hostname api.svc.test \
  -CAfile root.pem -untrusted intermediate.pem server.pem
```

The CA file is a deliberate trust input. Substituting the leaf or an arbitrary downloaded intermediate changes the question being tested.

## Rotation and old clients

Prefer a documented chain supported by your actual clients. Pinning an intermediate fingerprint for ordinary trust can convert routine CA rotation into an outage. Very old clients may have both a stale anchor set and an obsolete TLS implementation; an alternate chain only addresses the former.

Record whether the server's chain deployment changes automatically during renewal. Validate the returned chain rather than retaining a years-old hardcoded intermediate beside a newly issued leaf. Root expiration and distrust handling are verifier/policy-sensitive; test the intended path instead of assuming every root is processed exactly like a leaf.

## Primary references

- **RFC5280** — [X.509 certificates and CRLs / PKIX](https://www.rfc-editor.org/rfc/rfc5280.html).
- **OPENSSL-VERIFY** — [OpenSSL 3.5 verification options](https://docs.openssl.org/3.5/man1/openssl-verification-options/).
- **OPENSSL-SCLIENT** — [OpenSSL 3.5 s_client](https://docs.openssl.org/3.5/man1/openssl-s_client/).
- **LE-CHAINS** — [Let’s Encrypt roots and intermediates](https://letsencrypt.org/certificates/).
- **GO-X509** — [Go crypto/x509](https://pkg.go.dev/crypto/x509).
- **CURL-TRUST** — [curl TLS certificate verification](https://curl.se/docs/sslcerts.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
