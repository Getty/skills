# Files, uploads, media, and PDF-related components

**Read when:** adding uploads, previews, document viewing, audio/video, or export.

## Boundary and catalog distinctions

A file picker or drag/drop component provides interaction, not trustworthy file validation. Enforce size, type, content, and authorization on the receiving service as well as in client UX. Uppy and react-dropzone are discovery options. Distinguish `react-pdf`-style PDF viewing integrations from `@react-pdf/renderer`-style document generation; verify the exact package and worker/runtime requirements before writing code.

## Upload protocol

Specify accepted formats, maximum bytes, parallelism, cancellation, retry, resumability, integrity, and storage ownership. Treat the filename and claimed MIME type as untrusted. Use server-generated object identities and scoped upload capabilities where appropriate. Do not expose permanent storage credentials to React. A successful transfer is not necessarily a successful malware/content review or business operation.

For previews, revoke object URLs when no longer needed and bound decoded image/media dimensions. Avoid loading an entire large file into multiple copies of memory. Lazy-load decoders and workers through a CSP-compatible path. Render untrusted documents in an appropriately isolated surface; never insert arbitrary imported HTML into the app to preserve fidelity.

## Acceptance

Test zero-byte/oversized files, incorrect extensions, duplicate names, network interruption, cancellation, expired upload authorization, image orientation, and unsupported codecs. Verify keyboard alternatives to drop zones and accessible progress/error text. Test PDF/media workers in the production base path and Electron custom protocol when applicable. For export, document which data is included, sanitize dangerous spreadsheet values, and confirm generated artifacts match the canonical domain state rather than stale visible UI.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)
- [R68: DOMPurify official repository](https://github.com/cure53/DOMPurify)
- [R74: Vite](https://vite.dev/guide/)
- [E31: Native dialogs](https://www.electronjs.org/docs/latest/api/dialog)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
