# Linux/Unix trust stores and crypto backends

**Read when:** a Linux service or container cannot validate a private or public CA.

## Identify the trust source

Debian-family systems commonly manage a PEM bundle and hashed certificate directory through `update-ca-certificates`; RHEL-family systems use a shared trust mechanism with different source paths and tooling. Follow the distribution's documented mechanism instead of editing a generated bundle directly.

A statically linked tool, language package, custom OpenSSL build or container may ignore the host store. Inspect `curl -V`, `openssl version -a`, package/build metadata and explicit CA environment variables. The executable's OpenSSL version can differ from the library loaded by Python or another process.

## Scoped diagnosis

Use an explicit, approved CA bundle to test the trust hypothesis without modifying global policy. Confirm the service's actual user, filesystem namespace, chroot/container, file readability and working directory. Relative paths that work in an interactive shell may fail under a service manager.

Check whether the process reads trust at startup or per connection. Restart/reload only through the service's documented procedure and verify a new connection afterward. Do not assume a trust-file replacement updates a long-lived in-memory pool.

## OpenSSL provider and policy issues

OpenSSL configuration, loaded providers, security levels and distribution crypto policy can affect certificates and negotiation independently of root trust. A weak-key or unsupported-algorithm error is not repaired by adding the issuer to a CA file.

Treat legacy-provider use for a one-time import separately from the service's ongoing TLS policy. Never set a system-wide low security level as a generic compatibility fix. Identify the failing key/signature or protocol first and replace it where possible.

## Trust deployment

Use an approved configuration-management change with fingerprint verification and a removal plan. Test both the newly trusted intended endpoint and an unrelated untrusted endpoint. In containers, update the image or application bundle reproducibly; do not rely on a manual change made inside one running container.

## Primary references

- **DEBIAN-CA** — [Debian update-ca-certificates manual](https://manpages.debian.org/bookworm/ca-certificates/update-ca-certificates.8.en.html).
- **RHEL-CA** — [RHEL 9 shared system certificate storage](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/securing_networks/using-shared-system-certificates_securing-networks).
- **CURL-TRUST** — [curl TLS certificate verification](https://curl.se/docs/sslcerts.html).
- **OPENSSL-MIGRATION** — [OpenSSL 3.5 migration guide](https://docs.openssl.org/3.5/man7/ossl-guide-migration/).
- **DOCKER-CA** — [Docker host and container CA certificates](https://docs.docker.com/engine/network/ca-certs/).
- **PY-SSL** — [Python ssl library](https://docs.python.org/3/library/ssl.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
