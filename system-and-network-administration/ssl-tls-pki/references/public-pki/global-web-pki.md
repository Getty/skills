# How the international public Web PKI works

**Read when:** explaining public trust, comparing CAs, or designing a trust boundary.

## There is no single international SSL root

Public trust is assembled by relying-party software and platform root programs. Browser/OS vendors decide which anchors and constraints to distribute. Different clients can therefore reach different acceptance decisions for the same certificate. A public CA participates through documented practices, audits, disclosure, technical controls and ongoing root-program requirements; a self-signed root is not enough.

The CA/Browser Forum publishes common industry requirements. It is not a global root CA and does not install trust anchors on devices. The IETF specifies protocols and certificate-processing mechanisms. DNS administration and routing provide naming/reachability infrastructure, not browser trust. National or sector-specific trust schemes may impose additional requirements for other certificate purposes.

## Participants and responsibility

| Participant | Responsibility | Does not guarantee |
|---|---|---|
| Root program | Inclusion, constraints, distrust and distribution policy | Every installed application uses its decisions |
| Root/subordinate CA | Issue within authorized scope and published practices | The subscriber's application is secure |
| Registration/validation function | Establish entitlement using approved methods | The subscriber is trustworthy in every sense |
| Subscriber | Protect keys, control names, deploy and replace certificates | Clients all have the same trust store |
| CT log/monitor | Make issuance observable and detect suspicious entries | Prevent all misissuance or revoke certificates |
| Relying application | Validate path, identity, purpose and applicable policy | Authorization merely from a successful handshake |

CCADB supports cross-program disclosure and coordination. Public incident reporting and audit material allow reviewers to inspect CA behavior; they do not remove the need for each root program to exercise its own policy.

## What happens for a website

A subscriber generates or securely obtains a leaf key, proves entitlement to requested names and receives a CA-signed certificate plus chain material. The website deploys them. A visiting client selects a reference name, negotiates TLS, validates a path to a locally trusted anchor and applies service-identity and other relevant checks. The client does not normally contact every CA in the chain on every connection.

DV checks name/address control under the applicable policy. OV and EV add specified identity checks; they do not select a stronger TLS record cipher merely because the certificate costs more. No validation level proves that the page is non-malicious.

## Architecture consequence

Publicly trusted certificates are useful when you cannot manage the clients' trust stores. Private PKI is appropriate where you control enrollment and relying parties. A publicly resolvable owned name may identify a private service, with DNS-based validation avoiding inbound exposure, but public issuance can disclose the name through CT. Internal-only names and reserved private addresses are not ordinary public Web PKI certificate subjects.

For a CA selection decision, record target-client trust, accepted purposes, automation, chain options, incident response, account controls, availability and migration costs—not just price and key length.

## Primary references

- **CABF-BR** — [CA/Browser Forum TLS Baseline Requirements — current HTML](https://cabforum.org/working-groups/server/baseline-requirements/requirements/).
- **CHROME-ROOT** — [Chrome Root Program policy](https://googlechrome.github.io/chromerootprogram/crp/policy/).
- **MOZILLA-ROOT** — [Mozilla Root Store Policy](https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/policy/).
- **APPLE-ROOT** — [Apple trusted root certificate stores](https://support.apple.com/en-us/103272).
- **MS-ROOT** — [Microsoft Trusted Root Program requirements](https://learn.microsoft.com/en-us/security/trusted-root/program-requirements).
- **CCADB** — [Common CA Database](https://www.ccadb.org/).
- **CHROME-CT** — [Chrome Certificate Transparency policy](https://googlechrome.github.io/CertificateTransparency/ct_policy.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
