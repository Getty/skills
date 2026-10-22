# Tuya Zigbee: model IDs, manufacturer prefixes and data points

## Identity is model ID plus manufacturer string

A Tuya Zigbee device reports a `TSxxxx` model ID and a manufacturer string such as `_TZ3000_abcd1234`. The model ID names a device class at best; the same ID spans unrelated products and brands. Match `modelID` + exact `manufacturerName` + endpoint/cluster signature + firmware; the retail brand, app and case shape are clues, not a converter definition. Zigbee2MQTT therefore matches Tuya devices by fingerprint, not by `zigbeeModel`. [Z2M Tuya developer guide](https://www.zigbee2mqtt.io/advanced/support-new-devices/02_support_new_tuya_devices.html), [Z2M Tuya converters](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/tuya.ts). White-label definitions also live in vendor files (`moes.ts`, `lidl.ts`, `avatto.ts`, `zemismart.ts`, `girier.ts`, …): search the whole `src/devices/` tree for the exact manufacturer string.

## Manufacturer prefixes

The prefix meanings below are an observed convention in the Z2M and ZHA definitions (as of 2026-10), not a published Tuya specification. Always confirm with the cluster list in the device signature.

| Prefix | Usually seen on | Protocol behaviour | Implication |
| --- | --- | --- | --- |
| `_TZ3000_` (most common), `_TZ3210_`, `_TZ3002_`, `_TZ3040_`, `_TZ3290_`, `_TZB210_`, `_TYZB01_` (older) | ZCL-style model IDs: TS000x/TS001x/TS0726 switches, TS011F plugs, TS02xx sensors, TS004x buttons, TS05xx/TS110E lights, TS1201 IR (`_TZ3290_`) | Standard ZCL clusters, often plus Tuya attributes on `0xE000`/`0xE001` or extra Tuya settings | Basic function often works without a quirk; Tuya extras (power-on state, indicator, child lock, switch type) need the converter/quirk. Some firmware only reports after a "magic packet" (Z2M `configureMagicPacket`, ZHA `tuya_enchantment`: read of Basic attributes incl. `0xFFFE`) |
| `_TZE200_`, `_TZE204_`, `_TZE284_` (+ rare `_TZE210_`, `_TZE20C_`, `_TZE608_` …) | Almost always `TS0601`; exceptions exist (some TS0201, TS0222, TS0301, TS110E) | Zigbee module tunnels the product MCU's **data points (DPs)** over private cluster `0xEF00` (`manuSpecificTuya`) | Nothing works without a definition that maps DPs; DP numbers and scaling differ per product. `_TZE284_` strings often join an existing `_TZE200_`/`_TZE204_` definition as a newer hardware revision, but not always |

Tuya documents DPs ≤100 as standard and 101–255 as vendor-custom, with Boolean, value, enum, string, bitmap and raw types, carried on cluster `0xEF00`. [Tuya: Zigbee sub-device custom DPs](https://support.tuya.com/en/help/_detail/Kdah1urvujsay), [zigbee-herdsman cluster `manuSpecificTuya` 0xEF00](https://github.com/Koenkk/zigbee-herdsman/blob/master/src/zspec/zcl/definition/cluster.ts), [ZHA Tuya cluster IDs](https://github.com/zigpy/zha-device-handlers/blob/dev/zhaquirks/tuya/__init__.py).

## Product range by model ID

Classes verified against Z2M definition descriptions; "ZHA quirk" means a file in [`zhaquirks/tuya/`](https://github.com/zigpy/zha-device-handlers/tree/dev/zhaquirks/tuya) names that model ID. "No quirk" means ZHA relies on standard ZCL handling — test, do not assume full parity.

| Model ID | Device classes (Z2M descriptions) | Protocol | HA route | Key caveat |
| --- | --- | --- | --- | --- |
| TS0001–TS0004, TS0006, TS000F | 1–6 gang switch modules/relays with neutral, wall switches; TS0001 also valves, fingerbot, thermostat switch | ZCL On/Off + Tuya attributes | Z2M; ZHA quirk (`ts000x`, `ts000f_switch`, `ts0001_switch`) | Power-on state, switch type and backlight are Tuya extras; mains devices route |
| TS0011–TS0014 | 1–4 gang switches/modules **without neutral** | ZCL On/Off | Z2M; ZHA quirk (`ts001x`) | No-neutral units usually do not route; minimum-load flicker with LEDs |
| TS0726 | Newer multi-gang wall switches with backlight/scenes (`_TZ3002_`) | ZCL | Z2M; verify ZHA | Scene buttons may need converter support |
| TS011F | Plugs (with/without metering), in-wall outlets, power strips, DIN relays, valves | ZCL On/Off + metering + Tuya attributes | Z2M; ZHA quirk (`ts011f_plug`, `ts011f_switch`) | Firmware ≥1.0.5 on the common plug stopped reporting power/voltage/current — Z2M polls (`measurement_poll_interval`); some variants report metering unreliably. Router quality varies by unit — check routing/LQI before relying on one for the mesh |
| TS0121 | 10 A UK / 16 A EU metering plug | ZCL | Z2M; ZHA quirk (`ts0121_plug`) | Check rated load against the actual appliance |
| TS0201 | Temp/humidity (with/without display, illuminance, probe) | ZCL (most); a few `_TZE200_` DP variants | Z2M; ZHA quirk (`ts0201`) | Bad-OTA warning on the Z2M TS0201 page — see worked example |
| TS0222 | Light (lux) sensors, some temp/humidity/flower sensors | ZCL; one `_TZE204_` variant | Z2M; no ZHA quirk | Lux scaling differs by variant |
| TS0202, TS020C | PIR motion (some with lux or scene switch); also listed: a temp/humidity sensor, a 24 GHz presence sensor | ZCL IAS Zone | Z2M; ZHA quirk for some (`tuya_motion`) | Occupancy timeout often fixed in hardware |
| TS0203 | Door/window contact; also listed: pressure pad, temp/humidity | ZCL IAS Zone | Z2M; no ZHA quirk | Contact polarity — see worked example |
| TS0207 | Water leak detector; also listed: repeater, solar rain sensor | ZCL IAS (leak) | Z2M; ZHA rain quirk only | Same ID covers a mains repeater and a battery sensor |
| TS0204, TS0205, TS0210 | Gas, smoke, vibration | ZCL IAS | Z2M; ZHA quirk for TS0205, TS0210 | Safety devices: not a substitute for certified alarms |
| TS0215A, TS0218 | SOS button / security remote, single button | ZCL IAS ACE emergency command | Z2M; no ZHA quirk | Confirm action events, not only battery |
| TS0216, TS0224 | Sirens | TS0224 ZCL IAS WD; TS0216 Tuya-specific siren converter | Z2M | Test volume/duration control |
| TS0225 | Human presence sensor | DP (`0xEF00`) plus IAS occupancy | Z2M; ZHA quirk (`tuya_motion`) | Tuning parameters differ from TS0601 radars |
| TS0041–TS0046, TS0021, TS0026 | 1–6 button scene remotes/wall scene switches | Tuya-specific action command on the On/Off cluster | Z2M; ZHA quirks (`ts0041`…`ts0046`) | Single/double/hold support per variant |
| TS004F | 4/6-button remotes, dimming remote, rotary knob | ZCL commands; `operation_mode` command ↔ event | Z2M; ZHA quirk (`ts004f`) | Mode switch changes which actions exist |
| TS0501–TS0505 (A/B), TS0901 | Dimmable, CCT, RGB, RGBW, RGB+CCT bulbs and LED controllers | ZCL lighting | Z2M; mostly no ZHA quirk (TS0501B quirk) | Colour modes, power-on behaviour, transitions vary |
| TS110E, TS110F, TS1101, TS0052 | Dimmer modules (incl. no-neutral, 0–10 V) | ZCL Level + Tuya attributes | Z2M; ZHA quirk (`ts110e`) | Min/max brightness and load type are Tuya attributes |
| TS130F, TS0301, TS030F | Curtain/blind switch modules and motors | ZCL Window Covering (+ Tuya); some TS0301 are `_TZE2xx_` DP | Z2M; ZHA quirk (`ts130f`) | Calibration and direction reversal; verify reported position |
| TS0049, TS0111 | Water valves, irrigation timers (TS0111 also sockets) | TS0049 DP; TS0111 ZCL On/Off | Z2M; ZHA `tuya_valve` covers TS0049 | Battery valves: confirm fail state |
| TS1201 | IR blaster (`_TZ3290_`) | Zosung IR clusters | Z2M | Code learning via converter only |
| TS0601 | Generic DP device: switches, TRVs/thermostats, energy meters/breakers/RCBOs, mmWave/PIR presence, curtain motors, smoke/gas/CO, air quality, temp/humidity/soil, dimmers, valves, sirens, level sensors, garage openers, feeders, locks… | `0xEF00` DPs | Z2M (hundreds of fingerprints); ZHA quirks (`ts0601_*`, `tuya_*`, quirks-v2 `TuyaQuirkBuilder`); Tuya gateway + cloud integration | Unsupported fingerprint = no entities. Radars and air-quality units can flood the network; Z2M `throttle`/`debounce` exist for such devices |

[Z2M device options (`throttle`, `debounce`)](https://www.zigbee2mqtt.io/guide/configuration/devices-groups.html), [TS011F plug notes](https://www.zigbee2mqtt.io/devices/TS011F_plug_1.html).

### Other routes

- **Tuya Zigbee gateway → official Tuya integration**: cloud push, entities limited to what the Tuya SDK exposes; see [tuya-wifi-local-cloud.md](tuya-wifi-local-cloud.md).
- **Tuya Matter gateways** (e.g. Smart Wired Gateway Pro, CSA-listed as Aggregator/bridge, device type `0x000E`) bridge Zigbee sub-devices to Matter. Bridged device types and attributes are a subset; verify per class before choosing it over a coordinator. [CSA listing](https://csa-iot.org/csa_product/smart-wired-gateway-pro-3/).
- A Smart Life account is unnecessary for direct operation through a supported coordinator; vendor scenes, gateway-only features and Tuya-cloud OTA are lost. Record those differences.

## Worked example: TS0201 temperature/humidity and its OTA hold

The exact TS0201 page (BlitzWolf BW-IS4 white label) exposes temperature, humidity, battery and voltage. Other TS0201 fingerprints map to different definitions (display, lux, probe); confirm which one was selected. [TS0201](https://www.zigbee2mqtt.io/devices/TS0201.html).

As checked on 2026-10-22 the page states that the latest available firmware bricks the device and must not be applied. The linked firsthand report, opened 2024-12-14 on Z2M 1.42.0, describes a blank display and misidentification as LYWSD03MMC after update; the issue is closed, the warning remains. **Do not update a matching TS0201 because OTA is advertised.** Require a verified correct image and a resolved warning for that hardware. This hold is specific; it is not a claim that all Tuya updates are unsafe. [Issue 25207](https://github.com/Koenkk/zigbee2mqtt/issues/25207).

## Worked example: TS0203 contact polarity

The TS0203 page exposes contact, battery, voltage, tamper and low-battery. A converter's contact `true` can mean physically closed even where HA's opening binary sensor displays `off`; test physical open/closed transitions before heating or alarm use. [TS0203](https://www.zigbee2mqtt.io/devices/TS0203.html).

## Worked example: TS0601 data-point devices

Do not label a TS0601 as thermostat, presence sensor or switch until signature and capabilities are observed. For an unsupported device, capture diagnostics without changing device state first. Observe a physical action or a safe vendor operation; record DP number, raw type, scale, unit and timing (Z2M debug logs show `Datapoint 'N' with value 'V' not defined`). Repeat with an independent value. Label a guessed interpretation as a hypothesis; never write speculative temperature, valve, calibration, relay or protection DPs.

Keep separate mappings per fingerprint. Do not copy a TS0601 thermostat converter onto a superficially similar presence device. For a converter or ZHA quirk use the project's current guide (Z2M external converter; ZHA quirks v2 `TuyaQuirkBuilder`) and test against captured fixtures before installing. Include original signature, firmware, observed payloads and expected semantics in a support report.

## Battery sensors and radio diagnosis

Keep devices awake only through their documented short interaction while commissioning/configuring; do not continuously poll sleepy sensors. Test report freshness with a physical change, not a stored state. A missing battery percentage shortly after pairing can be a reporting delay rather than a failed interview. Preserve stale/unavailable distinctions in automations.

Do not switch ZHA ↔ Z2M to work around a single missing attribute before comparing the exact support entries and the migration cost. Read `smart-home-radio` for coordinator, interference, routers, backups and re-pairing.
