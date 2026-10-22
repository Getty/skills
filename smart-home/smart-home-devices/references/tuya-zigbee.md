# Tuya Zigbee: TS0201, TS0203 and TS0601

## The model string is only one key

Many white-label Tuya products reuse `TS0601` while implementing unrelated functions and data points. Match `modelID` plus exact manufacturer string such as `_TZE200_…`, `_TZE204_…`, `_TZ3000_…` or another observed value, endpoint/cluster signature and firmware. The retail brand, app and case shape are useful clues, not a converter definition. [Zigbee2MQTT Tuya developer guide](https://www.zigbee2mqtt.io/advanced/support-new-devices/02_support_new_tuya_devices.html).

| Model string | Initial hypothesis | What must be verified |
| --- | --- | --- |
| TS0201 | Temperature/humidity family, possibly with display | Full fingerprint, actual selected definition, battery/reporting behavior and OTA eligibility |
| TS0203 | Door/window contact family | Contact polarity, tamper/battery features, manufacturer variant |
| TS0601 | Undetermined | Do not label these as thermostats, presence sensors or switches until signature and capabilities are observed |
| Plugs and lights | Multiple product families | Metering, dimming/color modes, endpoint layout, power-on behavior and safe load rating |

The exact TS0201 page exposes temperature, humidity, battery and voltage. The TS0203 page exposes contact, battery, voltage, tamper and low-battery. A converter's contact `true` can mean physically closed even where HA's opening binary sensor displays `off`; test physical open/closed transitions before heating or alarm use. [TS0201](https://www.zigbee2mqtt.io/devices/TS0201.html), [TS0203](https://www.zigbee2mqtt.io/devices/TS0203.html).

## Specific OTA hold

As checked on 2026-10-22, the TS0201 device page contains an explicit warning about a bad available firmware image. The linked firsthand report, opened 2024-12-14 on Z2M 1.42.0, describes a blank display and misidentification as LYWSD03MMC after update. The issue is closed, but the device-page warning remains. **Do not update a matching TS0201 just because OTA is advertised.** Require a verified correct image and a resolved warning for that hardware before proceeding. This hold is specific; it is not a claim that all Tuya updates are unsafe. [Issue 25207](https://github.com/Koenkk/zigbee2mqtt/issues/25207).

## Data-point investigation

For an unsupported device, capture diagnostics without changing device state first. Observe a physical action or a safe vendor operation, record the resulting data point, raw type, scale, unit and timing. Repeat with an independent value. Label a guessed interpretation as a hypothesis; never write speculative temperature, valve, calibration, relay or protection data points.

Keep separate mappings for each fingerprint. Do not copy a TS0601 thermostat converter onto a superficially similar presence device. If creating a converter or ZHA quirk, use the matching project's current development guide and test it against captured fixtures before installing it. Include original signature, firmware, observed payloads and expected semantics in a support report.

## Battery sensors and radio diagnosis

Keep devices awake only through their documented short interaction while commissioning/configuring; do not continuously poll sleepy sensors. Test report freshness with physical change, not only a stored state. A missing battery percentage shortly after pairing can be a reporting delay rather than a failed interview. Preserve stale/unavailable distinctions in automations.

Do not switch ZHA ↔ Z2M to work around a single missing attribute before comparing the exact support entries and considering migration cost. Read `smart-home-radio` for coordinator, interference, routers, backups and re-pairing.

## Product-family expansion

Treat Tuya as a platform across thermostats, metering plugs, switches, curtains, locks, sensors, IR controllers, lamps and appliances. For every family ask whether this particular product is Zigbee, Wi-Fi, BLE or Matter. A Smart Life account is unnecessary for direct Zigbee operation through a supported coordinator, but vendor-specific firmware, scenes or optional features may be lost. Record those differences explicitly.
