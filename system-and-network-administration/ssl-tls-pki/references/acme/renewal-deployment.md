# Renewal is an end-to-end deployment transaction

**Read when:** automating certificates or diagnosing “renewed successfully, still expired”.

## The transaction has several independent states

```text
eligible → authorized → issued → checked → published → reloaded
         → externally observed → old generation retired
```

Monitor these separately. A renewed file does not prove the process loaded it. A Kubernetes Secret update does not prove every pod reloaded it. A successful reload does not prove that the load balancer routes to the updated replicas.

## Scheduling

Prefer ACME Renewal Information (ARI) where the client and CA support it. ARI communicates a suggested renewal window and allows replacement to be coordinated with the CA. It is not a deployment health check. Without ARI, use lifetime-aware scheduling with jitter and enough recovery margin; a fixed day-60 schedule fails when lifetimes shrink.

Persist account and renewal state. Use stable storage and a single owner or well-defined locking/leader mechanism. Recreating state can consume issuance limits and destroy the evidence needed to diagnose an outage.

## Candidate validation and activation

Before activation, check key correspondence, intended names, purpose, validity and expected trust path. Make certificate, private key and chain a coherent generation. Publish atomically using the application's supported mechanism. Avoid exposing a new certificate beside an old mismatched key.

Validate configuration, trigger the documented reload, then probe each endpoint with its real reference identity and representative clients. Compare the live leaf fingerprint to the candidate, and record convergence. Long-lived connections can continue with earlier session state; decide whether to drain them.

## Certbot-specific boundaries

`certonly` obtains credentials without being a universal server installer. Deploy hooks are intended for successful certificate deployment events; pre/post hooks have different semantics. A renewal dry run normally uses staging and does not automatically execute deploy hooks unless requested. Running a dry run can still have side effects such as temporary web-server changes and pre/post hooks.

Therefore test the hook independently in a safe environment, then exercise the real renewal path. Document credential permissions, service identity, PATH, working directory, container mounts and failure exit codes. A hook that logs an error but returns success can conceal an outage.

## Recovery budget

Define the maximum tolerated CA outage, DNS outage, deployment outage and human-response delay. Their combined recovery path must fit comfortably inside the remaining validity window. Keep alerts relative to actual lifetime and operational margin, not a universal “expires in 30 days” threshold.

Rollback may restore a known-good unexpired generation for a deployment defect. It must not restore a compromised key or reverse an intentional revocation. Escalate failure to renew before expiration rather than silently switching to a self-signed certificate.

## Primary references

- **RFC9773** — [ACME Renewal Information](https://www.rfc-editor.org/rfc/rfc9773.html).
- **CERTBOT** — [Certbot user guide](https://eff-certbot.readthedocs.io/en/stable/using.html).
- **LE-64D** — [64-day certificates: announcement on 2026-10-07](https://letsencrypt.org/2026/10/07/64-day-certs).
- **LE-45D** — [Let’s Encrypt planned 45-day default lifetimes](https://letsencrypt.org/2025/12/02/from-90-to-45).
- **LE-LIMITS** — [Let’s Encrypt rate limits](https://letsencrypt.org/docs/rate-limits/).
- **CM-CERT** — [cert-manager Certificate resources and renewal](https://cert-manager.io/docs/usage/certificate/).
- **NGINX-SSL** — [NGINX HTTP SSL module](https://nginx.org/en/docs/http/ngx_http_ssl_module.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
