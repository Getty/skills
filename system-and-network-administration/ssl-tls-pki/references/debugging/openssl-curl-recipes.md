# OpenSSL and curl: safe diagnostic recipes

**Read when:** running concrete checks without weakening verification.

## Prerequisites

Commands below target a modern OpenSSL CLI and curl; inspect installed help and backend versions. `approved-roots.pem` is an authenticated trust input, not a certificate collected from an untrusted server. Use timeouts in automation and preserve both exit status and stderr.

### Live DNS identity with explicit trust

```sh
openssl s_client -connect 127.0.0.1:8443 \
  -servername api.svc.test -verify_hostname api.svc.test \
  -verify_return_error -CAfile approved-roots.pem -showcerts </dev/null
```

`-servername` selects SNI. `-verify_hostname` checks the reference identity. `-verify_return_error` makes verification errors fatal. `-showcerts` displays the transmitted list, **not a validated path**. For an IP identity, use `-verify_ip` and do not invent a DNS SNI containing an IP literal.

Without the fatal-verification option, s_client can continue despite certificate errors. A negotiated cipher is therefore not proof of successful authentication.

### Offline path and purpose

```sh
openssl verify -x509_strict -purpose sslserver \
  -verify_hostname api.svc.test \
  -CAfile root.pem -untrusted intermediate.pem server.pem

openssl verify -purpose sslclient \
  -CAfile root.pem -untrusted intermediate.pem client.pem
```

The second command verifies client-certificate purpose, not application authorization. For leaf CRL enforcement, add `-CRLfile intermediate.crl.pem -crl_check`; full-path revocation requires the appropriate complete issuer data and policy.

### Pin the destination, not the identity

```sh
curl --fail --show-error --silent --connect-timeout 5 --max-time 10 \
  --cacert approved-roots.pem \
  --resolve api.svc.test:8443:127.0.0.1 \
  https://api.svc.test:8443/
```

This retains the URL identity, SNI and HTTP Host while changing address resolution. Replacing the URL with an IP and merely setting `Host:` is not equivalent. To deliberately bypass a proxy for an authorized direct probe, add a scoped `--noproxy` value; record that routing change.

### Isolate versions

Use `s_client -tls1_2` or `-tls1_3`. In curl, `--tlsv1.2` sets a minimum; add `--tls-max 1.2` to constrain both ends for a TLS 1.2-only experiment. Do not persist the test restriction accidentally.

### Read dates without overclaiming

```sh
openssl x509 -in server.pem -noout -dates -fingerprint -sha256
openssl x509 -in server.pem -checkend 86400 -noout
```

`-checkend` is an expiry-window check, not path/name/purpose verification. Avoid pipelines that hide s_client failure behind a successful final command; in Bash enable `pipefail` or capture status explicitly.

## Primary references

- **OPENSSL-SCLIENT** — [OpenSSL 3.5 s_client](https://docs.openssl.org/3.5/man1/openssl-s_client/).
- **OPENSSL-VERIFY** — [OpenSSL 3.5 verification options](https://docs.openssl.org/3.5/man1/openssl-verification-options/).
- **OPENSSL-X509** — [OpenSSL 3.5 x509](https://docs.openssl.org/3.5/man1/openssl-x509/).
- **CURL-MAN** — [curl command-line manual](https://curl.se/docs/manpage.html).
- **CURL-TRUST** — [curl TLS certificate verification](https://curl.se/docs/sslcerts.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
