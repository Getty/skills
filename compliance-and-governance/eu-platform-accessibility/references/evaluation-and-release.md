# Evaluation and release evidence

## Scope the evaluation

Inventory pages, templates, components, dynamic states, authenticated roles, device classes, locales and complete user journeys. Prioritize registration, authentication, payment, contract exits, data access and the core AI workflow. Record sampling rationale and exclusions. A sample can support a scoped assessment; it cannot justify a claim that unexamined features were tested.

## Combine methods

Use automated checks for machine-detectable issues and inspect whether the tested DOM states include dialogs, loading, validation and streamed content. Keep tool version and ruleset. Follow with manual keyboard, screen-reader, zoom/reflow, contrast and input-alternative checks. Involve users with disabilities where feasible to uncover interaction problems, while keeping standards evaluation separately documented. W3C explicitly warns that no tool alone can determine accessibility. [A12]

## Suggested core journeys

| Journey | Essential observations |
| --- | --- |
| Sign up and authenticate | Labels, instructions, MFA alternatives, errors, focus and recovery |
| Buy or change plan | Total price, comparison, payment, validation and durable receipt |
| Withdraw/cancel | Discoverability, minimal data, confirmation and receipt |
| Ask an AI question | Input naming, history navigation, streaming control and stop/retry |
| Approve a tool | Proposed action, consequences, reject/cancel, focus and outcome |
| Upload/export | File selection, progress/errors, document structure and links |
| Get support | Accessible route beyond a failing AI chat |

Use representative browser/OS/assistive-technology combinations based on audience and product support. Record exact versions rather than promising universal compatibility. Test at small viewport and increased text size. Include localization expansion and right-to-left behavior if supported.

## Finding format

Record task, preconditions, steps, observed result, expected criterion, user consequence, severity, screenshots or text evidence, affected versions, owner and fix. Separate legal duty from technical target. A severe barrier can exist without an automated violation; an automated warning may require human interpretation.

## Release decisions

Use explicit outcomes: scoped tests passed; known findings accepted under a reviewed plan; release blocked for a material barrier; or assessment incomplete. Do not equate `no_automated_findings` with `compliant`. Test repaired components in all affected core journeys, not only a synthetic component demo. Verify legal notices and receipts remain usable after language and content updates.

Keep nonconformity, contractual and public-information implications in the remediation workflow. Retain test evidence proportionately, with personal-data minimization. A screenshot containing a real user's chat should not become a broadly accessible audit artifact.
