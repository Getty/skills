# OSRAM, LIGHTIFY and LEDVANCE SMART+

Research baseline 2026-10-22. LEDVANCE (the former OSRAM general-lighting business) sells smart products under both the LEDVANCE and the licensed OSRAM brand ([HA blog](https://www.home-assistant.io/blog/2026/10/13/ledvance-joins-works-with-home-assistant/)). In the US the brand is SYLVANIA. One brand name covers four unrelated transports: Zigbee, Tuya-style Wi-Fi, Bluetooth mesh/HomeKit, and Matter over Wi-Fi. Identify the transport before picking anything.

## Product range

| Line / family | Device classes | Radio | HA route(s) | Key caveat |
| --- | --- | --- | --- | --- |
| OSRAM LIGHTIFY Home (discontinued) | Gateway, ZLL lamps, Flex strips, Gardenpole/Gardenspot, Surface/Under Cabinet, Switch 4x / Switch Mini, plug, motion sensor | Zigbee Light Link; gateway on Wi-Fi | Children: ZHA/Z2M. Gateway: legacy YAML `osramlightify` (local polling; lights, groups, sensors, switches) ([HA](https://www.home-assistant.io/integrations/osramlightify/)) | Servers and support ended 2021-08-31: no updates, no cloud-to-cloud, app not guaranteed on new OSes ([LEDVANCE FAQ](https://www.ledvance.com/en-asia/home-lighting/services/faq/faq-for-smart-zigbee-products), [OSRAM](https://ams-osram.com/news/press-releases/pr-09-03-2020)). The lamps' radios still work |
| LIGHTIFY Pro / professional Zigbee | Push-button controller (PBC), Biolux HCL panels, SubstiTUBE / T8 EM connected tubes, Zigbee 3.0 DALI CONV LI | Zigbee | Z2M (definitions exist); ZHA generic | Professional install items. Check the exact Z2M definition and endpoint layout (the DALI converter has 4 variants) |
| SMART+ Zigbee (OSRAM → LEDVANCE; still sold, 13 SKUs in the 2026 catalogue) | Classic A60/B40/P40, PAR16 GU10, filament, Flex indoor/outdoor, Gardenpole, panels, undercabinet, plugs (incl. `PLUG EU EM T` with energy meter), outdoor plug | Zigbee ZLL (old) or Zigbee 3.0 (QR code on product) | ZHA/Z2M; Hue Bridge (LEDVANCE lists Philips Hue as a platform) → `hue`; Echo with Zigbee hub; deCONZ/Phoscon | ZLL ↔ Z3 cannot be converted. SMART+ Zigbee Switches do not work with Z3 products. Bosch, Somfy TaHoma and Legrand take Z3 only ([FAQ](https://www.ledvance.com/en-asia/home-lighting/services/faq/faq-for-smart-zigbee-products), [catalogue](https://www.ledvance.com/en-int/professional-lighting/products/smart-home-c6248)) |
| SYLVANIA SMART+ / LIGHTIFY (US) | A19, BR30, RT5/6, MR16, Flex XL, plug, dimming switch, contact sensor | Zigbee | ZHA/Z2M (vendor "Sylvania") | US bases and SKUs; examples of modelID: `LIGHTIFY A19 RGBW`, `A19 TW 10 year`, `PLUG`, `Contact Sensor-A` ([Z2M sylvania.ts](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/sylvania.ts)) |
| SMART+ Wi-Fi (largest current line: 63 SKUs) | Lamps, spots, strips, Planon panels, outdoor, cameras, ceiling fans, contact/motion/outdoor-motion sensors | Wi-Fi 2.4 GHz, Tuya-based firmware | HACS `tuya-local` / LocalTuya with a local key; cloud skills (Alexa, Google) | Use the LEDVANCE app, not Smart Life. Reported: LEDVANCE does not open these devices to the Tuya platform ([forum report](https://community.home-assistant.io/t/local-integration-to-ledvance-smart-wifi/406475)). [tuya-local](https://github.com/make-all/tuya-local) has LEDVANCE Planon, camera and fan configs. Map DPs one model at a time |
| SUN@HOME (human-centric) | Classic E27/E14, Panan desk/floor/monitor-clip lamps, Planon panels, slim downlights | Wi-Fi; SunLike LEDs, 2200–5000 K | As SMART+ Wi-Fi; reports of `tuya-local`/LocalTuya ([product story](https://www.ledvance.com/en-uk/professional-lighting/lighting-insights/product-stories/sun-at-home)) | Controlled by the LEDVANCE SMART+ WiFi app. The circadian schedule lives in the app; HA has to rebuild it |
| SMART+ Bluetooth | Lamps, luminaires (mesh); older "Works with Apple HomeKit" generation | BLE mesh; BLE HomeKit | HomeKit-marked: HA `homekit_controller` over BLE (verify per model). Mesh-only: no HA route verified | Packaging carries a Bluetooth label or a HomeKit mark and an 8-digit Bluetooth ID ([FAQ](https://www.ledvance.com/en-asia/home-lighting/services/faq/faq-for-smart-zigbee-products)) |
| SMART+ Matter (13 SKUs; 116 models certified Works with HA on 2026-10-13) | Lamps, filament, spots, down/track lights, ceiling/wall, floor lamps, Flex strips, `SMART+ MATTER Plug EU`, Compact Outdoor Plug, wall switches, "Magic" luminaires | Matter over Wi-Fi, 2.4 GHz ([LEDVANCE FAQ](https://www.ledvance.com/en-int/home-lighting/services/faq/faq-for-smart-app_matter-products)) | HA `matter` (released). The `ledvance` brand page is 2026.11 metadata only | No LEDVANCE Matter-over-Thread product verified. Up to 5 fabrics. HA gets power-on behavior and some plug features. No Matter OTA: update through the SMART+ app. Amazon-only variants marked "Not compatible with SMART+ App" update only through Alexa |
| IR-remote RGB lamps (OSRAM/LEDVANCE, 24-button remote) | RGB lamps / lights | Infrared | `osram_infrared` (HA 2026.10) + an `infrared` emitter (e.g. ESPHome) ([HA](https://www.home-assistant.io/integrations/osram_infrared/)) | One-way, assumed state. No brightness. Colour snaps to remote presets. Add an IR receiver to track the physical remote |

Apps: OSRAM LIGHTIFY (dead), LEDVANCE SMART+ WiFi (old Wi-Fi app, cannot add Matter products), SMART+ app (`com.ledvance.smartunify`; Wi-Fi, Bluetooth mesh, Matter; no Zigbee) ([SMART+ app](https://www.ledvance.com/en-int/home-lighting/services/control-options/smart-app)). Cloud-to-cloud links built for SMART+ Wi-Fi do not work with SMART+ Matter products.

## Identify the line from the label or model ID

- **Zigbee manufacturer:** `OSRAM` (LIGHTIFY/SMART+ era) or `LEDVANCE` ([ZHA quirks](https://github.com/zigpy/zha-device-handlers/tree/dev/zhaquirks/osram)). US units are defined under the Sylvania vendor. Z2M sends the OSRAM-specific cluster `0xFC0F` (save/reset startup parameters) with manufacturer code `0x110C`.
- **modelID patterns** in [Z2M ledvance.ts](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/ledvance.ts) and [osram.ts](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/osram.ts):
  - `… - LIGHTIFY` or `LIGHTIFY …` = ZLL era.
  - `… Z3` = Zigbee 3.0 (`A60 TW Z3`, `PAR16 RGBW Z3`, `Plug Z3`).
  - A trailing ` T` marks the newer LEDVANCE generation (`A60 TW T`, `PAR16 DIM T`, `PLUG EU T`).
  - `Value` / `Value II` (`A60 RGBW Value II`) and `…S` variants (`A60S TW`, `PAR16S RGBW`).
  - The light-type token is `TW` (tunable white), `RGBW`, `DIM` or `FIL` (filament).
- **Article numbers:** EANs beginning `4058075`, `4099854`, `4052899` or `4062172`. Z2M also lists codes like `AC…`, `AB…`, `AA…` as model numbers. `ledvance.com/docs/<EAN>` opens the documents page for that EAN, including the manual and the EU Data Act sheet.
- **Box and product marks:**
  - Zigbee logo = Zigbee; a QR code printed on a Zigbee product = Zigbee 3.0.
  - Bluetooth label, HomeKit mark or 8-digit Bluetooth ID = Bluetooth line.
  - Matter badge with QR or 11-digit code = Matter (Wi-Fi). Packaging badges "works with SMART+ app" / "works with LEDVANCE app" say which app manages the product.
  - The FAQ separates first-generation LEDVANCE-brand Matter lamps from newer OSRAM-brand Matter lamps; the Wi-Fi remote works only with the latter.
  - "WIFI" or "Wi-Fi" in the product name without a Matter badge = Tuya-style Wi-Fi.

## Integrate and reset

Read labels and existing signatures first. A working Zigbee lamp can stay on its current coordinator or bridge when HA gets the controls it needs. Before moving it, inventory remote and group bindings. A failing LIGHTIFY gateway is no reason to discard working children; verify direct support for each one.

| Line | Reset (manufacturer) |
| --- | --- |
| Zigbee lamps and luminaires (ZLL and Z3) | 5× (on 5 s, off 5 s), then on. Confirmation: ZLL one flash; Z3 RGBW blue-green-red; Z3 TW cold/warm flashes; Z3 DIM up/down dimming |
| Zigbee plug / Switch / Switch Mini / motion sensor | Plug: hold ≥10 s. Switch: hold upper-left + lower-right ~10 s. Mini: hold middle + lower ~10 s. Motion sensor: hold grey button ≥10 s |
| Matter (Wi-Fi) lamps / plugs / wall switches | Lamps: 5× on/off at 3 s intervals; the 6th power-on blinks 6 s. Plug: hold 5 s. Switch: hold any button 5 s. Removing a device from its last fabric resets it |

Zigbee firmware: LEDVANCE ships updates through partner systems (Magenta SmartHome, Bosch, Schwaiger) and deCONZ/Phoscon. Z2M's OTA index holds OSRAM (`0x110C`) images for some models; check each model. In Z2M, `set_transition` sets the default on/off fade and `remember_state` stores current values as the startup state. `remember_state` has to be re-sent after every change.

Test minimum dimming, startup brightness, colour-temperature range, transitions and the state after power restoration. Do not let a wall switch cut a lamp that routes for battery devices. For plugs, read the physical load rating, not an integration capability. Use a manufacturer reset only when migration is intended, one lamp at a time, with a physical lighting fallback.

## Source date guard

At the baseline the HA `ledvance` brand page says **introduced in 2026.11**, and no `ledvance` brand is in core 2026.10.2. Do not treat the page as a released integration. The Works with HA certification (blog 2026-10-13) covers Matter-over-Wi-Fi devices on the existing `matter` integration, which is released. Unlisted products are not proven unsupported, and the certification says nothing about Zigbee, Wi-Fi/Tuya or Bluetooth lines ([observed page](https://www.home-assistant.io/integrations/ledvance/)).

## Evidence

Match a report to its line, model and firmware. Do not carry a LIGHTIFY ZLL issue over to SMART+ Matter Wi-Fi devices or to the reverse. [Z2M #26686](https://github.com/Koenkk/zigbee2mqtt/issues/26686) (2025-03-10) involved a LIGHTIFY-era Outdoor Flex RGBW (`4058075036185`, modelID `LIGHTIFY Outdoor Flex RGBW`) on Z2M 2.1.1/2.1.3 with Dongle-E firmware 7.4.5. It reported incomplete pairing that succeeded after further restarts or reconfigures. The issue closed as a duplicate of a delivery-failure issue. The maintainer suspected interference; the reporter disputed that. It shows no universal OSRAM defect and no general restart remedy. Separate identity match, interview completion and network delivery before changing a mesh. Tuya-local and LocalTuya reports for SMART+ Wi-Fi and SUN@HOME are community evidence. Confirm DPs on the exact unit.
