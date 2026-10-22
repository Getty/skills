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
| Hue bulbs/strips/luminaires (LCT/LCA/LTW/LWB… modelIDs), Essential, Bridge v1/v2/Pro (BSB00x), dimmers/Tap dial/buttons/wall modules, motion/contact sensors, MotionAware, Hue Secure cameras, Sync Box, Hue BLE, Hue Matter/Thread | [philips-hue.md](references/philips-hue.md) |
| Any Shelly: Gen1/Plus/Pro/Gen3/Gen4, BLU, Wave, Wall Display; model codes SH…/SN…/SP…/S3…/S4…/SB…/QN…; Plug S, Flood, 1PM, 3EM, Zigbee/Matter mode | [shelly.md](references/shelly.md) |
| THIRDREALITY plugs (E2 3RSPE01044BZ, Gen3/E3), sensors, lights, blinds, Matter Wi-Fi/Thread lines, MZ1 bridge, 3R… IDs | [third-reality.md](references/third-reality.md) |
| Tuya Zigbee `TSxxxx` model IDs, `_TZ3000_`/`_TZE2xx_` prefixes, 0xEF00 data points, TS0601 | [tuya-zigbee.md](references/tuya-zigbee.md) |
| Tuya Wi-Fi/BLE white-label, Smart Life cloud, LocalTuya, tuya-local, protocol 3.1–3.5, local keys, BK72xx/RTL reflash, cloudcutter | [tuya-wifi-local-cloud.md](references/tuya-wifi-local-cloud.md) |
| SONOFF SNZB/ZBMINI/ZBM5/TRVZB Zigbee, Wi-Fi BASIC/MINI/POW/TH/NSPanel, Matter lines, dongles, iHost, MS01, eWeLink/SonoffLAN | [sonoff-ewelink.md](references/sonoff-ewelink.md) |
| Zengge/Surplife OEM: Magic Home, Magic Hue, LEDnet/LEDnetWF, Hao Deng mesh, AK001-ZJ modules, reflash | [zengge-lighting.md](references/zengge-lighting.md) |
| ThermoBeacon, Xiaomi MiBeacon, pvvx/ATC, BTHome/Shelly BLU, Govee, Inkbird, SwitchBot, Qingping, Ruuvi BLE sensors | [thermobeacon-and-ble-sensors.md](references/thermobeacon-and-ble-sensors.md) |
| Aqara/Xiaomi `lumi.*` Zigbee, Aqara hubs, Thread/Matter, FP2, Xiaomi gateways, MIoT Wi-Fi, model-code lookup | [aqara-xiaomi-lumi.md](references/aqara-xiaomi-lumi.md) |
| OSRAM LIGHTIFY (ZLL, gateway), SMART+ Zigbee (Z3/“T” modelIDs, 4058075… EANs), SYLVANIA US, SMART+ Wi-Fi/SUN@HOME (Tuya), SMART+ Bluetooth/HomeKit, SMART+ Matter over Wi-Fi, OSRAM IR remote lamps | [osram-ledvance.md](references/osram-ledvance.md) |
| Govee H-numbers: strips, neon, bars, lamps, bulbs, outdoor, TV sync, BLE sensors, leak, appliances; LAN/BLE/cloud/Matter | [govee.md](references/govee.md) |
| Paulmann Zigbee 3.0, smik gateway, Plug & Shine, URail, remotes, Bluetooth line, article numbers | [paulmann.md](references/paulmann.md) |

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
