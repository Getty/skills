# Runtime monitoring and response

## Suggested signals

Track vendor/model configuration changes, new outbound hosts, consent-state/request mismatches, delete-job failures, unexplained retention growth, tenant isolation alerts, revoked-share access, unexpected public indexing, blocked abusive tool actions, output-marking loss, accessible journey regressions and legal-source review deadlines.

These are suggested operational signals, not a claim that every law mandates every log. Choose a purpose, owner, threshold, minimal fields, retention, access and response for each. Prefer counts, anonymised/aggregated trends where valid and synthetic probes. A security investigation may need more detail temporarily; record that purpose and limitation.

## Signal-to-action workflow

1. Validate the signal against deployment/version and known changes.
2. Identify affected users/data, feature and applicable controls.
3. Separate a technical alert, a failed contractual promise, a suspected legal breach and an actual incident.
4. Execute only authorised containment. Preserve evidence and engage the accountable incident owner.
5. Reassess notification/reporting thresholds and clocks under the relevant specialist skill.
6. Produce remediation, acceptance evidence and an explicit closure/reopen rule.

Do not equate alert volume with compliance risk. A missing alert is not proof that a control works. Verify monitor health and synthetic failure paths.

## Drift categories

Configuration drift: telemetry, model training settings, regions, permissions or feature flags no longer match the reviewed state.

Product drift: new customer uses, features, public claims or distribution modes change legal scope.

Evidence drift: reports are stale, broken, from another release/environment or no longer prove the current control.

Legal drift: the operative law, national implementation, authority guidance or contract changed. Use regulatory-watch for legal effect; a hash difference is only a signal.

## Scheduling boundary

Document the recommended cadence and ownership in the project. Do not create a background task, external subscription, chat notification or automation merely by loading this skill. If monitoring is explicitly requested, configure only the authorised data sources, schedule and recipients, and report what actually runs. A skill file is not a running monitor.

## Privacy of monitoring

Do not collect full customer prompts, credentials or documents for routine metrics. Redact before agent access. Limit retention and cross-border monitoring vendors. Validate that the controls used to supervise the platform do not create a new unassessed processing purpose or leak sensitive evidence into source control.
