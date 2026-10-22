# Tuya Wi-Fi, BLE, cloud and local integrations

## Place the device

Tuya is a platform behind many white-label brands. A product sold under its own brand app can still be a Tuya device: clues are a Smart Life/Tuya Smart pairing option, a Tuya module (WB/CB/WR/T-series label) on the PCB, or a MAC prefix from the DHCP list in the HA Tuya [manifest](https://github.com/home-assistant/core/blob/dev/homeassistant/components/tuya/manifest.json). The portal and the cloud-assisted local routes see devices only in Tuya's own **Tuya Smart** or **Smart Life** apps; moving a device from a brand app can lose brand-only features (tuya-local cites vacuum maps). [tuya-local DEVICE_DETAILS](https://github.com/make-all/tuya-local/blob/main/DEVICE_DETAILS.md).

| Module family (Tuya label) | Chip | Open-firmware status |
| --- | --- | --- |
| TYWE…, older ESP modules | ESP8266/ESP8285 | Tasmota/ESPHome via serial; tuya-convert OTA blocked by Tuya's January 2019 patch on newer firmware ([tuya-convert](https://github.com/ct-Open-Source/tuya-convert)) |
| WB2S, WB3S, WB2L, WB3L | Beken BK7231T | OpenBeken, ESPHome/LibreTiny; cloudcutter if SDK unpatched |
| CB2S, CB3S, CB2L, CB3L, CBU | Beken BK7231N | Same as BK7231T |
| WR1/WR2/WR3/WR3E | Realtek RTL8710BN | OpenBeken, ESPHome/LibreTiny; cloudcutter (SDK 2.0.0 not vulnerable) |
| WBR1/WBR2/WBR3/WBRU | Realtek RTL8720CF | LibreTiny (AmebaZ2), OpenBeken; cloudcutter, fewer profiles |
| T-series: T1, T2/T34, T3, T7 | BK7238, BK7231N, BK7236, BK7239N (per OpenBeken) | OpenBeken lists all four; ESPHome only T1 and T2/T34 (BK7238, BK7231N); T3/T7 not in ESPHome |
| Non-Tuya-labelled white-label | LN882H, BL602, W800 … | OpenBeken; ESPHome for LN882H |

Chip mapping: [cloudcutter README](https://github.com/tuya-cloudcutter/tuya-cloudcutter), [OpenBeken README](https://github.com/openshwprojects/OpenBK7231T_App), [LibreTiny supported](https://docs.libretiny.eu/docs/status/supported/), [ESPHome LibreTiny](https://esphome.io/components/libretiny/). Read the protocol version from a LAN scan (`tinytuya scan`), not from the chip. Confirm the chip from the module label or a teardown before any firmware work.

## Local protocol versions

| Version | Behaviour relevant to diagnosis |
| --- | --- |
| 3.1 | Local key used only for commands: a wrong key still shows status, commands fail |
| 3.2 / "3.22" | Can be misdetected as 3.3; tuya-local's `3.22` forces tinytuya's device22 handling |
| 3.3 | Most common; wrong key fails on decode |
| 3.4 | Session-key negotiation; LocalTuya upstream supports up to 3.4 |
| 3.5 | Needs AES-GCM; old crypto backends (pyaes, PyCrypto) cannot talk to it |

LAN discovery uses UDP 6666/6667/7000, control TCP 6668. Many devices accept only one local connection (some hubs 1–3). [tinytuya](https://github.com/jasonacox/tinytuya), [tuya-local configuration](https://github.com/make-all/tuya-local#configuration).

## Choose the route

| Route | What it does | Dependencies and limits |
| --- | --- | --- |
| HA core `tuya` | Cloud push via Tuya's device-sharing SDK. Setup: User Code from app (Me → gear → Account and Security), then scan the HA QR code with the app; no IoT developer project required | Cloud/account dependence; SDK exposes less than Smart Life; all HA platforms except lock and remote; reload to see newly added devices; repeated re-auth when iot.tuya.com terms change. Product-ID quirks from `tuya-device-handlers`; custom ones in `<config>/tuya_quirks/<category>_<product_id>.py` |
| `rospogrigio/localtuya` (v5.2.5, 2026-01) | Local push with manual entity/DP configuration | Protocols 3.1–3.4; optional Tuya IoT project credentials for key retrieval and auto-update after re-pairing |
| `xZetsubou/hass-localtuya` fork (active, 2026-10) | LocalTuya fork with discovery, auto-configure, gateway sub-devices, IR `remote` entities | Protocols 3.1–3.5; auto-configure needs cloud API setup. A different project from upstream; do not mix configs |
| `make-all/tuya-local` | Local handling with matched device profiles | Device ID, local key, IP, protocol and profile; cloud-assisted setup by Smart Life/Tuya login without a developer account; hub sub-devices via `node_id`; battery Wi-Fi sensors without a hub unsupported |
| `tinytuya` (library/CLI) | Scan, poll, control; `wizard` dumps local keys | Wizard needs an iot.tuya.com project; its IoT Core trial lasts one month and must be extended |
| Tuya BLE | Direct: [`PlusPlus-ua/ha_tuya_ble`](https://github.com/PlusPlus-ua/ha_tuya_ble) (no push since 2024-07 — verify a maintained fork). Via Tuya BLE gateway: core `tuya`, cloud | Direct route works locally but needs device ID and encryption key from the Tuya IoT cloud |
| Direct Zigbee | Coordinator/converter handles Zigbee sub-devices | No Wi-Fi local key; see [tuya-zigbee.md](tuya-zigbee.md) |
| Matter (Wi-Fi product, or Tuya hub exposing Matter) | HA Matter for a certified product/bridge | Do not assume energy, effects or proprietary settings are exposed; tuya-local suggests Matter for hubs where it works and local Tuya for the rest |
| Reflash: OpenBeken, ESPHome (LibreTiny), Tasmota (ESP) | Replace Tuya firmware; HA via MQTT or ESPHome API | Permanent loss of Tuya app/cloud; needs verified chip/pinout. Route to `smart-home-esphome-mqtt` |
| `tuya-cloudcutter` | Wireless exploit to detach from cloud or flash custom firmware OTA | Only unpatched BK7231T/N, RTL8710BN, RTL8720CF (Tuya patched the SDK Feb 2022); afterwards Tuya apps and servers are unusable; needs a spare AP-capable Wi-Fi adapter |

[HA Tuya](https://www.home-assistant.io/integrations/tuya/), [tuya-device-handlers](https://tuya-device-handlers.readthedocs.io/), [LocalTuya](https://github.com/rospogrigio/localtuya), [hass-localtuya](https://github.com/xZetsubou/hass-localtuya), [tuya-local](https://github.com/make-all/tuya-local).

Missing HA functionality in core `tuya` can reflect the SDK's exposed schema, not a broken device. LocalTuya and tuya-local are different projects, not spelling variants; read the selected repository before generating configuration. A local operational path can still depend on the cloud for commissioning or renewed credentials, and tuya-local notes local use does not stop the device reporting to the Tuya cloud.

## Commission a local path deliberately

Record product ID, exact hardware, current firmware and vendor account region. Retrieve a local key only through an authorized account and current supported method; store it as a secret. Do not ask the user to paste it into a public issue. Reserve the device address, select the confirmed protocol, inspect readable data points, then match a profile. Verify one safe command and its reported state before configuring all entities.

Pairing again changes the local key. Protocol 3.1 with a wrong key can show initial status but break commands; newer versions fail during decoding. Re-pairing without updating a stored key is therefore a concrete diagnostic branch. [tuya-local connection documentation](https://github.com/make-all/tuya-local#configuration).

## Avoid common false fixes

- Do not run multiple active local controllers (or the phone app on the same LAN) against a device while diagnosing socket/session limits.
- Do not map DP 1 to a relay or divide DP values by ten without model evidence.
- Do not label a battery Wi-Fi sensor as suitable for continuous local polling; verify its wake behavior and supported protocol.
- Do not factory-reset to test a key until the current state, account binding and recovery plan are recorded.
- Do not flash Tasmota/ESPHome/OpenBeken or run cloudcutter based on the retail name; chips and PCB revisions change within one listing. Route firmware work to `smart-home-esphome-mqtt` with verified hardware.

## Internet-blocking test

After normal operation is established, test only the necessary dependency under explicit task scope. Verify startup after a device reboot, recovery after HA restart, time-dependent schedules, DNS/NTP requirements and cloud token/key renewal. A command working for five minutes without WAN does not establish permanent cloud independence. Preserve the vendor app recovery route until local operation is demonstrated.

## Updating and removal

Back up the custom integration and config, record the version, and pilot a change on one noncritical device. Stop automations that may command through both old and new routes. Remove the previous integration only after remapping entity IDs and validating manual control, unavailable states and power restoration. Use `home-assistant-hacs` for trust, repository provenance and rollback; this reference establishes which project and device path is appropriate.

## Historical firsthand key-handling report

[LocalTuya issue 1380](https://github.com/rospogrigio/localtuya/issues/1380), opened 2023-05-07, described decryption errors after Smart Life reactivation produced differently formatted keys. Exact hardware and integration versions were not given. The reporter subsequently marked it resolved and linked change 1381; inspect that change before claiming a fixed release. The useful diagnostic lesson is to check key parsing, protocol and integration version as well as key identity. It is not evidence that the old defect persists in current releases.
