# THIRDREALITY

Third Reality, Inc. makes mostly Zigbee 3.0 devices, plus Matter-over-Wi-Fi and Matter-over-Thread lines, hubs/bridges and HA-oriented dev hardware. It has been a [Works with Home Assistant](https://www.home-assistant.io/integrations/third_reality/) partner for Zigbee and Matter since 2022. Range snapshot from the [US store catalog](https://www.3reality.com/products.json) and the [Z2M Third Reality converter](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/third_reality.ts), 2026-10. Regional catalogs differ (the EU plugs are sold through retailers), so confirm the exact model ID.

## Product range

| Line / family | Model IDs (Zigbee) | Radio | HA route | Key caveat |
| --- | --- | --- | --- | --- |
| Plug Gen1 / Gen2 (US) | `3RSP019BZ` (no meter), `3RSP02028BZ` (metering) | Zigbee router (+BLE) | ZHA quirk (Gen2), Z2M | Gen2 private cluster 0xFF03: energy reset, countdowns, LED |
| Plug E2 (EU, 16 A Type F) | `3RSPE01044BZ` | Zigbee router (+BLE) | ZHA (same quirk as `3RSP02028BZ`), Z2M | WWHA-certified as "Smart Plug E2". Chatty metering. Worked example below |
| Plug Gen3 family | `3RSP02064Z` (US Gen3), `3RSPU01080Z` (UZ1), `3RSPE02065Z` (E3, EU), `3RSP0186Z` (C1), `3RSPJ0187Z` (J1) | Zigbee router | One ZHA quirk, one Z2M definition | Metering-only mode, power rise/drop thresholds. Vendor: the relay stays put during OTA, ±1% calibration |
| Multi-outlet | `3RDP01072Z` (Dual Plug ZP1), `3RWP01073Z` (Wall Plug/Outlet ZW1) | Zigbee router | ZHA, Z2M | Two endpoints, each metered |
| Matter Wi-Fi plugs | Smart Plug M1 `3RSP03046W` (WWHA), Smart Plug M3 (ID: verify) | Matter over Wi-Fi | HA Matter | M3 has no power meter |
| Colour bulbs | ZL1 `3RCB01057Z`, ZL2 `3RCB1095Z` (A21, 100–130 V), ZL4 `3RCB02070Z`; older `3RSL011Z` (A19), `3RSL012Z` (BR30) | Zigbee router | ZHA, Z2M | US-voltage bulbs. ZB3 BR30 ID: verify |
| Night lights | `3RSNL02043Z` (Zigbee multi-function), `3RSNL02041WM` (Matter Wi-Fi colour), `3RSNL02042TM` (Night Light-T, Matter over Thread) | Zigbee router / Wi-Fi / Thread | ZHA·Z2M / Matter / Matter + Thread border router | Same product idea on three radios. Read the ID before choosing a route |
| Switch actuators | `3RSS009Z` (Smart Switch Gen3), `3RSS008Z` (RealitySwitch Plus), `3RSS007Z`; Smart Switch MT1 (Matter over Thread); Timer Switch | Zigbee end device / Thread / app (radio: verify) | ZHA, Z2M; Matter | Mechanical rocker/toggle pusher on battery. Check fit and force. Timer Switch: HA support not established |
| Motion / presence | `3RMS16BZ`, R1 `3RSMR01067Z`, PIR Gen2 `3RMS26Z`; presence R2 `3RPS01083Z`, R3 `3RPL01084Z` (60 GHz, USB-C, repeater); TL2 (60 GHz, Matter Wi-Fi) | Zigbee end device; R3 router; TL2 Wi-Fi | ZHA (radar quirks), Z2M; Matter | Battery PIR vs powered radar: different clear-delay and routing behavior |
| Contact / tilt / vibration | `3RDS17BZ` door, `3RDTS01056Z` garage tilt, `3RVS01031Z` vibration; Garage Door Opener (Matter Wi-Fi, paired tilt sensor) | Zigbee end device; opener Wi-Fi | ZHA, Z2M; Matter | Treat the garage opener as a safety-relevant actuator |
| Leak | `3RWS18BZ`, WL2 `3RWS0218Z`; KM1 kit `3RWLK01068M`/`…S` (controller + detectors) | Zigbee end device; KM1 Matter over Wi-Fi | ZHA, Z2M; Matter | The KM1 detector-to-controller radio is undocumented. Test the alarm path end to end |
| Temp/humidity, air | `3RTHS24BZ` (LCD), Lite `3RTHS0224Z`, Lite Gen2 `3RTHS0324Z`; air quality `3RAQ1096Z`; filter sensor `3RAP0149BZ` | Zigbee | ZHA, Z2M | Check which values the device actually measures |
| Garden | Soil `3RSM0147Z`, Gen2 `3RSM0347Z`; Watering Kit `3RWK0148Z` | Zigbee | ZHA quirks, Z2M | Keep a maximum run time on irrigation |
| Buttons | `3RSB22BZ` (Smart Button), Scene Button S3 `3RSB01085Z`; Button ZB2 (3-key, ID: verify) | Zigbee end device | ZHA, Z2M | Map single/double/hold per key |
| Covers | Smart Blind `3RSB015BZ`, Blind Gen2 `3RSB02015Z`, roller motor `TRZB3`; Blind Lite (ID: verify) | Zigbee | ZHA quirks (gen1/gen2), Z2M | Calibrate travel limits before automations |
| Other | Outdoor Repeater `3ROR0194Z`; Smart Scale ZS1 `3RKS030Z` (sold as HA-only) | Zigbee | Z2M; ZHA | — |
| Hubs, bridges, dev kits | Hub Gen2 Plus; Smart Bridge MZ1 (Zigbee→Matter, Wi-Fi); USB-C Zigbee dongle; Linux Box Dev Edition (Armbian, HA ZHA preloaded, Zigbee + Thread); Voice & Music Assistant Dev Edition | Zigbee/Wi-Fi/Thread | Dongle = coordinator (ZHA/Z2M); MZ1 exposes children over Matter | MZ1 bridges THIRDREALITY Zigbee end devices. Don't also pair them to HA Zigbee |

## Identify the line from the label or model ID

- The Zigbee model ID (`3R…`) is on the label and in the interview. Marketing names (E2, E3, UZ1, ZL1, ZP1, ZW1) map to IDs through the Z2M `whiteLabel` entries. Store SKUs (`P1…`, e.g. `P1SPD1Z` for Plug Gen3) are not Zigbee IDs.
- Family letters observed after `3R`: SP plug (SPE EU, SPU UZ1, SPJ J1), DP/WP multi-outlet, CB/SL lights, SNL night light, SS switch, MS/SMR/PS/PL motion/presence, DS door, DTS tilt, VS vibration, WS water, WLK leak kit, THS temp/humidity, AQ air, AP filter, SM soil, WK watering, OR repeater, KS scale. **SB means both blind and button** (`3RSB015BZ` shade, `3RSB22BZ` button), so never decode it alone.
- Suffixes observed, not vendor-documented: `Z` Zigbee, `BZ` Zigbee with BLE (Z2M calls `3RSP019BZ`/`3RSP02028BZ`/`3RSPE01044BZ` "Zigbee / BLE"), `WM` Matter over Wi-Fi, `TM` Matter over Thread, `W` Wi-Fi.
- Zigbee manufacturer string: `Third Reality, Inc` ([ZHA quirks](https://github.com/zigpy/zha-device-handlers/tree/dev/zhaquirks/thirdreality)), manufacturer code 0x1233. The Gen3 plug's private attributes use code 0x1407 in both ZHA and Z2M.
- The [WWHA list](https://works-with.home-assistant.io/certified-products/) has data errors: `3RMS16BZ` is shown as Matter over Wi-Fi, the tilt sensor carries the vibration ID `3RVS01031Z`, and M1 `3RSP03046W` is shown as Zigbee. Confirm against the label and the interview.

## Route rules

Choose one controller per device: HA Zigbee (ZHA or Z2M), the Third Reality hub/app, or MZ1→Matter. Mains devices (plugs, bulbs, night lights, presence R3, repeater) route. Battery sensors, buttons and switch pushers are end devices. Z2M support and ZHA support are separate, so check the quirk in the installed HA release independently. A BLE radio in a Zigbee plug does not mean HA's Bluetooth integration can control it.

## Worked example: Plug E2 `3RSPE01044BZ`

Keep the exact ID. Z2M exposes switch, power-on behavior, power, energy, current, voltage, AC frequency, power factor, LED brightness, energy reset, countdown on/off, and OTA ([device page](https://www.zigbee2mqtt.io/devices/3RSPE01044BZ.html)). These are converter capabilities. Firmware and the installed release decide what is actually available. ZHA applies the Gen2 quirk shared with `3RSP02028BZ` (energy reset, countdowns, LED brightness). The successor E3 `3RSPE02065Z` is a Gen3 device with a different cluster, metering-only mode and thresholds. Evidence about one is not evidence about the other. Z2M notes that by default Gen3 W readings can lag about a minute until the rise/drop thresholds are lowered ([Gen3](https://www.zigbee2mqtt.io/devices/3RSP02064Z.html)).

## Plug acceptance and measurement

Build a per-plug record: firmware, converter/quirk version, circuit and use, the control that is required, and the energy unit. Do not reset accumulated energy to "fix" a scaling discrepancy. Compare a steady resistive reference load and a representative appliance cycle against an independent meter. Current × voltage is apparent power and equals real power only at the corresponding power factor. Check power and cumulative energy separately. On Gen3, use metering-only mode where an accidental switch-off is harmful.

Measure the message rate with outputs on and with outputs off. Pilot one or two plugs before changing reporting on a batch. A successful write to the reporting table does not prove the device obeys it in every state. Protect button latency and battery-device delivery from metering traffic.

## Firsthand evidence (E2 `3RSPE01044BZ`)

- **2025-11-10, Z2M 2.6.3, plug firmware v1.00.98, SLZB-06M:** an owner reported excessive power/energy for a dishwasher on two units, checked against a separate meter. Closed as completed on 2025-12-12. This establishes neither a general fix nor a failure rate. [Issue 29573](https://github.com/Koenkk/zigbee2mqtt/issues/29573).
- **2026-03-09, Z2M 2.9.1, plug firmware 1.01.01, SLZB-06M:** an owner of a large plug fleet saw response improve after reducing reporting, then saw high-rate reporting while plugs were off. The issue is still open. On 2026-10-16 a vendor account asked whether it persists on firmware "104", with no answer recorded. [Issue 31332](https://github.com/Koenkk/zigbee2mqtt/issues/31332).

These reports justify targeted checks on this exact model. They do not show that a batch of these plugs necessarily overloads a network, or that every firmware shares the problem.

## Recovery and changes

Inventory IEEE addresses, aliases, firmware and parent router before updates. Pilot firmware with representative measurement and latency checks. If settings are ignored, keep the before/after trace and escalate with the model signature rather than rewriting clusters repeatedly. Factory reset is the last diagnostic step: it discards network membership and can break automation references.
