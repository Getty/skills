# Tables, data grids, and high-density editing

**Read when:** implementing sorting, grouping, selection, inline editing, or large datasets.

## Version and product gate

The reviewed TanStack Table current documentation is v9. Its headless processing/state model is not a styled grid, and v8 snippets must not be presented as current APIs without a migration label. Check the installed major before row-model factories, feature composition, and state subscriptions. AG Grid is a more integrated grid option; MUI's data-grid products have separate feature/licensing surfaces. Verify the exact package and edition.

## Data contract

Define stable row identity, column schema, null ordering, comparator behavior, selection scope, edit validation, and server/client ownership of sorting/filtering/pagination. Never sort one fetched page locally while presenting the result as a globally sorted dataset. “Select all” must say whether it means loaded rows, the current page, or all matching server records.

Keep editable drafts separate from acknowledged records. An optimistic edit needs row revision/conflict behavior and a recoverable rejected state. Persist column layout by stable column IDs with a schema version; renamed or removed columns need migration.

## Performance and usability

Choose pagination and/or virtualization based on actual interaction requirements. Pinning, variable row heights, grouping, expanded rows, keyboard navigation, and merged cells complicate virtualization. Memoize expensive cell calculations at a meaningful boundary; avoid mounting a heavyweight editor in every non-editing cell. Preserve focus during resorting and expose understandable loading/empty/error states.

## Acceptance

Test duplicate/missing IDs, null values, long text, very large numbers, timezone-sensitive dates, keyboard cell editing, rejected saves, and refresh during an edit. Verify export includes the intended rows and columns and prevents spreadsheet-formula injection when generating CSV. Test licensing-dependent features in the packaged production artifact, not merely an evaluation environment.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R40: TanStack Table](https://tanstack.com/table/latest)
- [R41: AG Grid React](https://www.ag-grid.com/react-data-grid/getting-started/)
- [R35: Material UI getting started](https://mui.com/material-ui/getting-started/)
- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
