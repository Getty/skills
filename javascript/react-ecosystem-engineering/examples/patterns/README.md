# Integration sketches

These snippets were syntax-transpiled, not installed-library typechecked or browser-tested. Add them only after checking the project's React, TanStack Query, React Hook Form, and Zod generations. They are not a standalone package.

`use-domain-events.ts` demonstrates a subscribe/unsubscribe lifecycle. `query.ts` demonstrates tenant-scoped cache identity, cancellation, status checking, and runtime parsing. `form.tsx` preserves numeric text drafts and parses at submission without assuming a particular resolver version. A production form still needs first-error focus, server field-error mapping, idempotency/business validation, and tests. The query service must enforce response-byte limits before JSON decoding; a row-count check alone does not bound transport memory.
