# TypeScript and component contracts

**Read when:** designing public props, generic components, integration boundaries, or runtime schemas.

## Model valid states

Use discriminated unions for mutually exclusive modes: loading versus ready versus failed, internal versus external links, or text versus numeric node types. Make impossible combinations unrepresentable before adding runtime conditionals. Prefer `unknown` at network, storage, IPC, and extension boundaries; narrow it with a parser. Type assertions do not validate data.

Derive DOM-facing props from the intended element, then explicitly omit conflicts. Preserve the element's accessible naming and event semantics. A polymorphic `as` API increases ref, prop, and semantic complexity; add it only when there is a real composition requirement. Keep refs correctly typed for the installed React generation. React 19 supports ref as a prop; older consumers may still require a compatible forwarding strategy.

## Tooling contract

Enable strict checking and test whether `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` are suitable for the repository. Do not silently weaken an existing configuration. Separate browser and server/Node libraries in tsconfig boundaries so accidental privileged imports fail visibly. Distinguish `tsc --noEmit` from a bundler transform that strips types without checking them.

Prefer inference from a schema only after deciding how input and parsed output differ. Defaults, transforms, coerced numbers, date parsing, and optional values can change that distinction. For generic tables or graphs, preserve the row/node union through callbacks rather than erasing it to `any`.

## Verify

Add compile-time fixtures that reject invalid props and event payloads, plus runtime fixtures for malformed external values. Test omitted versus explicit `undefined`, empty strings, numeric edge cases, and unknown discriminants. For exported libraries, build declarations and compile a separate consumer fixture. Avoid claiming source compilation alone proves a published package's export map works.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R12: React TypeScript guide](https://react.dev/learn/typescript)
- [R54: React Flow TypeScript](https://reactflow.dev/learn/advanced-use/typescript)
- [R25: Zod](https://zod.dev/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
