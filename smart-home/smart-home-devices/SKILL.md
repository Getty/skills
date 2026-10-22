---
name: smart-home-devices
description: "Use when identifying, choosing, integrating or debugging a specific smart-home product in Home Assistant — Philips Hue, Shelly, THIRDREALITY, Tuya and _TZ Zigbee fingerprints, SONOFF/eWeLink, Zengge, ThermoBeacon, Aqara/Xiaomi, OSRAM/LEDVANCE, Govee, Paulmann, thermostats, plugs, locks, covers, presence sensors, solar, EV chargers."
---

# Smart Home Devices

Build a device-specific integration decision. Identify the physical product before selecting software; measure required behavior before recommending replacement. Treat this collection as a product-family map and an evidence-driven workflow, not an exhaustive SKU database. Research baseline: 2026-10-22. Recheck firmware, supported-device lists, integration alerts, and repository releases before acting.

## Run the workflow

1. Capture the goal, exact label/model, hardware revision, firmware, market region, transport, existing hub, and HA/integration versions. Read [fingerprint-and-routing.md](references/fingerprint-and-routing.md). Preserve raw Zigbee manufacturer/model strings, not just the displayed friendly name.
2. Load only the matching vendor reference and relevant ecosystem reference below. Choose the route that exposes the required capabilities and has an acceptable failure mode; local connectivity alone does not prove cloud independence.
3. Produce a capability matrix for the actual device: command, reported state, event, diagnostics, firmware update, remote operation, and operation during internet/HA/hub failure. Mark each claim verified, reported, inferred, unknown, or unavailable.
4. Inspect the official integration and exact device definition first. Use manufacturer manuals to identify wiring, supply, load ratings, protocol and reset procedure. Review firsthand reports for the same hardware and software combination; read [community-evidence.md](references/community-evidence.md) and [procurement-and-community-research.md](references/procurement-and-community-research.md).
5. Preserve the current working configuration, entity IDs, automations and hub bindings. Pilot one device, including its manual control and recovery path. Do not reset a working fleet to test a theory.
6. Verify state in both directions: HA command → physical effect → observed state, then physical action → HA event/state. Test a realistic failure case and recovery. For battery sensors include a wake/report cycle and a physical stimulus; a successful pairing is insufficient.
7. Return the chosen route, prerequisites, feature losses, exact changes, acceptance evidence, rollback and unresolved questions. If support is unknown, specify the smallest fingerprint or diagnostic needed to resolve it.

## Load vendor references

| Device family or question | Read |
| --- | --- |
| Hue bulbs, strips, dimmers, motion sensors, rooms, Bridge generations | [philips-hue.md](references/philips-hue.md) |
| Shelly Plus Plug S, Flood, relay/meter/generation/API differences | [shelly.md](references/shelly.md) |
| THIRDREALITY 3RSPE01044BZ and other product families | [third-reality.md](references/third-reality.md) |
| Tuya TS0201, TS0203, TS0601, `_TZ…` signatures and data points | [tuya-zigbee.md](references/tuya-zigbee.md) |
| Smart Life/Tuya cloud, LocalTuya, tuya-local, Wi-Fi LAN keys | [tuya-wifi-local-cloud.md](references/tuya-wifi-local-cloud.md) |
| SONOFF SNZB-02P, SNZB-01P, ambiguous MS01, eWeLink and SonoffLAN | [sonoff-ewelink.md](references/sonoff-ewelink.md) |
| Zengge, LEDnet/LEDnetWF, Magic Home, RGB controllers | [zengge-lighting.md](references/zengge-lighting.md) |
| ThermoBeacon, SensorBlue, Bluetooth temperature/humidity sensors | [thermobeacon-and-ble-sensors.md](references/thermobeacon-and-ble-sensors.md) |
| LUMI, Xiaomi, Aqara Zigbee/Thread/HomeKit/MIoT variants | [aqara-xiaomi-lumi.md](references/aqara-xiaomi-lumi.md) |
| OSRAM, LIGHTIFY and LEDVANCE SMART+ variants | [osram-ledvance.md](references/osram-ledvance.md) |
| Govee lights, sensors, LAN/BLE/cloud/Matter paths | [govee.md](references/govee.md) |
| Paulmann smik, Plug & Shine, URail, LED controllers | [paulmann.md](references/paulmann.md) |

## Load broader market references

| Task | Read |
| --- | --- |
| Bosch, Homematic IP, tado, Netatmo, Daikin, Mitsubishi, heating and AC | [heating-hvac-ecosystems.md](references/heating-hvac-ecosystems.md) |
| IKEA, Nanoleaf, Eve, SwitchBot, Nuki, Yale, Somfy and covers | [lighting-locks-covers-ecosystems.md](references/lighting-locks-covers-ecosystems.md) |
| Tapo/Kasa, Meross, BSH Home Connect, LG ThinQ, Miele, Samsung, Roborock, Dreame, Ecovacs and garden | [plugs-appliances-cleaning-garden.md](references/plugs-appliances-cleaning-garden.md) |
| Meters, solar, batteries, chargers, Fronius, SMA, Powerwall and evcc | [energy-ev-solar.md](references/energy-ev-solar.md) |
| PIR/mmWave, presence zones, air quality and safety sensors | [presence-air-quality-safety.md](references/presence-air-quality-safety.md) |
| Exact-model buying research, Amazon variants, user experience quality | [procurement-and-community-research.md](references/procurement-and-community-research.md) |
| Dated firsthand issue records and their practical implications | [community-evidence.md](references/community-evidence.md) |
| Source hierarchy, refresh policy and primary-source entry points | [sources.md](references/sources.md) |

## Observe the known traps

- Treat a user-provided inventory as a report, not an HA export. Hue rooms can be logical groups; a count of Hue entries does not establish that many radios.
- Keep the exact THIRDREALITY identifier `3RSPE01044BZ`. A neighboring plug model is not interchangeable evidence.
- Do not classify `TS0601` devices by that shared model string. Require manufacturer fingerprint and exposed functions.
- Hold TS0201 OTA when the exact matching device page carries its known bad-image warning. See the Tuya reference before any update.
- Resolve `MS01` using its transport and physical form: the name appears in unrelated sensor contexts.
- Distinguish original Shelly Flood, later Flood generations and BLU sensors; sleep and event delivery differ.
- Do not choose an LED protocol from the Zengge logo or app name alone.
- Never promote an issue closure to proof of a firmware fix. Do not infer product failure rates from complaint counts.

## Route adjacent work

Use `fritzbox-operator` for FRITZ!Box, DECT thermostats, Control 440, AHA/TR-064 and cable-provider restrictions. Use `smart-home-radio` for coordinator, Zigbee mesh, Thread and BLE transport. Use `smart-home-video-media` for Reolink, NVRs, Ring/Blink/Eufy, Fire TV, LG TVs and video streams. Use `home-assistant-hacs` for installing custom code; `home-assistant-automations` for cross-vendor control logic; `smart-home-esphome-mqtt` for device firmware and MQTT. Keep vendor commissioning credentials and local keys out of shared reports.

Use [device-fingerprint.yaml](assets/device-fingerprint.yaml) and [capability-review.yaml](assets/capability-review.yaml) as task-local templates. Record only the fields needed for the task; do not gather household identities or network secrets unnecessarily.
