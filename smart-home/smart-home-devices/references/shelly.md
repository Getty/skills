# Shelly: product lines, generations, APIs and HA routes

Research baseline 2026-10-22. Shelly ships the same product name across generations (Plug S, H&T, Flood, 1PM, i4), so identify the line before you apply any instructions. Line lists: KB [Gen1](https://kb.shelly.cloud/knowledge-base/shelly-gen1-devices), [Plus](https://kb.shelly.cloud/knowledge-base/shelly-plus-devices), [Pro](https://kb.shelly.cloud/knowledge-base/shelly-pro-devices), [Gen3](https://kb.shelly.cloud/knowledge-base/shelly-gen3-devices), [Gen4](https://kb.shelly.cloud/knowledge-base/shelly-gen4-devices), [BLE](https://kb.shelly.cloud/knowledge-base/shelly-ble-devices), [Wave](https://kb.shelly.cloud/knowledge-base/shelly-wave-devices), [displays](https://kb.shelly.cloud/knowledge-base/shelly-control-panels). Per-device API pages: [Gen2+ docs](https://shelly-api-docs.shelly.cloud/gen2/), [BLU docs](https://shelly-api-docs.shelly.cloud/docs-ble/).

## Product range

| Line | Device classes (KB/API listings) | Radio | API | HA route | Key caveat |
| --- | --- | --- | --- | --- | --- |
| Gen1 (legacy) | 1, 1PM, 1L, 2, 2.5, i3, Uni, EM, 3EM, Plug, Plug S, Plug E, Plug US, Dimmer 1/2, RGBW2, Bulb/Duo/Vintage/Bulb RGBW, Button1, H&T, Flood, Door/Window 1/2, Motion 1/2, Gas, Smoke, TRV, 4Pro, Sense | Wi-Fi | [Gen1 HTTP](https://shelly-api-docs.shelly.cloud/gen1/), CoIoT (CoAP), MQTT | Native `shelly` (fw ≥1.9; DUO, Bulb RGBW, Dimmer, Dimmer 2, RGBW2, Vintage ≥1.11) | Needs CoIoT, see below. 4Pro and Sense are unsupported in HA. The latest Gen1 API changelog entry is v1.14.0 (2023-08-09) |
| Gen2 Plus | Plus 1/1PM/2PM (+UL), Plus 1/1PM/PM Mini, i4, i4DC, Uni, 0-10V Dimmer, Wall Dimmer (US), RGBW PM, Plug S V1/V2, Plug IT/UK/US, H&T, Smoke | Wi-Fi, BLE | Gen2 RPC over HTTP/WebSocket/MQTT, scripts | Native | Many models are feature-frozen at 1.7.x (see Gen2+) |
| Gen2 Pro (DIN rail) | Pro 1/1PM/2/2PM/3/4PM, Dual Cover/Shutter PM, Dimmer 1PM/2PM/0-1-10V PM, RGBWW PM, Pro 1–4CB circuit breakers, LAN Switch | Ethernet, Wi-Fi, BLE | RPC; KNX on relays/dimmers; BTHome and virtual components (fw ≥1.4.0) | Native | Ethernet is usable for HA. Check per-channel and total load ratings |
| Pro meters | Pro 3EM, Pro 3EM-400, Pro 3EM-3CT63, Pro EM-50 | Ethernet, Wi-Fi, BLE | RPC `EM`/`EMData` | Native | Check the CT clamp range against the main fuse |
| Gen3 | 1, 1PM, 2PM, 1L/2L, i4/i4DC, 1/1PM/PM Mini, Dimmer, Dimmer 0/1-10V PM, DALI Dimmer, Shutter, EM, 3EM-63, Plug S MTR, Plug M, Plug PM, Outdoor Plug S, AZ Plug, Plug CN, H&T, Duo Bulb E27, Multicolor Bulb E27, BLU Gateway Gen3, The Pill, Camera | Wi-Fi, BLE; Matter over Wi-Fi on many models | RPC; virtual components fw ≥1.2.0; KNX on relays/dimmers/Shutter | Native, or Matter | Matter is per model and often has to be enabled in the web UI ([KB](https://kb.shelly.cloud/knowledge-base/setting-up-gen3-devices-via-matter)). Shelly AZ H&T is unsupported in HA |
| Gen4 (multiprotocol) | 1, 1PM, 2PM (+ANZ), 1L/2L, i4, 1/1PM Mini, EM, EM Mini, Dimmer (EU), Dimmer US, Dimmer 0/1-10V PM, Plug US, Power Strip 4, Flood, Flood S, Presence (mmWave, USB-C) | Wi-Fi, BLE, Zigbee 3.0; Matter on most (not i4, EM, EM Mini) | RPC in Wi-Fi mode; [Zigbee component](https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Zigbee) | Native, Matter, or Zigbee via Z2M (ZHA: verify) | Matter (default) and Zigbee are firmware profiles, see Gen4 below |
| BLU (BLE only) | Button1, Button Tough 1, RC Button 4 (US), Wall Switch 4 (EU), Door/Window, Motion, H&T | BLE | BTHome v2 adverts, optional AES-CCM | [BTHome](https://www.home-assistant.io/integrations/bthome/) via HA Bluetooth, ESPHome or a Shelly proxy | The `shelly` integration does not support BLU devices. About 30 m line of sight |
| BLU ZB (BLE + Zigbee) | Button Tough 1 ZB, RC Button 4 ZB, Wall Switch 4 ZB (/DK), Remote Control ZB, Door/Window ZB (Mini, Outdoor), Motion ZB, H&T ZB, H&T Display ZB, Distance, TRV | BLE + Zigbee 3.0 | BTHome adverts + ZCL | BTHome or Z2M; TRV also via a BLU Gateway Gen3 in `shelly` | Pick one owner per function. TRV runs Zigbee and BLE together |
| BLU gateways | BLU Gateway (Gen2, feature-frozen), BLU Gateway Gen3 | Wi-Fi, BLE | RPC (`BluTrv` on Gen3) | Native | Serves BLU TRV and BLU devices on the Shelly side |
| Wave (Z-Wave) | Wave 1/1PM/2PM/Shutter/i4/i4 DC/1 Mini/1PM Mini/PM Mini/Dimmer/Plug S/Plug US/UK/Outdoor Plug S/H&T/Door-Window/Motion; Wave Pro 1/1PM/2/2PM/3/Shutter/Dimmer 1PM/2PM | Z-Wave; "LR" SKUs support Z-Wave Long Range | Z-Wave command classes (manufacturer 0x0460, Shelly Europe) | Z-Wave JS | No Wi-Fi/RPC. EU/US/AU/ANZ SKUs are different radios. On LR SKUs choose mesh or LR topology at inclusion |
| Wall Display (Android panels) | Wall Display, X2, X1i, X2i, XL | Wi-Fi, BLE | Gen2+ RPC (verify per model) | Native; media player on fw ≥2.2 | Mains-powered panel with a relay output. The original model also has T/H/lux sensors |
| ShellyX / Powered by Shelly | XMOD1, XT1 partner products (water valves, thermostats, EV charger), Ogemray 25A, Yihao YH002-A, Cury | Wi-Fi, BLE | Gen2+ RPC with extensions | Verify per product | Partner hardware: verify HA entity coverage per model |

Sources for HA support and limits: [HA Shelly](https://www.home-assistant.io/integrations/shelly/). Neutral: Gen3/Gen4 1L, 2L and Dimmer (EU) are rated "Neutral not needed: Yes" ([1L Gen4](https://kb.shelly.cloud/knowledge-base/shelly-1l-gen4)). [Dimmer Gen4 US](https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen4/ShellyDimmerG4US) requires N, and Shelly 1 Gen4 requires N or a DC supply ([KB](https://kb.shelly.cloud/knowledge-base/shelly-1-gen4)).

## Identify the generation/line from label, model or ID

| Model prefix | Line | Verified examples |
| --- | --- | --- |
| `SH…` | Gen1 | `SHSW-1` 1, `SHSW-PM` 1PM, `SHSW-L` 1L, `SHSW-21` 2, `SHSW-25` 2.5, `SHPLG-S` Plug S, `SHPLG-1` Plug, `SHPLG2-1` Plug E, `SHPLG-U1` Plug US, `SHWT-1` Flood, `SHHT-1` H&T, `SHDM-1` Dimmer, `SHRGBW2`, `SHEM`, `SHEM-3`, `SHIX3-1` i3, `SHUNI-1`, `SHBTN-1`, `SHDW-1/-2`, `SHMOS-01/-02`, `SHGS-1`, `SHSM-01`, `SHTRV-01` |
| `SN…` | Gen2 Plus | `SNSW-001X16EU` Plus 1, `SNSW-001X15UL` Plus 1 UL, `SNSW-001P16EU` Plus 1PM, `SNSW-002P16EU` Plus 2PM, `SNSW-001X8EU` Plus 1 Mini, `SNPM-001PCEU16` PM Mini, `SNSN-0024X` i4, `SNSN-0D24X` i4DC, `SNSN-0013A` H&T, `SNSN-0031Z` Smoke, `SNSN-0043X` Uni, `SNDM-0013US` Wall Dimmer, `SNDC-0D4P10WW` RGBW PM, `SNPL-00112EU` Plug S V1, `SNPL-10112EU` Plug S V2, `SNPL-00116US` Plug US |
| `SP…` | Pro | `SPSW-004PE16EU` Pro 4PM, `SPSH-002PE16EU` Dual Cover PM, `SPDM-002PE01EU` Dimmer 2PM, `SPDC-0D5PE16EU` RGBWW PM, `SPEM-003CEBEU` Pro 3EM, `SPEM-003CEBEU400` 3EM-400, `SPEM-002CEBEU50` EM-50, `SPCB-01VENEU` Pro 1CB |
| `S3…` | Gen3 | `S3SW-001X16EU` 1, `S3SW-001P16EU` 1PM, `S3SW-002P16EU` 2PM, `S3SW-0A1X1EUL` 1L, `S3SW-0A2X4EUL` 2L, `S3SW-001X8EU` 1 Mini, `S3PM-001PCEU16` PM Mini, `S3SN-0024X` i4, `S3SN-0U12A` H&T, `S3DM-0A101WWL` Dimmer, `S3DM-0010WW` 0/1-10V, `S3DM-0A1WW` DALI, `S3SH-0A2P4EU` Shutter, `S3EM-002CXCEU` EM, `S3EM-003CXCEU63` 3EM-63, `S3PL-00112EU` Plug S, `S3PL-30110EU` Plug M, `S3PL-30116EU` Plug PM, `S3PL-20112EU` Outdoor Plug S, `S3PL-10112EU` AZ Plug, `S3BL-D010009AEU` Duo Bulb, `S3BL-C010007AEU` Multicolor Bulb, `S3GW-1DBT001` BLU Gateway Gen3, `S3SN-0U53X` The Pill |
| `S4…` | Gen4 | `S4SW-001X16EU` 1, `S4SW-001P16EU` 1PM, `S4SW-002P16EU` 2PM, `S4SW-0A1X1EUL` 1L, `S4SW-0A2X4EUL` 2L, `S4SW-001X8EU` 1 Mini, `S4SW-001P8EU` 1PM Mini, `S4SN-0A24X` i4, `S4DM-0A101WWL` Dimmer, `S4DM-0A102US` Dimmer US, `S4DM-0010WW` 0/1-10V, `S4EM-002CXCEU` EM, `S4EM-001PXCEU16` EM Mini, `S4PL-00116US` Plug US, `S4PL-00416EU` Power Strip 4, `S4SN-0071A` Flood, `S4SN-0071Z` Flood S, `S4SN-0U61X` Presence |
| `SB…` | BLU / BLU ZB | `SBBT-002C` Button1 and Button Tough 1, `SBBT-004CEU` Wall Switch 4, `SBBT-004CUS` RC Button 4, `SBDW-002C` D/W, `SBMO-003Z` Motion, `SBHT-003C` H&T; ZB: `SBBT-102C`, `SBBT-104CEU`, `SBBT-104CUS`, `SBRC-005B`, `SBDW-103C`, `SBMO-103Z`, `SBHT-203C`, `SBHT-103C` (Display), `SBDI-003E` Distance, `SBTR-001AEU` TRV |
| `QN…` / `QL…` / `QP…` | Wave / Wave LR / Wave Pro | `QNSW-001X16EU` Wave 1, `QLSW-001X16EU` and `QLSW-001X15US` Wave 1 LR, `QNPL-0A112EU` Wave Plug S, `QNDW-002CEU` Wave D/W, `QLHT-0U2ZEU` Wave H&T LR, `QPSW-0A3X16EU` Wave Pro 3 |
| `SAWD…`, `GWF-`/`SNGW-` | Wall Display; BLU Gateway (Gen2) | `SAWD1` Wall Display, `SAWD-2A1XX10EU1` X2, `SAWD-3A1XE10EU2` XL; `GWF-KZ01` (firmware model `SNGW-BT01`) |

Source: each device's KB "Device identification" block, e.g. [Shelly 1 Gen4](https://kb.shelly.cloud/knowledge-base/shelly-1-gen4), [Wave 1](https://kb.shelly.cloud/knowledge-base/wave-1), and [BLU device pages](https://shelly-api-docs.shelly.cloud/docs-ble/Devices/BLU/button). The middle segments are not published as a decoding scheme, so match the full code. A regional suffix (`EU`, `US`, `UL`, `ANZ` page) marks a distinct product.

- **Default SSID/ID.** Gen1 SSIDs are lowercase plus 6 hex digits (`shelly1-XXXXXX`, `shellyswitch25-…`, `shellyht-…`). Plus SSIDs look like `ShellyPlus1PM-XXXXXX`. Gen3/Gen4 append `G3`/`G4` (`Shelly1PMG4-…`). A Gen2+ device ID is lowercase name plus MAC (`shellypro4pm-f008d1d8b8b8`).
- **Ask the device.** `GET http://DEVICE_IP/shelly` returns `type` (e.g. `SHSW-21`) on Gen1. On Gen2+ it returns `gen`, `model`, `app` and `id` ([Shelly component](https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Shelly)). The response is unauthenticated identification data. Do not dump `Shelly.GetConfig` instead.
- **Radio identifiers.** Zigbee devices report short model IDs (`1L`, `I4`, `EM Mini`, `BLU TRV`), which Z2M maps to the SKUs above ([converters](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/shelly.ts)). Wave devices report manufacturer `0x0460` plus a product type and ID.

## Gen1: CoIoT is required

For Gen1 HA communication, CoIoT must be enabled. A unicast peer targeting HA on UDP 5683 is required for battery devices, and routed networks must pass this traffic. Gen2+ uses a different connection model, so diagnose it with the matching section; opening CoAP is not a universal fix. [HA Shelly](https://www.home-assistant.io/integrations/shelly/).

## Gen2+ (Plus, Pro, Gen3, Gen4 in Wi-Fi mode)

- **Firmware policy.** Gen3/Gen4 and Gen2 models still in production receive all updates. Plus 1/1 Mini, 1PM/1PM Mini, 2PM, PM Mini, i4, Plug S, Plug US, H&T, 0-10V Dimmer and BLU Gateway are feature-frozen at 1.7.x and receive critical fixes only ([policy](https://shelly-api-docs.shelly.cloud/gen2/General/FirmwareUpdatePolicy)).
- **Battery devices.** Gen2+ battery devices (Plus H&T, Plus Smoke, H&T Gen3, Flood Gen4) must be woken for setup and may need the outbound WebSocket set to `ws://<HA>:<port>/api/shelly/ws`. Their update entities only report availability.
- **Bluetooth proxy.** Non-battery Gen2+ devices can serve as HA Bluetooth proxies, passive or active scanning. They cannot proxy GATT connections.
- **Enhanced Security** (fw 2.0.0) moves the device to HTTPS on port 443. Enable "Verify SSL" only with a CA that HA trusts.

### Worked example: Plus Plug S (Gen2)

Two hardware revisions exist: V1 `SNPL-00112EU` and V2 `SNPL-10112EU` ([KB V2](https://kb.shelly.cloud/knowledge-base/shelly-plus-plug-s-v2)); the Gen3 successor is `S3PL-00112EU`. The Plus Plug S exposes `switch:0`, power measurement, `PLUGS_UI` LED configuration, MQTT, outbound WebSocket and scripts. It is feature-frozen at 1.7.x ([API](https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen2/ShellyPlusPlugS/)).

```text
GET http://DEVICE_IP/rpc/Shelly.GetDeviceInfo
GET http://DEVICE_IP/rpc/Shelly.GetStatus
GET http://DEVICE_IP/rpc/Switch.GetStatus?id=0
```

Confirm these methods against the installed firmware. Do not put full configuration responses (Wi-Fi, MQTT, webhook credentials) into a shared diagnostic. Use the native integration unless a specific MQTT requirement justifies another path, and never let two paths issue commands concurrently.

Pilot one plug with a known steady load and compare device UI, HA power and a reference meter; keep W separate from cumulative Wh/kWh. Check:

- restored state after an authorised power interruption;
- overload behaviour against the manual;
- that no automation can switch off the HA host or router.

Test the reporting load of all plugs before shortening every interval.

## Gen4 and BLU ZB: Zigbee/Matter profiles

Gen4 Wi-Fi devices default to a Matter firmware profile. Pressing the button 5 times switches to the Zigbee profile and back, and 3 presses start inclusion for 3 minutes ([KB 1 Gen4](https://kb.shelly.cloud/knowledge-base/shelly-1-gen4), [Flood Gen4](https://kb.shelly.cloud/knowledge-base/shelly-flood-gen4)). Constraints in Zigbee mode:

- BTHome components are unavailable ([API 1 Gen4](https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen4/Shelly1G4)).
- Zigbee commands cannot start dimmer calibration ([Dimmer Gen4](https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen4/ShellyDimmerG4)).
- 2PM Gen4 appears as separate Z2M switch and cover definitions. Setting the profile before pairing is inferred, not documented.

Report (2025, fw 1.7.1, [HA forum](https://community.home-assistant.io/t/shelly-gen4-zigbee-mode/888242)): Wi-Fi stayed usable alongside Zigbee only with Bluetooth disabled, and Zigbee pairing and latency were inconsistent on ZHA and Z2M. Pilot one unit before you commit a fleet to Zigbee mode.

BLU TRV runs Bluetooth 5 LE and Zigbee 3.0 simultaneously. For Shelly-side control and schedules it needs a BLU Gateway Gen3 or another Shelly that can act as a BLU gateway. HA supports it through such a gateway or through Z2M ([KB](https://kb.shelly.cloud/knowledge-base/shelly-blu-trv), [API](https://shelly-api-docs.shelly.cloud/docs-ble/Devices/BLU_ZB/trv)).

## BLU sensors and buttons

BLU devices broadcast [BTHome](https://shelly-api-docs.shelly.cloud/docs-ble/) and can encrypt it with AES-CCM. The 16-byte key is generated on the device when you set a passkey, can be read only by a paired peer, and encryption is undone only by factory reset ([encryption](https://shelly-api-docs.shelly.cloud/docs-ble/encryption)). An encrypted device stays invisible in HA until you enter that key. Wall Switch 4 / RC Button 4 firmware below 1.0.22 enters pairing on a 10 s single-button hold; update before using holds for dimming or blinds. Acceptance means a real press or stimulus reaches HA through the intended receiver, not just discovery.

## Wave (Z-Wave)

Wave products are Z-Wave end devices. Include them with a Z-Wave controller under Z-Wave JS; Shelly Wi-Fi, RPC and CoIoT instructions do not apply. LR SKUs require choosing mesh or Long Range topology at inclusion, and mesh-only features do not apply under LR ([Wave 1 EU LR](https://kb.shelly.cloud/knowledge-base/shelly-wave-1-eu-lr)). Match the regional SKU to the controller's frequency region.

## Worked example: Flood leak sensors

Three products share the name; confirm the label first:

| Product | Model | Behaviour |
| --- | --- | --- |
| Original Flood | `SHWT-1`, Gen1 | Battery Wi-Fi sensor that sleeps between reports and events. Its local interface is reachable only in a limited setup wake window. Rain mode changes local alarm behaviour ([Gen1 API](https://shelly-api-docs.shelly.cloud/gen1/#shelly-flood)) |
| Flood Gen4 | `S4SN-0071A` | Leak-sensing cable |
| Flood S Gen4 | `S4SN-0071Z` | Single-point detector |

Both Gen4 models have Wi-Fi, BLE, Zigbee and Matter. One press wakes them for 3 minutes; two presses send them to sleep ([API Flood](https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen4/ShellyFlood)).

A sleeping HTTP endpoint does not by itself mean a broken sensor. Wake one unit and verify network and CoIoT/WebSocket/Zigbee settings, then run the manual's safe wet/dry test. Observe each separately:

- local alarm;
- HA wet event;
- notification;
- dry recovery;
- next health report.

Test every installed location, because a desk test does not establish radio behaviour near plumbing.

Report (2024-08-31, original Flood fw 1.14.0, HA 2024.8.3): local water detection and the audible alarm worked, but no HA event arrived. The issue was closed without an established universal fix ([core #124998](https://github.com/home-assistant/core/issues/124998)). A plausible battery value or a visible device is therefore not acceptance evidence for leak protection.

## Troubleshooting order

1. Capture exact model code, generation, profile (Wi-Fi/Matter/Zigbee) and firmware.
2. Inspect local state.
3. Verify that HA uses the right source interface (shelly, BTHome, Matter, Z2M or Z-Wave JS) and return path.
4. Confirm authentication.
5. Inspect event delivery.
6. Evaluate recorder load.

Use per-device logging for a bounded period. Change one parameter at a time and record its original value. Preserve local protective behaviour even if HA is offline.
