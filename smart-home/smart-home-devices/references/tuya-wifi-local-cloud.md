# Tuya Wi-Fi, cloud and local integrations

## Distinguish the projects

| Route | What it does | Dependencies and limits |
| --- | --- | --- |
| HA core `tuya` | Integrates devices associated with Tuya Smart/Smart Life through the supported account flow | Cloud/account dependence; exposed capabilities may be less than the vendor app |
| `rospogrigio/localtuya` and separately maintained forks | Custom local handling with device/entity configuration | Exact repository matters; verify release maintenance, protocol and key acquisition |
| `make-all/tuya-local` | Custom local handling with matched device profiles | Device ID, local key, IP, protocol and correct profile are required |
| Direct Zigbee | Coordinator/converter handles Zigbee device | No Wi-Fi local key for the endpoint; see the separate Zigbee reference |
| Matter variant | HA Matter for actual Matter product/bridge | Do not assume energy/effects/proprietary settings are exposed |

The current native setup uses an app account, user code and QR authorization. Do not prescribe an old Tuya IoT developer subscription as an unconditional native-integration prerequisite. Missing HA functionality can reflect the Tuya SDK's exposed schema, not a broken physical device. [HA Tuya](https://www.home-assistant.io/integrations/tuya/).

LocalTuya and tuya-local are different projects, not spelling variations. Read the selected repository before generating configuration. LocalTuya documents cloud-assisted key retrieval; tuya-local documents per-device connection and profile matching. A local operational path can still have a cloud dependency for commissioning or renewed credentials. [LocalTuya](https://github.com/rospogrigio/localtuya), [tuya-local](https://github.com/make-all/tuya-local).

## Commission a local path deliberately

Record product ID, exact hardware, current firmware and vendor account region. Retrieve a local key only through an authorized account and current supported method; store it as a secret. Do not ask the user to paste it into a public issue. Reserve the device address, select the confirmed protocol, inspect readable data points, then match a profile. Verify one safe command and its reported state before configuring all entities.

The tuya-local documentation notes that pairing again changes the key. It also distinguishes protocol versions whose wrong keys can allow initial status but break commands from newer versions that fail during decoding. Re-pairing without updating a stored key is therefore a concrete diagnostic branch. [tuya-local connection documentation](https://github.com/make-all/tuya-local#configuration).

## Avoid common false fixes

- Do not run multiple active local controllers against a device while diagnosing socket/session limits.
- Do not map DP 1 to a relay or divide DP values by ten without model evidence.
- Do not label a battery Wi-Fi sensor as suitable for continuous local polling; verify its wake behavior and supported protocol.
- Do not factory-reset to test a key until the current state, account binding and recovery plan are recorded.
- Do not flash Tasmota/ESPHome based on the retail name; chips and PCB revisions can change. Route firmware work to `smart-home-esphome-mqtt` with verified hardware.

## Internet-blocking test

After normal operation is established, test only the necessary dependency under explicit task scope. Verify startup after a device reboot, recovery after HA restart, time-dependent schedules, DNS/NTP requirements and cloud token/key renewal. A command working for five minutes without WAN does not establish permanent cloud independence. Preserve the vendor app recovery route until local operation is demonstrated.

## Updating and removal

Back up the custom integration and config, record the version, and pilot a change on one noncritical device. Stop automations that may command through both old and new routes. Remove the previous integration only after remapping entity IDs and validating manual control, unavailable states and power restoration. Use `home-assistant-hacs` for trust, repository provenance and rollback; this reference establishes which project and device path is appropriate.

## Historical firsthand key-handling report

[LocalTuya issue 1380](https://github.com/rospogrigio/localtuya/issues/1380), opened 2023-05-07, described decryption errors after Smart Life reactivation produced differently formatted keys. Exact hardware and integration versions were not given. The reporter subsequently marked it resolved and linked change 1381; inspect that change before claiming a fixed release. The useful diagnostic lesson is to check key parsing, protocol and integration version as well as key identity. It is not evidence that the old defect persists in current releases.
