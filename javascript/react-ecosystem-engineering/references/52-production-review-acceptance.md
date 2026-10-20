# Production review and acceptance gates

**Read when:** finishing a feature, reviewing a pull request, or preparing release.

## Required evidence

Provide the user-visible behavior implemented, changed files, architectural decisions, relevant dependency versions, commands executed, results, and known limitations. Keep observed facts separate from inference. Include the smallest reproduction for any unresolved defect. Use the supplied review and validation templates rather than a generic “all good.”

## Review dimensions

Correctness: one source of truth, validated external input, stable identity, no stale overwrite, and explicit conflict/error behavior. Accessibility: semantic controls, keyboard/focus, labels, loading/error announcements, and appropriate manual checks. Performance: realistic dataset, meaningful budgets, bounded resource lifetimes, and no unexplained broad subscriptions.

Security: backend authorization, client/server boundaries, content sanitization where necessary, credential redaction, current advisories, and no privileged renderer shortcuts. Operations: reproducible build, deployment base paths, cache/update behavior, migrations, logging, and rollback. Dependencies: justified selection, compatible generations, licenses, and removal/upgrade ownership.

## Minimum release scenarios

Exercise a cold start, direct deep link, slow dependency, malformed response, cancelled operation, expired session, denied authorization, duplicate action, and reload with persisted data. Add domain-specific scenarios: graph import/cycles/reconnect/history, form arrays/server errors, grid conflicts/export, or editor paste/collaboration.

Do not conflate an automated checklist with a complete assurance case. Document browser/OS coverage actually executed and all skipped runtime tests. A passing suite can still miss a production configuration failure; test the built/deployed artifact. Preserve a rollback path and a clear owner for known limitations rather than burying them in generated documentation.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)
- [R69: React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [R71: Playwright](https://playwright.dev/docs/intro)
- [R74: Vite](https://vite.dev/guide/)
- [E01: Electron security checklist](https://www.electronjs.org/docs/latest/tutorial/security)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
