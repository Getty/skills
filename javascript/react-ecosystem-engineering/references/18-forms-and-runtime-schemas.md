# Forms: React Hook Form, TanStack Form, and schemas

**Read when:** building complex forms, field arrays, validation, or schema-driven UI.

## Form contract

Define input representation separately from parsed domain output. A numeric text field needs to represent empty and temporarily invalid text without immediately destroying the user's draft. Decide when validation runs, when errors are announced, how server errors map to fields, and how defaults/reset behave after data changes.

React Hook Form and TanStack Form offer different form-state integration surfaces; use the installed library's intended ownership model. Avoid simultaneously controlling every field through an unrelated global store. Zod can provide runtime schemas, but its major-version behavior, coercions, transforms, and input/output types must be checked with the chosen resolver/adapter.

## Implementation sequence

Start with semantic labels, descriptions, fieldsets, and submit buttons. Add schema parsing at submission and targeted feedback during editing. For asynchronous validation, cancel or ignore obsolete requests and distinguish “not checked” from “valid.” Treat field arrays as entities with stable keys; deleting one row must not shift another row's draft into it.

For custom widgets, document controlled value shape, blur/touched events, ref/focus behavior, disabled/read-only behavior, and error association. A select with an object value needs a stable identity and serialization plan. File inputs, rich editors, date pickers, and masked inputs each need explicit adapters rather than pretending they are ordinary strings.

## Acceptance

Submit entirely by keyboard, trigger multiple errors, focus the first actionable error, edit during pending validation, reorder array fields, and reset to a different record. Test server rejection after optimistic UI, duplicate submit, loss of connectivity, and preservation of dirty fields during background refetch. Compare client and server schemas without assuming a shared package automatically enforces authorization or business invariants.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R24: React Hook Form repository](https://github.com/react-hook-form/react-hook-form)
- [R25: Zod](https://zod.dev/)
- [R26: TanStack Form](https://tanstack.com/form/latest/docs/overview)
- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
