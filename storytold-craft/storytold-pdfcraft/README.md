# PdfCraft skill

Read, inspect, organize, annotate, edit, secure and verify PDFs through PdfCraft's CLI and schema-described automation tools.

Start with [SKILL.md](SKILL.md). This entire folder can be installed independently in an agent's supported skill directory. No sibling folder is required and no host-specific installer or MCP client configuration is assumed. Preserve the folder structure; references load only when relevant.

## Contents

- [CLI commands and session-scoped tool scripts](references/cli-and-tool-scripts.md) — extracting PDF information, scripting a multistep edit, or discovering exact schemas.
- [MCP schemas, compact discovery and filesystem authority](references/mcp-and-root-policy.md) — starting PdfCraft automation or interpreting a validation refusal.
- [Page indexes, displayed geometry and existing-text edits](references/pages-geometry-and-text.md) — rotating/reordering pages, placing annotations or editing existing text and artwork.
- [Forms, review annotations and signature-sensitive workflows](references/forms-comments-and-signatures.md) — filling forms, editing field properties or preserving review intent.
- [Redaction, sanitization and accessibility evidence](references/redaction-sanitization-accessibility.md) — removing confidential information or preparing a security/accessibility-sensitive deliverable.
- [Save semantics and PDF acceptance gates](references/save-reopen-and-robustness.md) — committing edits or testing a heterogeneous PDF corpus.
- [Runtime discovery, bounded execution and evidence](references/runtime-and-evidence.md) — setting up an agent, running the supplied helpers, or deciding what has actually been verified.
- [Sources and review boundaries](references/sources.md) — verifying claims, exact source identities or version drift.

Machine-readable records: [runtime profile](assets/runtime-profile.json), [sources](assets/sources.json), [verification template](assets/verification-record.example.json), [verification schema](assets/verification-record.schema.json), [agent evaluation cases](tests/evaluation-cases.json).

## Validation boundary

Read [VALIDATION.md](VALIDATION.md). Source-reviewed examples are not represented as application-tested. Python helper tests use synthetic subprocesses, not the editor. This skill is original instructional synthesis with linked primary sources, not an upstream-official skill or a redistribution of the application.
