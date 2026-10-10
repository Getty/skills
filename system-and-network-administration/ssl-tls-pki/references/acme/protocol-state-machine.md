# ACME: account, order, authorization, challenge, certificate

**Read when:** implementing certificate automation or explaining how Let’s Encrypt proves control.

## Roles and key separation

The ACME client is the operator's automation. The ACME server belongs to a CA. The ordinary flow keeps the certificate private key at the client or its chosen key custodian; the client submits a CSR, not the private key. The ACME account has a separate key used to authenticate management requests.

A useful conceptual state machine is:

```text
Discover directory → establish/reuse account → request order
  → satisfy required authorizations → order ready
  → finalize with CSR → issuance processing → certificate available
  → validate returned material → deploy → verify live endpoints
```

The last three deployment checks are operator responsibilities, not a guarantee provided by the ACME protocol.

## Protocol objects

| Object | Meaning | Diagnostic question |
|---|---|---|
| Directory | Endpoint discovery and advertised capabilities | Correct CA and production/staging environment? |
| Account | Authenticated management identity | Correct account URL, key and terms status? |
| Order | Requested identifiers and issuance state | Exact SAN set and supported identifier types? |
| Authorization | Permission associated with an identifier | Pending, valid, expired or invalid? |
| Challenge | Concrete proof method | Is the CA seeing the required response? |
| Finalization/CSR | Public key and requested certificate data | Does it match the authorized identifier set? |
| Certificate resource | Issued leaf and chain | Correct key, profile, names, lifetime and chain? |

Requests use signed structures and replay protection. Nonces, account-key rollover and authenticated resource retrieval are protocol concerns; do not build a production client from a few ad-hoc `curl` calls. Use a maintained ACME library/client and expose its structured errors.

## Security consequences

Control of a DNS API token, challenge-serving path or account key grants different powers. Inventory each separately. External Account Binding connects a new ACME account to an external registration system when the CA requires it; it does not replace domain validation universally.

Reusing a valid authorization is a CA-policy decision with a bounded lifetime. A new certificate may sometimes be issued without a freshly visible challenge, so “I did not see a TXT change” is not proof of an issuance error. Conversely, persistent account storage does not guarantee that authorizations remain reusable.

## Recovery-friendly implementation

Persist account keys and order state with appropriate permissions. Distinguish terminal invalid states from retryable processing. Respect server retry guidance and deadlines. Do not create a new account every time a container starts. Maintain one clearly owned renewal/deployment path for a credential set, or implement safe distributed coordination.

Use staging or a dedicated test CA for failure experiments. The included local PKI lab tests certificate acceptance, not this ACME state machine. Pebble is a separate useful integration-test option; its deliberately simplified behavior is not production CA behavior.

## Primary references

- **RFC8555** — [Automated Certificate Management Environment](https://www.rfc-editor.org/rfc/rfc8555.html).
- **RFC9773** — [ACME Renewal Information](https://www.rfc-editor.org/rfc/rfc9773.html).
- **CERTBOT** — [Certbot user guide](https://eff-certbot.readthedocs.io/en/stable/using.html).
- **CM-ACME** — [cert-manager ACME issuers](https://cert-manager.io/docs/configuration/acme/).
- **LE-STAGING** — [Let’s Encrypt staging environment](https://letsencrypt.org/docs/staging-environment/).
- **LE-PEBBLE** — [Pebble as an ACME development test server](https://letsencrypt.org/2025/04/30/pebbleacmeimplementation).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
