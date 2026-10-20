# Constrained Electron shell

Original demonstration of an isolated, sandboxed renderer; self-contained preload; three fixed IPC operations; sender/frame/page validation; runtime payload validation; a token bucket/in-flight limit; deny-by-default permissions/navigation/new windows/downloads; fixed custom-protocol assets; and a restrictive CSP. This is a small reviewed example, **not a production security certification**.

## Offline tests

From the skill root:

```sh
node --test tests/policy.test.cjs
```

These execute pure policies with mocks. They do not launch Electron or verify Chromium/OS enforcement.

## Install in a networked environment

No Electron version is fabricated or embedded as “latest.” First inspect the current official support timeline, release notes, advisories, and native/OS constraints. After reviewing the version selected by npm, install an exact supported patched release and inspect lifecycle scripts. Electron installation downloads runtime binaries.

```sh
cd examples/secure-shell
npm view electron dist-tags --json
npm install --save-dev --save-exact electron
npm start
```

Commit the generated lockfile after review. The manifest intentionally omits an unverified runtime dependency. Registry access was unavailable during authoring, so installation, Electron launch, packaging, signing, and update testing were not executed.

For the provided integration specification, also review/install `@playwright/test` and the matching `playwright` as exact dev dependencies, then run `npm run test:desktop` on an appropriate non-root desktop/CI environment. Do not disable sandboxing to work around launch failures. The specification covers a small smoke scenario, not the full threat-model test matrix.

## Deliberate limits

Preferences are in memory. There is no database, durable write protocol, user authentication, single-instance enforcement, multi-window synchronization, updater, signing/packager configuration, production fuse application, or plugin execution. Those concerns have dedicated references and templates. The fixed asset allowlist is not a general filesystem server. Do not replace it with unvalidated path concatenation. The CSP allows no remote connection; React Flow integration would require a deliberate style policy and new renderer bundle, not relaxed script/Node security.

The authorization helper's mocked frame identity must be verified against actual WebContents/WebFrameMain behavior in the chosen Electron release. Test real subframe/other-window/navigation denial before release. The app can be launched from the source directory after installation, but a production release requires the packaged, signed, installed, and update-stage checks in the skill.
