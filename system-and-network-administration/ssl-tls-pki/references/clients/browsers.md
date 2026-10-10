# Browsers, public trust, interception and pinning

**Read when:** a browser rejects a site that command-line tools accept, or vice versa.

## Browser verification includes policy beyond a generic socket

A browser can enforce root-program distrust, CT policy, service-identity rules, revocation mechanisms and remembered HTTPS policy. A generic OpenSSL verification result does not reproduce that complete decision. Capture browser version, exact error code, URL and certificate chain before changing anything.

Browsers may also obtain intermediates or use cached material that a minimal runtime lacks. Reproduce in a clean profile or fresh supported device where permitted. Never treat a cached success as proof that the server sends a complete chain.

## Enterprise roots and interception

Firefox has documented enterprise mechanisms for using organization-managed roots. Behavior depends on platform, version and policy. Do not assume either “Firefox always ignores OS roots” or “all browsers share one store.” Check the effective enterprise policy and actual trust source.

A corporate TLS inspection proxy may present a different leaf issuer than the public site. Confirm whether interception is authorized and expected. Do not remove or install enterprise trust to bypass organizational controls without approval. For debugging, compare the expected network route and issuer fingerprints, not just the destination URL.

## HSTS and certificate errors

HSTS can prevent insecure fallback and constrain user bypass. It does not cause the underlying certificate failure; it changes what the browser permits after that failure. Diagnose trust, identity, validity or policy instead of advising a user to disable browser security.

## Pinning

Application pinning binds trust to specific keys/certificates or another constrained set. It can reduce reliance on broad CA trust but makes issuer/key rotation and recovery harder. Define backup pins, overlap, update channels and emergency removal before introducing it. Pinning is not a repair for a missing intermediate or incorrect name.

Do not recommend historical browser HPKP as a modern deployment pattern. For a controlled native application, use its platform's current pinning guidance and test rotation failures explicitly.

## Acceptance

Test current supported browsers, private/enterprise roots where relevant, a fresh trust environment, CT-sensitive public issuance and all frontend regions. Check the application response after TLS succeeds; the correct certificate does not prove the browser reached the intended tenant or origin behavior.

## Primary references

- **CHROME-ROOT** — [Chrome Root Program policy](https://googlechrome.github.io/chromerootprogram/crp/policy/).
- **CHROME-CT** — [Chrome Certificate Transparency policy](https://googlechrome.github.io/CertificateTransparency/ct_policy.html).
- **MOZILLA-ROOT** — [Mozilla Root Store Policy](https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/policy/).
- **FIREFOX** — [Firefox enterprise certificate authorities](https://support.mozilla.org/en-US/kb/setting-certificate-authorities-firefox).
- **RFC6797** — [HTTP Strict Transport Security](https://datatracker.ietf.org/doc/html/rfc6797).
- **ANDROID** — [Android Network Security Configuration](https://developer.android.com/privacy-and-security/security-config).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
