# Managed devices, EAP-TLS and certificate-based access

**Read when:** TLS certificates are used for Wi-Fi, network admission, devices or VPNs.

## Establish the actual protocol and identities

EAP-TLS, an HTTPS VPN control channel, IPsec certificate authentication and WireGuard are not interchangeable. Identify the supplicant/client, authenticator/gateway, authentication server, enrollment system and authorization decision. Use the protocol-specific product documentation before producing router commands.

For EAP-TLS, validating the authentication server is essential; accepting any certificate signed by a broad root set can enable an unintended authentication endpoint. Define expected server identities and trust explicitly, then map device/user client credentials to network-access policy.

## Managed-device enrollment

Determine whether the identity belongs to a person, machine, application or hardware-bound key. Bind issuance to managed enrollment or attestation, constrain permitted identities and separate device offboarding from certificate expiration. Device cloning, shared bootstrap passwords and exportable fleet-wide keys undermine individual revocation.

EST is one standards-based enrollment option. Actual ecosystems may require other enrollment and management protocols. Avoid claiming that a generic CA with a CSR endpoint meets a vendor's device-provisioning requirements.

## Client constraints

Inventory supported key algorithms, certificate sizes, chain depth, EKUs, SAN parsing, clock source and trust-update mechanism. A device without dependable time can fail validity checks after reboot; solve the bootstrap/time problem rather than issuing effectively eternal certificates.

Hardware-backed keys can reduce extraction risk, but assess backup/replacement and firmware support. Device firmware can have a trust store unrelated to the operating system used to manage it.

## Lifecycle tests

Test first enrollment, certificate renewal while connected, loss of network access during renewal, user/device removal, expired client certificates and server-root replacement. Ensure a quarantined or expired device has a controlled recovery path that does not grant unrestricted network access.

For VPNs, separately analyze control-channel authentication and data-plane protection. A TLS-valid connection to a gateway does not establish correct routing policy, tenant isolation or access authorization. Keep those decisions in the relevant VPN/network skill.

## Primary references

- **RFC9190** — [EAP-TLS 1.3](https://datatracker.ietf.org/doc/html/rfc9190).
- **RFC7030** — [Enrollment over Secure Transport](https://datatracker.ietf.org/doc/html/rfc7030).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).
- **RFC5280** — [X.509 certificates and CRLs / PKIX](https://www.rfc-editor.org/rfc/rfc5280.html).
- **ANDROID** — [Android Network Security Configuration](https://developer.android.com/privacy-and-security/security-config).
- **SCHANNEL** — [TLS cipher suites in Windows 11 / Schannel](https://learn.microsoft.com/en-us/windows/win32/secauthn/tls-cipher-suites-in-windows-11).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
