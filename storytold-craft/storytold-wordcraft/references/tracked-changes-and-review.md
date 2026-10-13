# Reliable tracked changes and review handoffs

**Read when:** copyediting, commenting or producing a reviewable revision.

Enable tracking with `review.trackChanges {"value":true}`. Omitting value toggles the state and can turn tracking off in a document that already had it enabled. Use explicit assignments for desired state rather than toggle commands in retryable automation.

Set the author before creating tracked changes or comments. Inspect the current tracking state, revision metadata and existing reviewers. Do not accept/reject all revisions or delete comments simply to simplify a clean export unless that was part of the instruction. Preserve an editable review document separately from any clean reading copy.

Apply changes in bounded sections. Re-read the affected text and inspect revisions after each conceptual edit. A formatting operation, a tracked insertion and a deletion have different review artifacts; verify that the intended operation was recorded rather than relying on the active tracking flag alone.

For rendered proof, `convert ... --markup` can include tracked changes and comment presentation in PDF/PNG. An ordinary clean-looking PDF does not establish that revisions were discarded or absent from the editable source. Conversely, showing markup in a proof is not the same as retaining full editability in the delivered file.

A practical review handoff includes the reviewed DOCX, a rendered proof appropriate to the audience, a concise change summary, and unresolved decisions. Do not copy confidential removed passages into broadly distributed logs. After save/reopen, verify author, tracking state, representative insertions/deletions and comment anchoring.

## Evidence

- [word-mcp](https://github.com/storytold/wordcraft/blob/main/docs/mcp.md)
- [word-cli](https://github.com/storytold/wordcraft/blob/main/apps/wordcraft-cli/src/main.rs)
