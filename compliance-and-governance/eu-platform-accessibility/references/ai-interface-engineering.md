# AI interface engineering

## Chat and streaming

Use a navigable conversation structure with sender identification, timestamps where useful, headings and a predictable reading order. Preserve focus in the input when new content arrives unless the user requested a context change. Avoid moving focus to every streamed update. Provide an accessible status for generating, waiting for a tool, failure and completion; allow users to control announcements. A polite live region that appends every token can still be unusable.

Make stop, retry, regenerate, copy, edit and branch actions available by keyboard with contextual names. Preserve the user's position when older messages load. Do not create an infinite focus trap through virtualized messages. Expose links, tables and code semantically. Maintain text equivalents for meaningful images and audio; distinguish a generated description from a verified description.

## Agent approvals and tools

An approval dialog must clearly identify the proposed action, target, effect, choices and relevant uncertainty. Use labels comprehensible outside color or icon context. Keep reject and cancel usable and do not allow a timeout to silently become approval. Restore focus to a sensible location after completion. For dangerous or financially consequential actions, integrate the platform's approved confirmation policy without inaccessible cognitive puzzles.

Provide a linear alternative for workflow graphs, drag-and-drop builders, canvases and branching conversations. A keyboard shortcut alone is insufficient if the feature has no discoverable instructions or focus representation. Make selected state, relationships and validation errors programmatically understandable.

## Accounts and ecommerce

Test SSO, MFA, passkeys, password managers and recovery. Do not block paste or force memory tasks without assessing accessible alternatives. Include PSP and consent manager overlays, withdrawal forms and cancellation receipts. BFSGV § 19 specifically covers relevant identity/security/payment functions; a third-party iframe cannot be omitted from the user journey merely because it is outsourced. [A4]

## Visual, audio and timing controls

Respect zoom, reflow, text spacing, contrast and motion preferences. Ensure focus is visible and not hidden behind sticky chat inputs or banners. Use adequate target size and alternatives to dragging. Make timeout extensions and error recovery usable. Voice must have an alternative when speech or hearing is unavailable; user-generated and generated content need a defined accessibility strategy rather than a promise that a model always creates correct captions or descriptions.

## Documents and exports

Generate structured HTML or tagged/document formats with headings, reading order, language, tables, alt-text review and accessible links. A PDF screenshot of the chat is not an accessible transcript. Include plain structured exports where useful, while checking the legally relevant delivery format. Test generated invoices, contract notices and receipts, not just the application shell.

## Implementation method

Start with native elements and tested design-system components. Add ARIA only with the required behavior; role labels cannot repair missing keyboard logic. Define accessibility acceptance criteria next to component behavior, and preserve them in regression checks. These are engineering methods for meeting selected targets; cite the exact standard criterion when asserting conformance. [A11, A12]
