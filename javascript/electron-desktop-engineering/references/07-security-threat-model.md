# Desktop threat model and defense-in-depth baseline

**Read when:** reviewing architecture, loading external content, or shipping a release.

## Start from compromise assumptions

Assume renderer content may be compromised by XSS, dependency code, imported documents, or an unsafe embed. List assets: local files, credentials, personal data, database contents, process execution, device permissions, and update authority. Draw trust boundaries among renderer, preload, main, utility/worker processes, OS services, remote APIs, and update infrastructure.

Baseline: supported patched Electron, isolated/sandboxed renderer, no Node integration, web security retained, narrow validated bridge, restrictive navigation/permissions, and explicit CSP. These controls reinforce one another; none makes all application code trustworthy. Do not solve a compatibility problem by disabling several controls together.

## Review dangerous shortcuts

Reject `webSecurity: false`, certificate-error bypasses, broad shell/process APIs, unrestricted `openExternal`, arbitrary file paths, wildcard update/remote origins, and universal permission grants. Keep development server allowances conditional and absent from production policy. Inspect preload dependencies and install/build scripts as supply-chain inputs.

Signed applications and ASAR packaging do not remove the need for runtime authorization. Electron fuses can reduce attack surface but must be chosen/tested with packaging and tooling. A utility process running Node is not a safe destination for hostile user code; arbitrary-code execution needs an additional isolation design.

## Acceptance artifact

Deliver a threat table with attacker capability, entry point, affected asset, control, negative test, residual risk, and owner. Include renderer compromise tests against every bridge capability. Review what happens after update compromise, local filesystem tampering, stolen session data, and a malicious imported project. Record unsupported targets or untested controls rather than labeling a configuration “secure” solely because it matches a checklist.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E01: Electron security checklist](https://www.electronjs.org/docs/latest/tutorial/security)
- [E05: Context isolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation)
- [E06: Process sandboxing](https://www.electronjs.org/docs/latest/tutorial/sandbox)
- [E12: Fuses](https://www.electronjs.org/docs/latest/tutorial/fuses)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
