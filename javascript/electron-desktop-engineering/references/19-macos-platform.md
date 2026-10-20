# macOS, signing, notarization, and application behavior

**Read when:** targeting macOS, shipping universal builds, or requesting OS capabilities.

## Separate distribution models

Conventional notarized distribution and Mac App Store distribution have different requirements. The macOS App Sandbox is not the same mechanism as Chromium renderer sandboxing. Verify current signing, entitlements, hardened-runtime, notarization, and store requirements for the selected channel instead of combining fragments from incompatible guides.

## Build and lifecycle

Record supported macOS versions, Intel/Apple Silicon targets, and universal-build policy. Native modules and helper executables must support the architecture actually launched; combining application bundles does not magically create universal native dependencies. Inspect/sign nested code in the correct build sequence and avoid modifying signed contents afterward.

Follow expected activation and window behavior: closing the last window and quitting the application are distinct. Handle early open-file/open-url events and reopen/activate behavior. Preserve native keyboard/menu conventions where possible. Test titlebar customization, full-screen behavior, display scaling, and multiple Spaces where relevant.

## Privacy and storage

Camera, microphone, screen capture, automation, and file access may involve OS privacy prompts/entitlements beyond Electron permission handlers. Request only needed access, explain the purpose, and handle denial/revocation. Do not assume a development binary's granted permission applies identically to a newly signed installed build. Validate secure storage behavior when the keychain is unavailable or locked.

## Acceptance

Test on clean target machines/accounts with the final signed/notarized artifact, including first launch, offline launch, permission denial, update, and uninstall. Verify stapling/notarization outcomes with the selected tooling and retain records. Exercise Intel/Apple Silicon native features as claimed. Document any store-specific limitations and do not weaken production entitlements merely to make a development automation tool work.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E19: Code signing](https://www.electronjs.org/docs/latest/tutorial/code-signing)
- [E28: App API](https://www.electronjs.org/docs/latest/api/app)
- [E33: Desktop capture](https://www.electronjs.org/docs/latest/api/desktop-capturer)
- [E41: Mac App Store guide](https://www.electronjs.org/docs/latest/tutorial/mac-app-store-submission-guide)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
