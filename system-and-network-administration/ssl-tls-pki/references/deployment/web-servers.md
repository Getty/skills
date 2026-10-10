# Web servers, certificate loading and HTTPS policy

**Read when:** deploying TLS on NGINX, Apache or Caddy.

## Common deployment contract

Load a matched private key and leaf-plus-intermediate chain. Restrict key access, use supported protocol settings and validate configuration before reload. After activation, check live names, chain, protocol and fingerprint from outside the service. Test default-vhost and unknown-SNI behavior so that one tenant's certificate is not mistaken for another's.

NGINX, Apache and Caddy have different loading and automation models. Do not transpose directive names or assume every package includes optional ACME capabilities. Consult the version actually installed.

## NGINX

Use `ssl_certificate` for the server chain and `ssl_certificate_key` for its key. Client-CA trust and upstream trust have other directives and purposes. Explicitly configure upstream verification when proxying HTTPS. The included [NGINX example](../../examples/nginx-verified-upstream.conf) is a template for both boundaries, not an automatic installer.

A syntax test can detect unreadable files, mismatched keys and invalid directives. It does not prove endpoint reachability or the correct certificate on every worker/replica.

## Apache

Follow current mod_ssl guidance for leaf/chain configuration and name-based virtual hosting. Distinguish `SSLVerifyClient` from server certificate settings and `SSLProxy*` controls for outgoing TLS. Legacy examples may split chain files differently; use the documented behavior for the selected 2.4 release.

## Caddy

Automatic HTTPS can combine issuance, renewal and serving, but still depends on reachable challenges, persistent state, correct names and supported issuer policy. Private/internal issuance changes trust requirements for clients. Validate behavior in containers and HA deployments rather than treating automatic as stateless.

## HTTP policy around TLS

HSTS tells supporting browsers to require HTTPS for a hostname according to its policy. It does not install a CA, repair an invalid certificate or encrypt the first unprotected visit by itself. `includeSubDomains` and preload decisions affect more than the current vhost and need ownership and rollback planning.

Do not enable long-lived HSTS across unrelated or not-yet-HTTPS subdomains without inventory. Keep ACME HTTP challenge handling functional under the CA's redirect rules. Cookies, authentication, CSP, application vulnerabilities and origin authorization still require their own security work.

## Deployment acceptance

Test valid and wrong hostnames, complete and incomplete chains, reload failure, file permissions, unknown SNI, upstream impersonation and certificate replacement under active traffic. Record which properties are enforced by the server and which are left to clients.

## Primary references

- **NGINX-SSL** — [NGINX HTTP SSL module](https://nginx.org/en/docs/http/ngx_http_ssl_module.html).
- **NGINX-PROXY** — [NGINX HTTP proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).
- **APACHE** — [Apache HTTP Server mod_ssl](https://httpd.apache.org/docs/2.4/mod/mod_ssl.html).
- **CADDY** — [Caddy automatic HTTPS](https://caddyserver.com/docs/automatic-https).
- **RFC6797** — [HTTP Strict Transport Security](https://datatracker.ietf.org/doc/html/rfc6797).
- **LE-CHALLENGES** — [Let’s Encrypt challenge types](https://letsencrypt.org/docs/challenge-types/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
