# React Native, Expo, alternative renderers, and scope limits

**Read when:** a task mentions mobile/native rendering, custom renderers, or code sharing.

## Scope boundary

This skill is deep on React DOM and browser/Electron integration. React Native, Expo, React Native Web, Ink, and specialized renderers are catalog discovery routes, not complete native-platform engineering coverage. Retrieve their official version-specific documentation and use a dedicated skill for native builds, permissions, platform APIs, signing, stores, and device testing.

Do not assume DOM elements, CSS, events, refs, accessibility props, or browser libraries work unchanged in another renderer. Sharing React's programming model does not imply sharing its host environment. A package that imports `window`, the DOM, or a Node builtin needs an appropriate adapter or replacement.

## Sharing strategy

Share domain schemas, pure transformations, validation, API contracts, and state-machine logic where semantics match. Keep platform I/O, navigation, storage, permissions, and visual primitives behind explicit boundaries. Avoid forcing every platform into a lowest-common-denominator UI abstraction unless the maintenance tradeoff is justified by real reuse.

Record renderer/runtime versions independently. For React Three Fiber or other custom renderers, verify peer compatibility with React and the underlying host library. Do not upgrade React in isolation when a renderer's supported generation differs.

## Acceptance

Compile and execute on each claimed target, including real-device or supported emulator tests where required. Check accessibility, text input, gestures, lifecycle/background behavior, and resource cleanup per platform. A successful web build is not mobile compatibility evidence. Report the exact supported boundary and list native concerns intentionally delegated rather than presenting a broad catalog entry as a full implementation guide.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R01: React reference](https://react.dev/reference/react)
- [R65: React Three Fiber](https://r3f.docs.pmnd.rs/getting-started/introduction)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
