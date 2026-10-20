# Component contracts and accessibility acceptance

**Read when:** creating reusable UI or reviewing interactive components.

## Specify behavior before markup

Every interactive component needs a role, accessible name, state announcement, keyboard contract, focus strategy, disabled/read-only behavior, and error/loading semantics. Start with native elements. Introduce ARIA to express a real pattern when native semantics are insufficient, not to decorate arbitrary clickable divs.

For a button, cover pending versus disabled, duplicate action prevention, icon labeling, and destructive confirmation. For an input, cover labels, descriptions, invalid state, input method composition, autocomplete, and preserving drafts. For a dialog, cover initial focus, tab containment, Escape, background interaction, and restoration. For tabs, distinguish navigation links from a tab interface and select an intentional activation model.

## Review matrix

Test mouse, touch, keyboard, screen reader, zoom, reduced motion, forced colors, long content, localization, and empty/error states as applicable. Automated tools catch a subset of issues; manual interaction and assistive-technology checks remain separate evidence. A passing component test does not establish whole-page reading order or contrast.

For asynchronous controls, announce meaningful state transitions without announcing every keystroke or rapidly changing graph coordinate. Keep focus on a stable element when a background update replaces content. Provide non-drag alternatives for operations that otherwise depend on pointer precision.

## Reusable acceptance record

Record component purpose, supported variants, controlled/uncontrolled ownership, public props/events, accessibility behavior, styling hooks, tested environments, and known limitations. Add stories for failure and loading states rather than only ideal content. Verify the composed product view: an accessible primitive can become inaccessible through missing labels, duplicate IDs, misplaced portals, or nested interactive elements. Prefer tests that exercise visible roles and names over private class names and implementation structure.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)
- [R33: React Aria getting started](https://react-aria.adobe.com/getting-started)
- [R69: React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [R73: Storybook](https://storybook.js.org/docs)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
