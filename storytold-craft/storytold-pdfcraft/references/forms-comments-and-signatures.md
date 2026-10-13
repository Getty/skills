# Forms, review annotations and signature-sensitive workflows

**Read when:** filling forms, editing field properties or preserving review intent.

Discover fields and annotations before editing. A visible label is not necessarily the field's internal name; form data, field appearance and surrounding page text can disagree. Read the current schema and values, apply a bounded change, then inspect both stored value and rendered appearance.

`form_set_props` can update one field or a list of 1–1000 unique field names. The multi-field variant is atomic and creates one undo step. A missing/locked field, malformed appearance or invalid option refuses the whole edit. Only supplied properties change; field identity/rectangles/rotation require the single-field form. This local atomic guarantee must not be transferred to generic `command_batch`.

Treat field scripts, file import/export, external resources, passwords and cryptographic signing as distinct operations with explicit permission. Do not extract passwords or private keys into a recipe file or transcript. A pasted signature image is not a cryptographic signature, and a visually signed page is not a verified signer identity.

## Image-signature previews

`comment_image_preview` can return the page background without a selected signature/initials and the isolated image layer with alpha. It reports displayed rectangle, rotations and opacity. For proportional resizing, use the embedded image's actual aspect ratio, not a rectangle that may already have been stretched. `comment_edit` commits the new geometry; the preview itself does not mutate the document.

For review handoff, preserve annotation identities, authors, relevant page references and decisions about accepting/removing comments. Validate saved/reopened fields and annotations instead of checking only the in-memory editor. When a document has cryptographic signatures, inspect verification status after the intended operation and report any change rather than promising that a save preserved validity.

## Evidence

- [pdf-automation](https://github.com/storytold/pdfcraft/blob/7163ba3dee8becfff6871c9a65d0d8314314742b/crates/automation/README.md)
- [pdfcraft-readme](https://github.com/storytold/pdfcraft/blob/main/README.md)
