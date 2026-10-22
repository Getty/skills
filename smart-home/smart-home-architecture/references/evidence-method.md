# Research capabilities and user experiences

## Use evidence with a specific purpose

1. Use vendor interface/model manuals and integration documentation for intended support.
2. Inspect the actual integration/converter source at the installed release when behavior matters.
3. Use maintainer issues and users' original forum posts for observed failures, successes and workarounds.
4. Use retailer reviews only after resolving the exact variant and date. Treat anonymous ratings and affiliate roundups as weak leads.

A firsthand issue is primary evidence for the author's experience, not proof of all installations. Maintain a separate technical conclusion and confidence statement. Do not turn the number of open issues, stars or enthusiastic posts into a reliability percentage.

## Search reproducibly

Search exact model plus full manufacturer identifier, integration and symptom. Then search the same model for successful setup and fixes. Include German and English terms where useful. Follow linked issues/PRs; note whether a fix is merged, released, or actually installed. Search with a recent window for current regressions and without a window for long-standing device behavior.

For a Tuya device, search the full `_TZE…`/`_TZ…` signature together with `TS0601`, not just the shared model. For an NVR, include its hardware code. For a plug, include region and generation. For a TV, include OS family, model/year and power settings.

## Store an evidence card

```yaml
claim: "Describe one capability or observed symptom"
source_kind: "official-doc | implementation | firsthand-report | local-test"
source_url: "https://example.invalid/replace-with-real-source"
published_or_reported: null
checked_on: "2026-10-22"
model: null
hardware_revision: null
firmware: null
integration_and_version: null
topology: null
observed_behavior: null
mitigation: null
status: "unknown | open | fixed-upstream | released | locally-confirmed"
limitations: "State which identifiers or comparisons are missing"
```

The example URL is an explicit placeholder and is not a source. Never save a completed evidence card with an invented source or date.

## Handle conflicting or stale material

An old missing-feature post and a newer feature announcement can both be truthful. Explain the release boundary. A closed issue may be stale, duplicate or unconfirmed rather than fixed; inspect the closing reason. A positive report on a direct camera does not settle NVR-mediated support. A bridge being local does not establish local control for every bridged function.

At this collection's research date, some live pages already describe HA **2026.11**. That version is later than **2026-10-22**. Label forward-looking guidance, verify release tags, and do not present it as released behavior. Treat `main`, `dev`, and documentation previews similarly. Use installed versions as the operational authority.

## Convert evidence into a useful experiment

Propose the smallest discriminating check. Examples: compare a direct versus NVR event; keep an ESPHome proxy's hardware/YAML constant while testing a known fixed release; verify a temperature sensor's reporting threshold against a controlled temperature change. Measure latency, lost events, stale intervals and recovery explicitly. Do not use a room's day-long ambient drift as proof of sensor accuracy.

Cite sources beside claims in user-facing recommendations. For the suite, use source ledgers to refresh claims; do not treat a checked-on date as permanent validity.
