# Styling, tokens, CSS architecture, and themes

**Read when:** choosing styling tools, building a design system, or diagnosing visual inconsistency.

## Establish one design vocabulary

Define semantic tokens for foreground/background, interactive states, typography, spacing, radius, elevation, and motion. Separate raw values from purpose: `surface-danger` is easier to evolve than scattering a particular red value. Include high contrast, dark/light modes, reduced motion, and density requirements before building many components.

Compare plain CSS/CSS Modules, utility CSS, and CSS-in-JS against the existing rendering/bundling model. Tailwind's installation differs by generation; inspect the installed major and bundler before copying a configuration. Do not add a legacy configuration file solely because an older tutorial used one. SSR style extraction, ordering, and hydration behavior depend on the selected styling system.

## Composition rules

Document precedence between component defaults, variants, consumer classes, and inline geometry. Keep behavior primitives separate from product visual decisions. Use an explicit variant API for intended combinations rather than unbounded one-off overrides. Treat reset/global styles as application-level dependencies; importing a widget must not unexpectedly restyle the host page.

Check portals and shadow roots: a dialog mounted elsewhere may not inherit a theme wrapper. Container queries, writing direction, zoom, and long translated text should work without per-screen patches. For canvas/graph components, preserve required positioning and dimensions when applying resets; an aggressive SVG or button rule can break library internals.

## Verification

Capture key states across light/dark, density, disabled/error, high contrast, and localization. Test keyboard focus outlines and 200% zoom. Inspect CSS ordering in the production bundle, not only development hot reload. Review icon-only controls, contrast, and motion manually. Do not claim that choosing an accessible primitive automatically makes the final styled composition accessible. Store tokens and documented exceptions near the components that consume them.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R30: Tailwind with Vite](https://tailwindcss.com/docs/installation/using-vite)
- [R31: Radix Primitives overview](https://www.radix-ui.com/primitives/docs/overview/introduction)
- [R33: React Aria getting started](https://react-aria.adobe.com/getting-started)
- [R74: Vite](https://vite.dev/guide/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
