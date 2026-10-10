# Apple and Android trust and application policy

**Read when:** a mobile app rejects a CA accepted by a desktop browser.

## Platform trust is not identical to application trust

On Apple platforms, trusted-root availability is OS/version-specific. A manually installed certificate profile may require additional trust activation; managed deployment can have different behavior. Follow the current platform instructions and the organization's device-management policy rather than assuming installation alone grants SSL trust.

Native applications can impose additional transport policy or custom trust handling. Record app build, OS release, profile-management path, requested hostname and certificate chain. A Safari success is useful evidence but not proof that another app's custom verifier accepts the same connection.

## Android Network Security Configuration

Android applications can define trust anchors, domain-specific rules, debug overrides and pinning through Network Security Configuration. User-added CA trust depends on app target/platform behavior and configuration; a user-installed root is not universally inherited by all modern apps.

Keep debug-only trust in debug configuration and verify that release builds exclude it. Scope private roots to the domains that require them when the platform supports that policy. Do not disable hostname checks or accept all certificates in custom code.

## Operational pitfalls

A device can have a correct root but lack a needed intermediate, use an outdated clock or encounter a different IPv6/CDN path. Inspect the chain on the actual mobile network. VPNs, captive portals and managed inspection can alter the observed endpoint and trust environment.

Client certificates require a private key and an appropriate selection/access mechanism. Device enrollment, app key access and TLS client-authentication support are distinct steps. Do not distribute one exportable client key to an entire fleet.

## Test matrix

Test supported OS versions and release/debug app builds separately. Include unknown-root rejection, name mismatch, expired leaf, removed management profile, root overlap/removal and key rotation. For pinned apps, prove both planned rollover and recovery from a lost key. Update dormant-device handling before adopting very short-lived credentials.

## Primary references

- **APPLE-ROOT** — [Apple trusted root certificate stores](https://support.apple.com/en-us/103272).
- **APPLE-PROFILE** — [Apple manually installed certificate profiles](https://support.apple.com/en-us/102390).
- **ANDROID** — [Android Network Security Configuration](https://developer.android.com/privacy-and-security/security-config).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
