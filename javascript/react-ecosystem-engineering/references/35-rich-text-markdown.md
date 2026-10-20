# Rich-text editors, Markdown, and collaborative documents

**Read when:** embedding an editor, rendering user-authored content, or enabling collaboration.

## Define the document contract

Choose the canonical representation before selecting UI: a versioned rich-text tree, Markdown with documented extensions, or a constrained HTML format. Tiptap and Lexical have different extension/state architectures. Do not treat their serialized trees as interchangeable or assume a DOM snapshot is a durable schema. Slate, Plate, ProseMirror, and the unified/remark/rehype ecosystem are additional catalog routes requiring focused review.

Separate editor state, domain metadata, upload references, and collaboration transport. Give each mounted editor instance a clear lifecycle owner and dispose listeners/plugins on unmount. Avoid replacing the entire document on every React render or background refetch, which can reset selection and undo history. Controlled React props should not accidentally become a second authoritative editor engine.

## Trust and persistence

Treat pasted HTML, links, imported documents, embeds, and collaborative updates as untrusted. Parse only allowed schema nodes/marks and apply an appropriate maintained sanitizer when HTML is rendered. A Markdown parser is not automatically an HTML sanitizer. Restrict link schemes and embedded content; never enable arbitrary script/iframe execution to match a document's appearance.

For Yjs-backed collaboration, explicitly choose shared document structure, provider, persistence, authentication, awareness/presence, offline/reconnection behavior, and compatible editor bindings. CRDT convergence is not permission enforcement. Undo needs an origin/user policy, not a whole-document replacement that overwrites peers.

## Acceptance

Test paste from office tools, malformed content, emoji/IME composition, large documents, link handling, undo across async image upload, and reload from old schemas. For SSR, follow the editor's documented client initialization rather than guessing browser globals. Check licensing for optional collaboration services/extensions and preserve required notices. Benchmark typing and selection, not only initial render.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R62: Tiptap React](https://tiptap.dev/docs/editor/getting-started/install/react)
- [R63: Lexical React](https://lexical.dev/docs/getting-started/react)
- [R64: Yjs](https://docs.yjs.dev/)
- [R68: DOMPurify official repository](https://github.com/cure53/DOMPurify)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
