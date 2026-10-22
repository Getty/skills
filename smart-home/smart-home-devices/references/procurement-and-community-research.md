# Buying research and interpretation of user experience

Research baseline: 2026-10-22. Run current research whenever recommending a purchase, a firmware upgrade or a substantial migration. Product availability, hardware revisions, app requirements and integration support change. This workflow applies to Amazon Germany/EU listings and other retailers; an ASIN identifies a listing, not necessarily a fixed hardware revision.

## Start from the need

Write down required functions, acceptable outage behavior, installation constraints, region/socket/voltage, budget, existing radios/hubs and maintenance tolerance. Use the inventory already available; do not demand a new complete export before doing useful work. Separate “must work locally after setup” from “must never need an account,” because they are different requirements.

Compare at least one route that preserves working devices with any replacement proposal. A new hub or protocol is justified by a concrete capability, reliability problem or operating constraint, not by a general preference for novelty.

## Identify the exact purchasable variant

| Field | Where to verify | Why it changes the decision |
| --- | --- | --- |
| Full model / article / EAN and chosen variant | Manufacturer page/manual, listing variation, delivered label | Similar retail names can cover Zigbee, Wi-Fi, BLE, Matter and older generations |
| Regional version | Official regional specification and socket/valve/lock fit | Plug type, supply, radio, heating valve, lock body and app region can differ |
| Hardware and firmware revision | Label, device diagnostics, dated owner report | A new production batch may expose different fingerprints or capabilities |
| Hub requirement | Manufacturer installation instructions and integration page | “Works with Alexa” does not identify a direct HA transport |
| Integration path | Current HA documentation or exact Z2M definition; custom project release/code | A brand name or HACS listing is not exact-model support |
| Required features | Exposes/entities/actions and a same-model test | Discovery and on/off do not prove metering, button events, zones or updates |
| Subscription / account / service | Current vendor terms and API documentation | Local operation can still rely on cloud commissioning or token refresh |
| Total cost | Dated price, required bridge/radio, adapters, batteries and subscriptions | Compare the functioning system, not only the endpoint's price |

When a seller merges reviews, use the review's selected variant, date and attached label if available. Do not carry a Zigbee review over to a Wi-Fi variant. Avoid basing technical compatibility on a marketplace title or generated shopping summary alone.

## Research sequence

1. Open the official model manual/specification and identify the actual transport and installation requirements.
2. Open the current official HA integration page or exact Z2M device page. For ZHA, inspect the actual quirk/support source when specialized behavior matters; a Z2M listing is not automatic ZHA proof.
3. For custom integrations, inspect the canonical repository, released version, supported models, open issues, installation procedure, maintenance activity and recovery steps. A community fork may be appropriate, but identify its owner and compatibility explicitly.
4. Search original issues and community posts with exact model, firmware, integration and symptom. Read enough of the thread to identify the original report, attempted workaround and final state.
5. Search for disconfirming evidence: different firmware, resolved bug, alternative route, successful same-model setup or a maintainer explanation. Do not treat repeated copies of the same report as independent evidence.
6. Check present-day price and availability immediately before a purchase recommendation. State the market/date and any missing specification. Do not order or pay unless the user has authorized that action.

Example search patterns, substituting actual identifiers:

```text
"3RSPE01044BZ" site:zigbee2mqtt.io
"3RSPE01044BZ" "1.01.01" site:github.com/Koenkk/zigbee2mqtt/issues
"TS0601" "_TZE200_exact_signature" home assistant
"exact model" "exact firmware" unavailable site:community.home-assistant.io
"integration-domain" "HA version" site:github.com/home-assistant/core/issues
"manufacturer article number" manual Zigbee Matter
```

These are query templates, not claims that each query has results. If search fails, retain “unknown” and ask for the smallest useful fingerprint rather than silently substituting another model.

## Evaluate firsthand evidence

Capture source URL, original report date, model/fingerprint, firmware, HA/integration/coordinator versions, symptom, reproduction, attempted workaround, outcome and status at review. Explicitly mark missing fields. Keep alleged causes separate from observed facts. A user can accurately report “the entity became unavailable after an update” without proving that update was the sole cause.

Use these labels:

| Label | Appropriate meaning |
| --- | --- |
| Documented support | Current primary integration/device documentation names the model or capability |
| Reproduced here | This task's actual hardware/software passed a stated test |
| Firsthand report | An identifiable original participant describes their experience; not independently reproduced here |
| Maintainer diagnosis | A maintainer interprets the report; still distinguish a hypothesis from a demonstrated fix |
| Reporter-resolved | The reporter describes recovery; capture the specific conditions |
| Fixed in release | A linked change/release and applicable version establish the claimed fix |
| Closed / duplicate / stale | Repository workflow status only; do not equate with functional resolution |
| Unknown | Evidence does not resolve the claim |

Never derive a failure rate or a reliability ranking from issue counts. There is no denominator for installed devices, and popular products often generate more reports. Do not call two similar posts “consensus.” Use anecdotes to design acceptance tests and identify risks worth checking.

## Produce a reviewable comparison

Use one row per exact candidate/route with: required capabilities, local/cloud dependency, hub requirements, features lost, identity confidence, dated primary sources, directly relevant user report, price/market if checked, and unresolved test. Recommend the candidate whose verified behavior best fits the user's constraints. If a required feature remains unknown, state a return-window pilot or the exact vendor question rather than claiming full compatibility.

When reporting experiences, include successful workarounds and unresolved cases. Explain whether a result applies to a particular firmware or protocol. Do not use review tone, affiliate rankings, star averages or brand reputation as substitutes for the missing technical evidence.

## Date and source guard

Read the page's release/introduction date, not just its crawl date or search snippet. During this research the HA LEDVANCE page existed but identified release 2026.11, later than the 2026-10-22 baseline. It was excluded as evidence of already released native support. Apply the same guard to every new product, firmware and integration feature. Retain a promising future route as “announced / not yet verified released,” then recheck when implementation occurs.

Use [community-evidence.md](community-evidence.md) as a starting ledger and [sources.md](sources.md) as source entry points. Refresh the relevant items, not every vendor in the bundle, for each task.
