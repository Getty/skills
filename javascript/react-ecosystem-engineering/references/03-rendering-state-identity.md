# Rendering, state ownership, identity, and reconciliation

**Read when:** state resets unexpectedly, lists behave incorrectly, or component architecture becomes difficult to reason about.

## Working model

Treat a render as a pure calculation from current props, state, and context. A state value read in a handler belongs to that render's snapshot. Schedule updates with functional setters when the next value depends on the previous one. Never mutate data retained by earlier renders, props, context objects, or query-cache entries.

Identity is a domain decision. Use stable entity IDs for editable, sortable, or asynchronous lists; array positions are not stable IDs. Generate an ID when an entity is created, not while rendering it. A deliberate key change can reset a subtree, but a random key can conceal an ownership bug by repeatedly destroying state. Do not define a component inside another component merely to capture props when that changes component identity.

## Procedure

Locate the source of truth, all writers, and all derived values. Delete redundant state that can be computed cheaply and deterministically. Lift state only to the lowest common owner that needs coordination. Split contexts by update frequency and consumer needs rather than placing the whole application in one object. Use reducer events to express meaningful transitions such as `itemConfirmed`, not arbitrary field patches that permit invalid combinations.

For controlled components, document the value, change callback, disabled/read-only behavior, and reset semantics. For uncontrolled components, document the initial value and how an intentional reset happens. Avoid switching an input between controlled and uncontrolled operation.

## Verify

Reorder and delete rows while a field is focused. Switch between two records with different defaults. Execute rapid repeated actions, interrupted navigation, and Strict Mode development mounting. Assert domain state and user-visible results, not render counts as a correctness contract. Development replays should reveal missing cleanup or impure behavior, not motivate disabling Strict Mode.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R01: React reference](https://react.dev/reference/react)
- [R13: StrictMode](https://react.dev/reference/react/StrictMode)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
