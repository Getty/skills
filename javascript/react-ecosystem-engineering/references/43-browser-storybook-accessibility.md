# Browser tests, Storybook, visual checks, and accessibility

**Read when:** validating complete interactions, reviewing components, or setting a release gate.

## Browser coverage

Use Playwright or the repository's established browser runner against a production-like build. Cover direct route load, navigation, authentication renewal, form submission, errors, and one critical product workflow. Prefer stable roles/test contracts, controlled test data, and observable completion conditions. Capture traces on failure and retain enough environment detail to reproduce.

For React Flow, test real node dimensions, drag/connect/reconnect, viewport conversion, keyboard alternatives, and save/load. For overlays, test focus order and restoration. For SSR, inspect hydration and console errors on a fresh navigation. Test responsive layouts and keyboard use, not only one desktop screenshot.

## Storybook role

Use stories as reproducible component states: empty, loading, error, disabled, long content, localization, and edge cases. Keep loaders/mocks deterministic. Interaction tests can validate the component contract, while visual diffs detect unintended appearance changes. Neither proves backend authorization or full production deployment behavior.

## Accessibility evidence

Automated rules, keyboard review, contrast review, zoom/reflow, reduced motion, and screen-reader testing are separate checks. Record actual platforms and assistive technologies used. Do not label an application “accessible” based solely on a zero-violation automated scan. Inspect composed screens because portals, headings, focus, and labels interact across component boundaries.

## Release discipline

Keep flaky tests visible; quarantine with an owner, explanation, and expiry rather than deleting them silently. Do not loosen assertions to make a failing interaction pass. Use stable test fixtures and predictable clocks before increasing retries. Archive browser version, build revision, dataset, and relevant trace for performance/visual comparisons. Test deployment paths and headers as shipped, including old tabs surviving a new release.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R71: Playwright](https://playwright.dev/docs/intro)
- [R73: Storybook](https://storybook.js.org/docs)
- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
