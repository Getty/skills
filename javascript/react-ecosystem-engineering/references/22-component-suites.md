# Component suites: MUI, Mantine, Chakra, Ant Design, and alternatives

**Read when:** selecting or maintaining a broad UI component system.

## Evaluation matrix

Compare the actual required controls, table/calendar/editor needs, theming, accessibility behavior, SSR integration, bundle/loading characteristics, localization, support policy, and licenses. MUI, Mantine, Chakra UI, and Ant Design have distinct API generations and design assumptions; confirm the installed major before generating providers, theme tokens, slot overrides, or form integrations. Fluent UI, PrimeReact, HeroUI, and React Bootstrap are catalog alternatives, not automatically equivalent drop-ins.

Build a representative settings form, nested dialog, asynchronous combobox, and dense data view. Include an error state, long translations, and keyboard operation. This exposes integration cost more reliably than counting available components. Distinguish community components from separately licensed advanced grids/charts or templates; never imply that an entire vendor ecosystem shares one license.

## Integration rules

Use application-owned adapters only where they standardize a real product contract. Avoid wrapping every prop of a large component into another equally large API. Centralize tokens and repeated defaults. Preserve escape hatches for accessibility attributes and test identifiers without making arbitrary internals part of your stable API.

Do not install two full suites because one page prefers a different visual style. Compare the cost of a focused primitive/widget against duplicate theme providers, CSS resets, overlay systems, and bundles. Mixing suites is a deliberate integration project, not a harmless import.

## Verify

Test SSR/hydration when used, portal theming, focus restoration, form error association, dense layouts at zoom, and locale/RTL support. Inspect production imports and licensing of advanced features actually shipped. During upgrades, review provider, theme, slot, and removed/deprecated component changes independently of purely visual regressions. Preserve screenshots and interaction tests for your application wrappers.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R35: Material UI getting started](https://mui.com/material-ui/getting-started/)
- [R36: Mantine getting started](https://mantine.dev/getting-started/)
- [R37: Chakra installation](https://chakra-ui.com/docs/get-started/installation)
- [R38: Ant Design introduction](https://ant.design/docs/react/introduce/)
- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
