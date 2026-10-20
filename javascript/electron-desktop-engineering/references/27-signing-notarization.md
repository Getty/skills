# Signing, notarization, certificates, and release authority

**Read when:** shipping signed desktop artifacts or rotating release credentials.

## Identify the distribution contract

Specify OS, architecture, package format, release channel, installer/update mechanism, signing identity, certificate/provider, and relevant store/notarization requirements. These differ across macOS, Windows, Linux channels, and enterprise deployment. Verify current official platform/tooling requirements at implementation time; this skill does not assert static legal or certificate-policy details.

## Protect release authority

Store signing and publishing credentials in an authorized secret-management system with least privilege, audit, and rotation. Do not place private keys, passwords, token-bearing URLs, or service-account files in the repository or renderer bundle. Separate untrusted pull-request builds from credentialed signing/publishing workflows.

Build, rebuild native code, assemble resources, set fuses/integrity, sign nested and outer artifacts in the required sequence, then notarize/staple or perform channel-specific validation. Do not mutate signed contents afterward. Record artifact hashes, identity, tool versions, timestamps, and verification outputs.

## Recovery design

Plan certificate/key expiry, revocation, compromise, identity continuity for updates, and emergency release. Signing does not protect against malicious code deliberately signed by a compromised pipeline. Review source/dependency provenance and approval controls as part of the same authority chain.

## Acceptance

Verify signatures/notarization with the platform tooling and install on a clean target environment. Test offline first launch where relevant, update continuity, and native/helper code loading. Inspect entitlements/permissions for overbreadth. Treat a successful local signing command as one evidence item, not proof of reputation, all store requirements, or functioning updates. Never claim signing/notarization was executed when credentials and target runners were unavailable.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E19: Code signing](https://www.electronjs.org/docs/latest/tutorial/code-signing)
- [E41: Mac App Store guide](https://www.electronjs.org/docs/latest/tutorial/mac-app-store-submission-guide)
- [E40: Windows Store guide](https://www.electronjs.org/docs/latest/tutorial/windows-store-guide)
- [E35: ASAR integrity](https://www.electronjs.org/docs/latest/tutorial/asar-integrity)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
