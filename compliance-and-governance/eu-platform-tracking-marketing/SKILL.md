---
name: eu-platform-tracking-marketing
description: "Use when adding or auditing cookies, local storage, analytics, pixels, SDKs, session replay, fingerprinting or server-side tagging, building a consent banner or CMP, or sending newsletters, email, SMS or phone marketing — ePrivacy, TDDDG, UWG, GDPR."
---

# EU Platform Tracking and Marketing

Review actual terminal operations, personal-data uses, message channels and recipient relationships.
Keep three separate permissions: device access, subsequent personal-data processing, and marketing contact.
Add advertising/platform restrictions and national rules where the facts trigger them.
Use English working documents and accurately localised user controls.

## Establish scope

1. Identify the operating entity, relevant markets/countries, intended users and product surfaces.
2. Inventory every script, SDK, pixel, storage key, fingerprint input, backend event and recipient.
3. Capture the exact purpose, data, trigger, lifetime, sharing and identity joins for each operation.
4. For messages, identify channel, promotional content, recipient type, source and existing relationship.
5. Record unknown vendor behaviour or consent provenance as `needs-evidence`.
6. Choose the applicable national overlay before asserting an exemption.

Do not assume `cookieless`, `server-side`, `anonymous analytics`, `B2B`, or `GDPR-ready` means exempt.
Do not collect raw customer prompts or sensitive page contents merely to measure compliance.

## Source discipline

Read [sources.md](references/sources.md) for primary laws, adopted guidance and source limits.
Record assessment date, operative legal version, country and source/article for each obligation.
Treat proposed changes to ePrivacy/GDPR as changes only once enactment and applicability are established.
Differentiate national legislation, regulator interpretation and conservative product design choices.
Do not export Germany's UWG contact rules or another country's analytics interpretation across Europe.

## Workflows

### 1. Determine terminal-access and data-processing requirements

Read [terminal-access-consent.md](references/terminal-access-consent.md).
Apply the relevant national implementation of ePrivacy Art 5(3) to storing/accessing terminal information.
Assess the narrow exceptions operation by operation and record the requested service/necessity.
Then assess GDPR scope, lawful basis, transparency, rights, recipients and transfers separately.
Use [consent-register.yaml](assets/consent-register.yaml) as the purpose/vendor control record.

### 2. Build enforceable consent controls

Read [implementation-verification.md](references/implementation-verification.md).
Block consent-dependent operations before a valid choice; include prefetch and server-side paths.
Provide clear granular information, an affirmative choice, practical refusal and easy withdrawal.
Keep consent proof proportionate and tied to the exact notice/purpose/vendor version.
Do not make a framework consent string the sole evidence that consent was valid.

### 3. Verify the real browser/app behaviour

Use [tracking-test-plan.md](assets/tracking-test-plan.md).
Test fresh state, no choice, refusal, selected purposes, acceptance, withdrawal and changed configuration.
Inspect storage, actual network requests, payloads, backend exports and identity joins.
Record environment, commit, configuration, browser/device, locale, result and limitations.
Treat a banner screenshot as UI evidence only; it does not prove that tracking was blocked.

### 4. Review a campaign

Read [direct-marketing.md](references/direct-marketing.md).
Use [campaign-review.md](assets/campaign-review.md) for channel, recipient, country and evidence checks.
Verify both the permission to contact and the GDPR basis for address selection/profiling.
Check consent scope or every condition of a relied-on existing-customer exception.
Apply suppression before sending and to queued retries, automation and external marketing providers.
Review AI-generated outbound messages using the same legal checks as human-written campaigns.

### 5. Review profiling and advertising

Read [profiling-adtech.md](references/profiling-adtech.md).
Assess sensitive inferences, children, data-broker inputs, audience matching and ad recipients.
Screen DSA and other advertising restrictions only where the service/feature is in scope.
Do not let a person's marketing opt-in waive a separate statutory advertising prohibition.

### 6. Adapt for countries

Read [jurisdiction-overlays.md](references/jurisdiction-overlays.md).
Apply the German TDDDG/UWG overlay only where relevant; obtain national sources for other markets.
Use common enforcement infrastructure with country-specific rules/decisions where justified.
Treat the UK and Switzerland as separate regimes, not automatically as EU implementations.

## Reopen review when behaviour changes

Trigger a review for new SDK/tag/recipient/purpose, consent wording, storage lifetime, fingerprinting,
session replay, page content, sensitive segment, cross-device link, new country or campaign channel.
Also trigger on a vendor's configuration change, new server-side export, failed suppression or legal update.
Do not rely on a scan from before the latest tag-manager publish.

## Required output

Return a concise map plus:

| Field | Required content |
| --- | --- |
| Operation/campaign | Exact surface, trigger, channel, purpose, recipient/data and country |
| Legal layers | Terminal access; GDPR; marketing channel; advertising restrictions where relevant |
| Decision | Applicable rule/exemption with source/article, facts and uncertainty |
| Control | Blocking/choice/withdrawal/suppression behaviour and actual implementation |
| Evidence | Consent text/version, logs, bounded tests, date/configuration and limitations |
| Status/action | `satisfied`, `gap`, `needs-evidence`, `needs-review`, or justified `not-applicable`; owner and due date |

Escalate disputed exemptions, consent-or-pay designs, sensitive/minor profiling, bought lists,
unproven contact permission and unreviewed national expansion before the affected activity starts.
Continue authorised reversible implementation and tests using synthetic users and recipients.
Prepare a concrete reviewed campaign configuration; do not send marketing messages without authorisation.
Do not describe the audit as a blanket legal guarantee.
