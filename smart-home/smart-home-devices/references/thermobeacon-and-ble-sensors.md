# ThermoBeacon and Bluetooth environmental sensors

## Range and route map

Most BLE climate sensors broadcast non-connectable advertisements that HA parses through the Bluetooth integration. A sensor is identified by its advertisement (service-data UUID, manufacturer ID or local name), not by its retail label. Matchers below come from the HA integration manifests (checked 2026-10).

| Brand / family | Advertising format and matcher | HA route | Caveat |
| --- | --- | --- | --- |
| ThermoBeacon / SensorBlue WS03, WS07, WS08 | Proprietary: service UUID `0xFFF0` + manufacturer IDs 16, 17, 20, 21, 24, 27, 48, or local name `ThermoBeacon` | `thermobeacon` | Sold under other labels; Brifit is reported. Only 20-byte frames carry measurements; 22-byte frames are other data ([HA ThermoBeacon](https://www.home-assistant.io/integrations/thermobeacon/), [parser](https://github.com/Bluetooth-Devices/thermobeacon-ble)) |
| Xiaomi Mijia stock firmware: `LYWSD03MMC`, `LYWSDCGQ`, `LYWSD02MMC`, `MJWSD05MMC`, `MJWSD06MMC`, `XMWSDJ04MMC`; Miaomiaoce `MHO-C401`; Qingping-for-Mijia `CGG1`, `CGDK2` | MiBeacon service data `0xFE95`. v2/v3 use a 24-hex key; v4/v5 use a 32-hex authenticated key | `xiaomi_ble`; for v4/v5 it can import the bindkey from the bound Xiaomi account | No BLE Mesh support. Some entities, such as battery, appear only after the first matching broadcast ([HA Xiaomi BLE](https://www.home-assistant.io/integrations/xiaomi_ble/)) |
| Telink models flashed with pvvx/ATC firmware | Selectable: Mi-like MiBeacon (optionally encrypted), BTHome v2, ATC1441 (`0x181A`), pvvx Custom (`0x181A`) | BTHome v2 → `bthome`; MiBeacon → `xiaomi_ble`. `0x181A` formats need Passive BLE Monitor (HACS); ESPHome `atc_mithermometer` parses ATC1441 only | The device disappears from Mi Home after flashing. LYWSD03MMC needs >40% battery to flash. pvvx advises against buying LYWSD03MMC HW B1.5/B1.6 (sold since 2025-03) and documents a special first OTA for B1.6 ([pvvx README](https://github.com/pvvx/ATC_MiThermometer)) |
| BTHome devices: Shelly BLU H&T, BLU Door/Window, BLU Button; DIY sensors | BTHome v2, service data `0xFCD2`. v1 (`0x181C`/`0x181E`) has been deprecated since 2022-11 | `bthome`; enter a 32-hex bindkey if encryption is on | The Shelly integration does not handle BLU sensors (only BLU TRV, through a gateway). BLU H&T is rated 10 m indoors and 30 m outdoors ([BTHome](https://bthome.io/), [Shelly BLU H&T](https://kb.shelly.cloud/knowledge-base/shelly-blu-h-t)) |
| Govee H5xxx thermo-hygrometers (H5051–H5179) and sensors/buttons | Proprietary; local names `GVH5*`, `Govee*`, `GV51xx*` | `govee_ble` | H5074, H5075 and H5129 require active scans. Wi-Fi/cloud/Matter models: see [govee.md](govee.md) ([HA Govee BLE](https://www.home-assistant.io/integrations/govee_ble/)) |
| Inkbird IBS-TH1/TH2, ITH-11-B/13-B/21-B, IBS-P01B, IAM-T1/T2, BBQ probes | Proprietary; names such as `Inkbird*`, `sps`, `tps`, `ITH-*` | `inkbird` | Most models need active scans to be discovered, and battery needs active scans. IAM-T1/T2 use connectable advertisements. IAM-T1 can show stale readings ([HA INKBIRD](https://www.home-assistant.io/integrations/inkbird/)) |
| SwitchBot Meter, Meter Plus, Indoor/Outdoor Meter, Meter Pro, Meter Pro CO2 | Proprietary; service data `0xFD3D`, manufacturer ID 2409 | `switchbot` (Bluetooth, no hub needed) | With a passive-mode adapter, devices are not discovered locally; sync them through the SwitchBot account ([HA SwitchBot](https://www.home-assistant.io/integrations/switchbot/)) |
| Qingping CGG1/CGG3, CGDN1, CGP1W, CGP22C, CGP23W, CGF1W, CGM1, CGD1, CGC1, CGH1, CGPR1 | Qingping service data `0xFDCD` | `qingping` (passive, no cloud) | CGG1 and CGDK2 also exist as Mijia variants that use MiBeacon. Check the UUID to pick between `qingping` and `xiaomi_ble` ([HA Qingping](https://www.home-assistant.io/integrations/qingping/)) |
| Ruuvi RuuviTag, RuuviTag Pro, Ruuvi Air | Manufacturer ID 1177 (`0x0499`) | `ruuvitag_ble`; Ruuvi Air since HA 2025.11 | If a tag is not discovered, update its firmware ([HA Ruuvi BLE](https://www.home-assistant.io/integrations/ruuvitag_ble/)) |
| SensorPush HT1, HT.w, HTP.xw | Proprietary; local name `SensorPush*` | `sensorpush` | Entities appear only after the device is activated in the SensorPush app ([HA SensorPush](https://www.home-assistant.io/integrations/sensorpush/)) |
| BlueMaestro Tempo Disc THD/THPD | Proprietary | `bluemaestro` | Only the listed models ([HA BlueMaestro](https://www.home-assistant.io/integrations/bluemaestro/)) |
| Airthings air-quality sensors | Bluetooth mode or SmartLink | `airthings_ble` | Needs active connections for local readings; SmartLink mode is a different route ([HA Airthings BLE](https://www.home-assistant.io/integrations/airthings_ble/)) |
| Sensirion gadgets | Proprietary | `sensirion_ble` | Some listed models are marked untested ([HA Sensirion BLE](https://www.home-assistant.io/integrations/sensirion_ble/)) |

Rules:
- An unknown sensor is not automatically unsupported. First capture its advertisement (UUID, manufacturer ID, name) and match it against the manifests.
- Re-flashing or switching the advertising format moves the device to a different integration, which gives it new entities.
- For a Xiaomi device, record its hardware revision as well as its model.

## Receivers and scanning

- HA's Bluetooth integration offers **Auto**, **Active** and **Passive** scanning modes:
  - Passive saves sensor battery, but some integrations need active scans.
  - Auto and Passive need an adapter that supports passive scanning; on Linux that means BlueZ 5.63+ with experimental features (HAOS 9.4+).
  - Auto falls back to Active where passive scanning is unsupported.

  [HA Bluetooth](https://www.home-assistant.io/integrations/bluetooth/).
- ESPHome Bluetooth proxies forward advertisements from firmware 2022.8.2 and bundle them from 2023.6.0. They can also make active connections. Space multiple proxies apart so they do not interfere.
- Shelly Gen2+ mains devices can proxy advertisements (active or passive) but not GATT connections ([HA Shelly](https://www.home-assistant.io/integrations/shelly/)).
- The pvvx README claims that ESP32/ESPHome receivers miss packets and that Passive BLE Monitor cannot receive BT5 LE Long Range. This is the firmware author's position and conflicts with HA guidance. Test with the actual receiver, and keep legacy 1M advertising unless the whole chain is shown to receive Coded PHY.
- Advertisements and active GATT connections have different resource and range needs. Use `smart-home-radio` for receiver placement and proxy design; one adapter in a metal server cabinet will not cover a house.

## Diagnose the observation chain

1. Record the local display or a reference reading, with time and placement.
2. Verify Bluetooth receiver health and whether the raw advertisement is visible.
3. Determine whether the advertisement is parsed into the expected HA sensor, and by which integration.
4. Compare HA last-update time, value and availability. A stored number can legitimately stay unchanged, or it can be stale.
5. Move one test receiver or sensor temporarily to separate range problems from parsing problems.
6. Apply a physical stimulus and test recovery after an HA restart, then restore normal placement.

Do not change sensor firmware, integration and receiver at the same time. "Nearby Bluetooth devices detected" does not prove that this sensor's packets were received. A sensor can send identity or battery frames more often than measurement frames.

## Calibration and automation

Use a stable comparison interval and similar placement before setting an offset. When the goal is room temperature, keep the sensor away from sun, radiators, electronics and drafts. Preserve raw data while investigating spikes, and do not hide a parsing problem behind aggressive smoothing. Automations that control heating or ventilation need freshness and plausibility bounds, plus a fallback for when no valid measurement arrives.

Temperature and humidity do not establish mold, CO2, occupancy or air safety; measure those quantities separately. Displayed decimal precision is not sensor accuracy.

## Worked example: parser regression after an upgrade

A report opened **2025-03-06** described periodic invalid ThermoBeacon values after moving from HA **2025.2.5** to **2025.3.0**, using a Brifit-branded device and Raspberry Pi 5 Bluetooth. It was closed as a duplicate of root issue 139917. That issue was fixed by bumping `thermobeacon-ble` to 0.8.1 (a revert of 18-byte frame handling), shipped in HA **2025.3.1**. [Core issue 139972](https://github.com/home-assistant/core/issues/139972), [root issue 139917](https://github.com/home-assistant/core/issues/139917), [fix PR 139919](https://github.com/home-assistant/core/pull/139919).

When an upgrade lines up with a measurement fault, compare the parser change and the raw packets before buying new sensors. Follow the root issue to the release that carries the fix, and record "unknown" where the fix version is not established.
