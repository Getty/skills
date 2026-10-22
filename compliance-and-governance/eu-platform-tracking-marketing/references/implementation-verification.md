# Implement and verify consent end to end

Sources: T2–T8. These are engineering controls supporting consent rules; test scope and limitations must remain explicit.

## Consent state model

Use explicit states such as `unknown`, `refused`, and `granted` for each purpose/vendor version, with an auditable change event. Treat unknown as not granted for consent-dependent operations. Do not confuse a stored UI selection with an authenticated guarantee of valid consent; validate origin/integrity and expiry rules proportionately.

Use one authoritative enforcement point or a well-defined shared policy contract across browser, mobile SDK, backend event pipelines and providers. Keep consent updates ordered so stale asynchronous jobs cannot re-enable a withdrawn purpose. A global boolean is often too coarse for different purposes and vendors.

## Prevent early access and disclosure

Inspect server-rendered tags, preload/prefetch/preconnect where relevant, tag managers, iframes, embedded media, SDK constructors, service workers, route transitions, error reporting, session replay, conversion APIs, attribution links and mobile lifecycle events. A component can transmit before it renders a visible consent interface.

Load only the operations justified before consent. For optional embeds, use a local placeholder and an accurately described activation path. Do not assert every third-party asset always requires device consent; analyse terminal operations and personal-data disclosure separately.

Server-side tags must enforce purpose eligibility before forwarding events. Block unauthorised identifiers and content at the source, not merely in the vendor dashboard. Enforce an allowlist for event fields, strip sensitive query strings/prompts, and prevent free-text form data or passwords from entering analytics.

## Refusal and withdrawal

Keep core requested service functionality working where optional tracking is refused. Ensure keyboard/screen-reader/mobile usability and no deceptive visual choices. Withdrawal must be as easy as giving consent under Art 7(3); make the route discoverable from relevant surfaces.

After withdrawal, stop future consent-dependent access/use and downstream forwarding, cancel or suppress queued jobs, update vendors where necessary, and determine the lawful handling of existing data. Delete optional local identifiers where appropriate; a retained minimal refusal marker may itself be justified to remember the choice. Do not repeatedly pressure refusal into acceptance or silently regenerate identifiers from account/fingerprint data.

## Proof without overcollection

Record purpose/vendor scope, notice/version, choice, timestamp, collection surface, evidence method, withdrawal and necessary recipient propagation. Use a proportional identifier; do not store full IP/user-agent histories indefinitely simply to prove consent. Set purpose-specific evidence retention based on actual legal needs, not a universal number.

A double-opt-in flow can improve evidence for email registration but does not repair vague wording, purchased lists, coercion or an unrelated recipient/purpose. A CMP/IAB-style consent string is a signal that must be tied to a lawful collection process; it is not legal certification.

## Verification matrix

Use an isolated profile or cleared application state and synthetic test data. Capture actual storage and network behaviour for:

1. First load and navigation before any choice.
2. Refuse all, reload, new route and later visit.
3. Purpose-specific grant; confirm only the authorised subset starts.
4. Accept all; confirm actual recipients match the notice/register.
5. Withdraw/restrict; verify cessation, local cleanup, backend suppression and queued-event handling.
6. Logout/login, account switch and multiple tabs/devices where choice propagation is claimed.
7. Changed vendor/purpose/version and expired or corrupted state.
8. Failure of the CMP, tag manager, network, storage API or geographic classification.

Test the product's policy for unknown geography, not an invented legal rule that IP always determines the applicable country. Keep optional consent-dependent operations disabled until a reliable decision is available. Inspect server-side destinations because a clean browser request list alone cannot establish the whole flow.

Report failing operation/recipient, reproducible steps, state, payload category, version, expected control and evidence. Do not retain raw screenshots or network captures containing real customers, payment details or credentials in public issues. After fixing concrete gaps, rerun affected scenarios; avoid endless unrelated scans.
