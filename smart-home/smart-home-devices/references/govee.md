# Govee

Govee (appliances also sold as GoveeLife) ships hundreds of SKUs. Support is decided per **H-number**, never per family name: two strips with the same marketing name can use different controllers. Research baseline 2026-10-22.

## Product range

| Line / family | Device classes (example SKUs from Govee/HA lists) | Radio | HA route(s) | Key caveat |
| --- | --- | --- | --- | --- |
| LED strips: RGB, RGBIC, RGBICW/RGBWW, COB, M1 | H615A–H615E, H6143/H6144, H618A–H618G, H619A–H619Z, H61B1–H61BE, H61E0/H61E1 (M1), H61F2–H61F6 (Strip 2 Pro), H1A42–H1A45, H1AB1–H1AB3 (COB 2) | Wi-Fi + BLE | `govee_light_local` if listed; else govee2mqtt / cloud API | LAN covers some MultiColor/RGB SKUs too (H6110, H6159, H615A–E); BLE-only kits never |
| Neon rope | H61A0–H61A9, H61C2–H61C5, H61D2–H61D6 (Neon 2) | Wi-Fi + BLE | as strips | Segment/scene control needs cloud API or govee2mqtt |
| Bars, Glide, Hexa, Lines, panels, sconces | H6046–H6048, H6056, H6061 (Glide Hexa), H6062/H6065/H6066/H6067, H606A, H6063, H6069, H610A/H610B, H6038/H6039 | Wi-Fi + BLE | LAN if listed | LAN commands cover power, brightness, colour/CT only; per-panel effects need cloud/govee2mqtt |
| Floor/table lamps, projectors | H6072, H6076, H6078, H607C, H60B0–H60B3, H16B0, H1630, H6022 (Table Lamp 2), H8022, H6051/H6052, H6093–H6095, H609D | Wi-Fi + BLE | LAN if listed | Check each SKU; lamps of one family span several SKUs |
| Bulbs, downlights, ceiling | H6003–H6010 (Wi-Fi/Wi-Fi+BLE bulbs), H1401, H14A1, H14B1, H14C2, H8015, H601A–H601C, H801A/H801D, H60A0/H60A1/H60A4/H60A6, H1232/H1252/H1270 | Wi-Fi + BLE; some Matter | LAN if listed; Matter on Matter models | A BLE-only SKU needs a BLE project, not the LAN route |
| Outdoor: string, permanent, flood, path, net/tree, curtain | H7020–H7046 (string), H705A–H705F, H706A–H706C, H707A–H707C, H3A51–H3A53 (permanent), H7060–H7066 (flood/spot), H7055/H3500/H3510 (path), H6810/H6840/H70B1/H70BC/H70B6 (net, tree, curtain) | Wi-Fi + BLE | LAN if listed | LAN addresses the controller as one light, not per segment |
| TV backlights, DreamView, AI Sync Box | H6167, H6182, H6671/H6672 (TV Backlight 2), H6199 (DreamView T1, reported), H6604 (AI Sync Box 2) | Wi-Fi + BLE (+HDMI/camera) | LAN only for listed SKUs; sync mode via Govee app | Camera/HDMI sync is not reproducible from HA; H6199/H6604 are not in the core LAN list — verify |
| BLE thermo-hygrometers, meat/fridge thermometers | H5051/H5052, H5071–H5075, H5100–H5110, H5112, H5129, H5174, H5177–H5179, H5191, 5055/5181–5185/5198 | BLE | core `govee_ble` | H5074, H5075, H5129 need active scanning |
| BLE sensors and buttons | H5121 motion, H5122 button, H5123 window, H5124 vibration, H5125/H5126 switches, H5127 presence, H5130 pressure, H5106 air quality, H5140 CO₂ | BLE | core `govee_ble` | Events arrive via advertisements; check freshness and battery |
| Leak/contact sensors with gateway | H5054, H5059 leak and B5023 contact (433 MHz, rtl_433 decoders); H5058 Leak Detector 2 sensor; H5040 gateway | sub-GHz to Wi-Fi gateway (H5058 radio: verify) | rtl_433 (SDR) → MQTT; cloud via gateway (verify) | Not BLE: `govee_ble` does not list them; B5023 reports open only |
| Plugs | H5082 (govee2mqtt issue); other plug SKUs verify | Wi-Fi | cloud API / govee2mqtt | govee2mqtt calls Platform API plug control buggy |
| Appliances (GoveeLife) | humidifiers (H7160), heaters/fans/purifiers (H7101, H7102, H7111, H7121, H7130, H7131, H713A, H7135), kettles (H7171, H7173), ice makers, diffusers | Wi-Fi | cloud API: govee2mqtt or HACS goveelife | No LAN API for appliances; cloud-dependent |

Example SKUs come from Govee's LAN list, HA integration pages, govee2mqtt SKU notes and rtl_433; they are reference points, not a full catalogue. Re-check the live LAN list for any SKU.

## Identify the line from the label or model ID

- The SKU is printed on the controller/box label and shown in the Govee app device settings; the LAN scan reply returns it as `"sku":"Hxxxx"` with BLE and Wi-Fi hardware/software versions.
- Observed prefix pattern (inference, not a Govee spec): `H50xx/H51xx` BLE sensors, `H60xx` lamps/bars/panels/bulbs, `H61xx` strips/neon/TV strips, `H66xx` gaming/TV, `H68xx` holiday/net/tree, `H70xx` outdoor, `H71xx` appliances, `H80xx` later revisions of existing products (e.g. H8022 Table Lamp 2S, H80A1 ceiling light), `H1xxx`/`H3xxx` newer indoor/outdoor families. Never route on the prefix alone.
- `R`-prefixed SKUs (R60B3, R1250, R3A51) appear beside H-models of the same product name in Govee's LAN list; treat them as separate SKUs.
- Suffixed variants (H6076A, H8076A) and Matter certificates can differ from the base SKU. One CSA Matter record (Ceiling Light Pro) carries Product ID `0x60A6`, matching H60A6 — useful corroboration, not a rule.

## Routes

| Route | Scope | Requirements / limits |
| --- | --- | --- |
| Core `govee_light_local` (HA 2024.2+, local push) | Lights on the core supported list | Enable LAN control per device in the app; some scenes are not supported on every device |
| Govee LAN API | Same lights | Device joins multicast `239.255.255.250`, listens on UDP 4001; client receives scan replies on UDP 4002 and sends commands to UDP 4003. Commands: `turn`, `brightness` (1–100), `devStatus`, `colorwc` (RGB or 2000–9000 K). If the LAN switch is missing on a listed SKU, power-cycle and wait ~30 min |
| Core `govee_ble` | Listed BLE sensors/buttons | Bluetooth integration working; active scan for H5074/H5075/H5129. Sensor support does not cover BLE light control |
| Matter (Wi-Fi) | Matter-certified SKUs (M1 strip, Ceiling Light Pro, TV Backlight 3S, Light Wall, Cone Tree Lights per CSA/Govee) | IPv6, 2.4 GHz, commission within 15 min of power-on; on/off, brightness, CT, colour only. Changing Wi-Fi in the Govee app disables Matter until reset |
| Govee developer/OpenAPI (cloud) | Lights, plugs, sensors, appliances | API key requested in the Govee app; `https://openapi.api.govee.com`, header `Govee-API-Key`; capability model (on/off, range, segment colour, dynamic scene, work mode…); per-account and per-device rate limits, 429 on excess |
| govee2mqtt (add-on/Docker, MQTT) | Mixed fleets | LAN first, then undocumented AWS IoT (account e-mail/password, "likely unsupported") and Platform API (key); no BLE |
| HACS `goveelife` | Wi-Fi devices via OpenAPI v2, incl. appliances, RGBIC segments | Cloud polling (60–120 s suggested); not all devices exposed |
| HACS `govee_ble_lights` | Some BLE lights | Per-model BLE protocols; few releases — verify activity |
| HACS `hacs-govee` (LaggAt) | Legacy cloud API | Author discontinued development; prefer a maintained route |

## Worked example: LAN discovery that does not work

Order: SKU on LAN list → LAN switch on → device IP → HA host interface/VLAN → multicast and UDP 4001/4002/4003 return path → duplicate listener → parser. A working cloud app does not prove LAN is enabled. A **2025-03-08** report on HA **2025.3.1** (working on 2025.2.x) showed Govee Lights Local unable to bind port 4002; closed stale/not planned, no universal fix established. [Core issue 140100](https://github.com/home-assistant/core/issues/140100). Port 4002 is the client-side scan listener, so look for another LAN client (govee2mqtt, a second integration) on the same host first.

## Integration assessment

Record which capability matters: on/off, RGB/white, per-segment colour, scenes, music mode, temperature, leak alarm, buttons, appliance settings. Test each on the candidate route; status may echo the last command rather than hardware state. Use one command owner while testing: a local integration, govee2mqtt and a cloud automation together compete for sockets and state.

## Commissioning and updates

Pilot one device: manual/app change reflected in HA, device reboot, HA restart, internet loss, recovery. Preserve vendor scenes where important. If firmware removes or changes the LAN option, keep exact version evidence before reset or replacement. Do not claim availability, reliability or API pricing without a fresh check.
