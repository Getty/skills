# Practical implementation patterns and example map

**Read when:** translating architecture guidance into code.

## Start from the supplied executable core

The Flow example separates pure graph validation/history from the React canvas. Run its offline model tests first. Inspect the allowed node/port vocabulary and extend it deliberately; do not weaken validation to accept arbitrary imported data. The TSX editor is an integration example requiring dependency installation, peer checks, typechecking, and browser execution in your environment.

The subscription hook demonstrates resource cleanup and a stable domain event contract. The query example demonstrates request cancellation, response status checking, a runtime parser, and resource-key scope. The form example shows the separation between a text draft and parsed domain input. These snippets are not a complete backend, authentication integration, or production design system.

## Pattern: one state owner

A component reads a selected entity and emits a domain command. The command handler validates the current revision and creates a new state. The view does not maintain another independent copy of the same saved entity. Temporary input drafts are explicit and merge only through a defined submit/cancel workflow.

## Pattern: bounded async work

Every external operation has an owner, input limit, cancellation or obsolete-result rule, timeout/retry policy, sanitized error, and observable completion condition. A UI spinner does not establish any of these. For an async graph layout, record the source revision and reject stale completion. For saves, use conflict-aware revisions rather than last writer wins by accident.

## Review before copying

Check imports against installed versions, adapt aliases/build settings, preserve accessible labeling, and connect real domain schemas. Read the example README and validation report. Run `tsc --noEmit`, production build, relevant tests, and browser behavior after installation. Do not promote a source-reviewed snippet to “tested integration” merely because its TypeScript syntax transpiles.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R04: Effects decision guide](https://react.dev/learn/you-might-not-need-an-effect)
- [R18: TanStack Query defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)
- [R24: React Hook Form repository](https://github.com/react-hook-form/react-hook-form)
- [R25: Zod](https://zod.dev/)
- [R54: React Flow TypeScript](https://reactflow.dev/learn/advanced-use/typescript)
- [E07: IPC tutorial](https://www.electronjs.org/docs/latest/tutorial/ipc)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
