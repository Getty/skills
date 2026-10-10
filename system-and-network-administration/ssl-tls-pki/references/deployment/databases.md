# Database TLS: PostgreSQL and transferable checks

**Read when:** securing database links or diagnosing libpq certificate failures.

## PostgreSQL: encryption is not verification

For libpq, use `sslmode=verify-full` with an approved trust source to require authenticated server identity. `prefer` permits weaker behavior, and `require` is not an explicit hostname-verification policy. A root file can change legacy `require` behavior toward CA verification, but relying on that implicit interaction is not a substitute for `verify-full`.

```sh
psql 'host=db.internal.example.com hostaddr=10.20.0.20 port=5432 dbname=app user=app sslmode=verify-full sslrootcert=/etc/app/pki/database-roots.pem'
```

`hostaddr` fixes the network destination while `host` supplies the intended name for verification. Keep passwords out of command arguments and use the application's supported secret mechanism.

## Server configuration and admission

`ssl=on` enables TLS but does not by itself disallow plaintext connections. Review ordered `pg_hba.conf` rules, including `hostssl`/`hostnossl` behavior and broader rules that could still admit unwanted traffic. Prove rejection of plaintext with a negative test.

The server certificate file can include intermediates. `ssl_ca_file` establishes trust for client certificates; it is not a substitute for the chain the server presents. Client-certificate verification, certificate-to-database-user mapping and database grants are separate controls.

## Identity compatibility

PostgreSQL 18 documents legacy CN fallback and IP/name handling differences from modern service-identity recommendations. Issue proper DNS/IP SANs anyway and test with the deployed libpq version. Do not infer database behavior solely from curl or a browser.

Client private keys have strict ownership/permission expectations. Credential replacement also needs the server's reload behavior: a failed TLS configuration reload can leave an earlier valid configuration active. Check logs and the served fingerprint.

## Beyond PostgreSQL

For MySQL, Redis, LDAP-backed applications, connection pools and vendor drivers, ask the same questions without copying PostgreSQL flags: does the mode require encryption, verify the issuer, verify the expected name, send a client certificate and prohibit fallback? Does the pool create fresh connections after trust/credential rotation?

These are a transferable checklist, not verified configuration recipes for every product. Load the product's current TLS/driver documentation before generating exact switches.

## Acceptance tests

Use the real application driver against an approved server, then repeat with an untrusted CA, wrong name, missing intermediate and plaintext-only endpoint. Test account authorization after successful mTLS. Verify failover replicas and backup/replication clients separately.

## Primary references

- **PG-CLIENT** — [PostgreSQL 18 libpq TLS](https://www.postgresql.org/docs/18/libpq-ssl.html).
- **PG-SERVER** — [PostgreSQL 18 server TLS](https://www.postgresql.org/docs/18/ssl-tcp.html).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).
- **OPENSSL-SCLIENT** — [OpenSSL 3.5 s_client](https://docs.openssl.org/3.5/man1/openssl-s_client/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
