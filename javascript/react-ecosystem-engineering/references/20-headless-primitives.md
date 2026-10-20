# Headless UI: Radix, Base UI, React Aria, and composition

**Read when:** implementing dialogs, menus, popovers, comboboxes, or custom design-system behavior.

## Choose a coherent primitive layer

Radix Primitives, Base UI, and React Aria offer different composition and behavior models. Evaluate them with one difficult representative widget, not a button screenshot. Inspect controlled/uncontrolled conventions, portal behavior, focus management, collection APIs, styling hooks, ref handling, SSR support, and interoperability with the current React version. Headless UI and Downshift are catalog alternatives requiring their own installed-version review.

Prefer one primitive family for related overlays and selection widgets unless a documented gap justifies mixing. Two focus scopes, outside-click systems, or scroll locks can interfere even when each library works independently. Radix documentation currently supports coordinated individual packages and an umbrella package; follow the project's established installation model rather than installing both indiscriminately.

## Integration procedure

Specify trigger semantics, accessible name, focus destination on open, focus restoration on close, Escape behavior, dismissal on outside interaction, and nested overlay behavior. Preserve required prop/ref forwarding when wrapping or composing elements. Do not render nested interactive controls through an `asChild` or slot mechanism without checking the resulting DOM.

A combobox is not merely a styled select. Define text input, selected value, active option, filtering, asynchronous loading, and announcement behavior separately. A modal must prevent unintended interaction behind it while preserving a useful reading order.

## Acceptance

Test keyboard-only operation, screen-reader announcements, touch, text selection, nested popovers, scrolling, and focus restoration after the trigger unmounts. Verify the same behavior through your wrapper component, not only the vendor demo. Document any behavior deliberately overridden; changes to primitive defaults should have tests demonstrating that accessibility and interaction contracts remain intact.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R31: Radix Primitives overview](https://www.radix-ui.com/primitives/docs/overview/introduction)
- [R33: React Aria getting started](https://react-aria.adobe.com/getting-started)
- [R34: Base UI quick start](https://base-ui.com/react/overview/quick-start)
- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
