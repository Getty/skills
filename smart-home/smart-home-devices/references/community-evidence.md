# Firsthand experience ledger

Reviewed 2026-10-22. These are original user reports, not measured failure rates or a representative product survey. They identify conditions worth testing. No case below was reproduced on the user's hardware in this task. Missing firmware/model details remain unknown; repository closure alone is not proof of a fix.

## Contents

- [Interpretation](#interpretation)
- [THIRDREALITY: reporting volume](#thirdreality-reporting-volume)
- [THIRDREALITY: metering](#thirdreality-metering)
- [Tuya TS0201: OTA damage](#tuya-ts0201-ota-damage)
- [Tuya LAN: key handling](#tuya-lan-key-handling)
- [Shelly Flood: local alarm without HA event](#shelly-flood-local-alarm-without-ha-event)
- [Hue Bridge Pro: availability](#hue-bridge-pro-availability)
- [ThermoBeacon: invalid measurements](#thermobeacon-invalid-measurements)
- [Zengge: legacy integration dependency](#zengge-legacy-integration-dependency)
- [SONOFF SNZB-02P: configure failure](#sonoff-snzb-02p-configure-failure)
- [Paulmann 50139: fingerprint mismatch](#paulmann-50139-fingerprint-mismatch)
- [Govee LAN: port conflict](#govee-lan-port-conflict)
- [Aqara: disconnects and conflicting advice](#aqara-disconnects-and-conflicting-advice)
- [MS01: ambiguous product identity](#ms01-ambiguous-product-identity)
- [OSRAM: partial pairing](#osram-partial-pairing)
- [IKEA DIRIGERA: bridge versus Matter sharing](#ikea-dirigera-bridge-versus-matter-sharing)
- [Use and refresh](#use-and-refresh)

## Interpretation

A report can establish that its author encountered a symptom in a stated setup. It cannot establish how common the symptom is, prove the suspected cause, or guarantee that a workaround transfers to another revision. The practical tests below are our synthesis. Read the linked discussion and current release notes before acting.

## THIRDREALITY: reporting volume

- **Source/date:** [Z2M issue 31332](https://github.com/Koenkk/zigbee2mqtt/issues/31332), 2026-03-09.
- **Setup:** twenty `3RSPE01044BZ` plugs; plug firmware 1.01.01; Z2M 2.9.1; SLZB-06M, adapter firmware 8.0.2.
- **Reported behavior:** the owner could reduce reporting while on but described excessive reports while off despite configuration.
- **Outcome/status:** observed open at review; no verified release fix identified in the captured discussion.
- **Practical test:** measure messages from one on and one off plug before a batch firmware rollout. Do not infer that another installation has the same defect or that aggressive interval writes will solve it.

## THIRDREALITY: metering

- **Source/date:** [Z2M issue 29573](https://github.com/Koenkk/zigbee2mqtt/issues/29573), 2025-11-10.
- **Setup:** `3RSPE01044BZ`, firmware 1.00.98; Z2M 2.6.3; Ember adapter firmware 8.2.2.
- **Reported behavior:** dishwasher power was substantially above the owner's independent-meter expectation.
- **Outcome/status:** closed; no applicable confirmed fix established from the captured evidence.
- **Practical test:** compare the same physical load and interval with an appropriate reference. Preserve raw power/voltage/current readings; do not replace metering with an assumed voltage-times-current calculation for every load.

## Tuya TS0201: OTA damage

- **Source/date:** [Z2M issue 25207](https://github.com/Koenkk/zigbee2mqtt/issues/25207), 2024-12-14.
- **Setup:** TS0201; Z2M 1.42.0; SLZB-06 firmware 20230507. The precise retail hardware variant must still be matched.
- **Reported behavior:** after OTA, the display became blank and the device was identified as another model.
- **Outcome/status:** issue closed, but the current [TS0201 device page](https://www.zigbee2mqtt.io/devices/TS0201.html) still carries an explicit harmful-update warning.
- **Practical test:** hold OTA for a matching affected device, inspect the warning and exact image/fingerprint. Do not interpret the closed issue as permission for a fleet update.

## Tuya LAN: key handling

- **Source/date:** [LocalTuya issue 1380](https://github.com/rospogrigio/localtuya/issues/1380), 2023-05-07.
- **Setup:** Smart Life-reactivated devices; exact device model and integration version not given in the report.
- **Reported behavior:** decryption failed after keys with different characters appeared; fetching keys again did not initially resolve it.
- **Outcome/status:** the author reported resolution on 2023-05-08 and linked proposed change 1381 on May 9; closed as completed. Do not infer the precise installed fixed release without inspecting that change.
- **Practical test:** verify actual key, protocol, integration version and key parsing; a “wrong key” message does not by itself prove the key is incorrect. This historical case is not evidence that current LocalTuya still has the bug.

## Shelly Flood: local alarm without HA event

- **Source/date:** [HA issue 124998](https://github.com/home-assistant/core/issues/124998), 2024-08-31.
- **Setup:** original Shelly Flood firmware 1.14.0; HA 2024.8.3.
- **Reported behavior:** the physical device alarmed on water while HA did not receive the expected state update.
- **Outcome/status:** closed with insufficient-information context; no demonstrated universal fix.
- **Practical test:** verify wet and dry transitions, CoIoT peer and sleeping-device event delivery. Device-local audible alarm and a live battery entity do not validate the HA leak notification path.

## Hue Bridge Pro: availability

- **Source/date:** [HA issue 154049](https://github.com/home-assistant/core/issues/154049), 2025-10-09.
- **Setup:** Hue Bridge Pro, HA 2025.10.1; complete light model/firmware inventory not established.
- **Reported behavior:** unavailable/light-state problems persisted despite network/placement changes.
- **Outcome/status:** closed as not planned with stale context; the captured report does not establish a proven cause or firmware fix.
- **Practical test:** distinguish bridge reachability, HA event/state handling and individual light radio behavior. Do not extrapolate this Bridge Pro case to every original Bridge or Hue lamp.

## ThermoBeacon: invalid measurements

- **Source/date:** [HA issue 139972](https://github.com/home-assistant/core/issues/139972), 2025-03-06.
- **Setup:** Brifit-branded sensor through ThermoBeacon; Raspberry Pi 5; HA 2025.3.0, reported previous working 2025.2.5. Exact sensor revision/firmware unknown.
- **Reported behavior:** periodic invalid temperature/humidity values after the upgrade.
- **Outcome/status:** closed as duplicate of issue 139917; this closure does not itself identify the fixed release.
- **Practical test:** compare raw packet/parser and version evidence before discarding a sensor. A successful BLE reception does not guarantee correct decoding.

## Zengge: legacy integration dependency

- **Source/date:** [HA issue 124083](https://github.com/home-assistant/core/issues/124083), 2024-08-16.
- **Setup:** legacy `zengge` YAML path on HA 2024.8.2; exact controller variant not established.
- **Reported behavior:** startup failed around a `bluepy` dependency.
- **Outcome/status:** closed as not planned/stale; no modern-device compatibility conclusion follows.
- **Practical test:** identify the controller's actual protocol and select flux_led, LED BLE or the appropriate custom LEDnetWF route. Do not patch managed HA OS Python packages to preserve an obsolete assumed route.

## SONOFF SNZB-02P: configure failure

- **Source/date:** [Z2M issue 27919](https://github.com/Koenkk/zigbee2mqtt/issues/27919), 2025-07-07.
- **Setup:** SNZB-02P; Z2M 2.5.1, Ember firmware 8.0.2, Raspberry Pi 5. Sensor firmware not established.
- **Reported behavior:** binding/configure-reporting failed with delivery errors.
- **Outcome/status:** closed as not planned with stale context; no verified model-wide fix.
- **Practical test:** capture interview, awake state and route evidence. A paired sensor can still lack configured reports; do not reset every working SONOFF sensor because one reports a configure warning.

## Paulmann 50139: fingerprint mismatch

- **Source/date:** [Z2M issue 26186](https://github.com/Koenkk/zigbee2mqtt/issues/26186), 2025-02-04.
- **Setup:** Paulmann 50139, model `TS000F`, manufacturer signature displayed as `_TZ3210_hjxqqofs�`; installed software version not independently established here. The reporter referenced expected support in 2.1.0.
- **Reported behavior:** interview succeeded but the device was not matched as supported.
- **Outcome/status:** closed; no verified applicable release fix identified in the captured record.
- **Practical test:** preserve raw signature bytes/escaping and compare the installed converter. Removing a seemingly odd character from the fingerprint can hide the actual mismatch.

## Govee LAN: port conflict

- **Source/date:** [HA issue 140100](https://github.com/home-assistant/core/issues/140100), 2025-03-08.
- **Setup:** Govee local integration on HA 2025.3.1; reporter listed 2025.2.x as last working. Exact light model not established.
- **Reported behavior:** UDP port 4002 was already in use.
- **Outcome/status:** closed as not planned/stale; a universal fixed version was not established.
- **Practical test:** identify the actual listener and overlapping integration/container before resetting lamps. Do not assume every failed discovery is Wi-Fi signal loss or unsupported hardware.

## Aqara: disconnects and conflicting advice

- **Source/date:** [HA community thread 751436](https://community.home-assistant.io/t/aqara-sensors-keep-disconnecting/751436), original post 2024-07-19.
- **Setup:** ZHA, Sonoff Zigbee 3.0 stick and several Aqara sensors; exact individual models and firmware not fully specified.
- **Reported behavior:** devices dropped out after days. An unsecured-rejoin suggestion did not solve the original owner's problem, reported 2024-08-13. A different later participant described improvement after deliberate parent selection.
- **Outcome/status:** multiple installations and mixed results, not one confirmed resolution.
- **Practical test:** examine the actual endpoint/parent relationship and repeatable dropout conditions. Do not weaken trust-center policy or publish a universal “bad router” list from this thread.

## MS01: ambiguous product identity

- **Source/date:** [XiaomiGateway3 issue 738](https://github.com/AlexxIT/XiaomiGateway3/issues/738), 2022-04-25.
- **Setup:** a motion device described as MS01/SNZB-03 via XiaomiGateway3; exact versions not established.
- **Reported behavior:** pairing worked but occupancy did not activate, whereas the owner reported operation in Z2M.
- **Outcome/status:** outcome not established in this ledger; used primarily as identity evidence.
- **Practical test:** do not infer the inventory's MS01 is the SONOFF wired soil probe. Check transport, appearance and raw model/manufacturer first.

## OSRAM: partial pairing

- **Source/date:** [Z2M issue 26686](https://github.com/Koenkk/zigbee2mqtt/issues/26686), 2025-03-10.
- **Setup:** OSRAM strip linked to model 4058075036185; Z2M 2.1.1/2.1.3; Dongle-E firmware 7.4.5, Windows x86-64.
- **Reported behavior:** inconsistent interview/configuration; the owner eventually reported success after another restart/reconfigure.
- **Outcome/status:** closed as duplicate of 26692; maintainer suspected the wider network's delivery/interference problem, which the reporter disputed. Device firmware not established.
- **Practical test:** separate endpoint matching, delivery and network interference. This is not proof that all OSRAM hardware is defective or that restarting Z2M is a universal fix.

## IKEA DIRIGERA: bridge versus Matter sharing

- **Source/date:** [HA issue 160196](https://github.com/home-assistant/core/issues/160196), 2026-01-03.
- **Setup:** DIRIGERA; initial reporter HA 2025.6.3 in containers; mixed Zigbee and Matter/Thread children.
- **Reported behavior:** Zigbee children appeared through the Matter bridge; native Matter children did not automatically appear.
- **Outcome/status:** individual device sharing and IPv6 repair helped some participants. Closed as completed by a maintainer on 2026-06-09 as a bridge/sharing distinction; not a universal firmware defect fix.
- **Practical test:** identify whether a device is bridged Zigbee or native Matter and verify its fabric sharing and IPv6 route. Do not count adding a bridge as commissioning every Matter endpoint.

## Use and refresh

Before using a record, confirm model/fingerprint and version overlap with the current task. Open linked follow-ups when the exact fix matters. Add a new dated record if the same model behaves differently with a newer version; preserve the historical conditions instead of replacing them with “works” or “broken.” Keep original reporter identity out of shared inventories unless attribution requires it; source URLs provide provenance.

For a new candidate, seek primary documentation and an original experience report, but do not fabricate missing experience coverage. A vendor with no relevant report found remains unassessed. For more careful comparisons and purchasing output use `procurement-and-community-research.md`.
