# Animation, gestures, and view transitions

**Read when:** adding transitions, animated layouts, gestures, or motion-heavy interactions.

## Choose the smallest mechanism

Use CSS for simple visual state changes, React's version-gated view-transition integration for suitable view changes, and Motion when the interaction requires its gesture/layout/animation model. Current Motion documentation uses `motion` with React imports such as `motion/react`; older Framer Motion package assumptions need a migration check. Do not combine several animation owners on the same element without defining which owns transforms and lifecycle.

## Interaction contract

Specify the event that starts motion, interruption behavior, final state, exit behavior, reduced-motion alternative, and focus policy. Animation must not delay authorization feedback, destructive confirmation, or the availability of a primary action. For drag interactions, distinguish a visual gesture from the domain operation it commits.

Avoid animating properties that cause broad layout work unless that cost is acceptable. Measure on representative hardware. Keep display state correct when animations are skipped, interrupted, or disabled. An element visually leaving the screen may still be focusable until explicitly removed or made noninteractive.

## Integration review

Portal overlays, virtualized items, and React Flow nodes already have positioning/lifecycle owners. Adding a second transform to the wrong wrapper can break coordinates, hit testing, or measured bounds. Use a nested visual element when it keeps geometry ownership clear. Verify identity keys so exit/entry behavior does not accidentally discard user state.

## Acceptance

Enable reduced motion, interrupt transitions repeatedly, navigate while an exit is pending, switch tabs, and run under CPU throttling. Check that focus never lands in an invisible exiting subtree and that the final state matches the domain state after cancellation. Preserve a deterministic non-animated test path without claiming it covers timing-sensitive browser behavior.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R47: Motion for React](https://motion.dev/docs/react)
- [R02: React 19.3 release](https://react.dev/blog/2026/09/09/react-19-3)
- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
