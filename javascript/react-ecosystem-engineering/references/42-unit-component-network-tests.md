# Unit, component, and network-boundary tests

**Read when:** creating a test strategy, fixing regressions, or migrating implementation details.

## Match test scope to the claim

Use pure tests for parsers, reducers, graph rules, schema migrations, transformations, and command logic. Use React Testing Library for user-observable component behavior. Use MSW or an equivalent controlled network boundary for request outcomes where appropriate. Vitest is a test runner/toolchain choice; inspect its installed environment and configuration before assuming browser APIs exist.

Query by accessible role/name and assert meaningful output. Avoid coupling tests to private component state or arbitrary class names. Use realistic user interactions and await the resulting UI; do not add arbitrary sleeps to disguise a missing asynchronous condition. Keep fake timers scoped and restore them after each test.

## Fixture design

Include loading, empty, partial, malformed, failed, cancelled, and successful data. Make timezone/locale and clocks explicit. Isolate cache/store instances per test and reset network handlers. Verify that errors actually reach the intended boundary instead of being swallowed by a blanket mock. Treat console errors about missing keys, invalid hooks, or hydration as investigation signals.

For effects, test unmount, identity change, and obsolete completion. For optimistic changes, complete operations out of order. For forms, test keyboard submission and server errors. For graph logic, test invariants without requiring a DOM.

## Limitations

JSDOM does not prove real layout, pointer hit testing, browser rendering, native behavior, or accessibility with assistive technology. Geometry mocks can unblock a component harness but require corresponding browser tests. Coverage percentages indicate executed lines, not correctness. Keep a reproducible regression test for the original defect and document what remains outside the harness. This bundle's executed offline tests are listed separately from dependency-requiring example tests.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R69: React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [R70: Vitest](https://vitest.dev/guide/)
- [R72: MSW](https://mswjs.io/docs/)
- [R13: StrictMode](https://react.dev/reference/react/StrictMode)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
