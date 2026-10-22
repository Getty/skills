# Troubleshooting, acceptance and sources

## Isolate one layer

| Observation | First evidence | Next controlled check |
|---|---|---|
| Validation fails | Exact ESPHome version and first configuration error | Resolve schema/component compatibility before building |
| Compile fails | First compiler/linker error and dependency revisions | Compare minimal baseline; check flash/RAM target |
| Board boot-loops | Serial log, reset reason, power and pin map | Remove newly added component on a bench unit |
| Wi-Fi works, HA API fails | API key, port reachability, client log | Compare provisioned key without printing it |
| OTA upload refused | Running firmware, uploader version and handshake | Follow encrypted OTA migration; preserve known authentication |
| MQTT connected, entity missing | Discovery topic/payload and HA MQTT diagnostics | Verify prefix, unique ID and entity enablement |
| Value becomes stale | Publication interval, retained flag, source time and availability | Test expiry and HA restart with a stopped producer |
| Periodic device restart | API, Wi-Fi and MQTT timeout configuration | Identify which disconnected client triggers recovery |
| BLE advertisements arrive but commands fail | Active connection use and exact device support | Test one connection on a nearby supported proxy |

Avoid clearing all broker persistence, resetting a device, or reinstalling HA as an initial diagnostic. Capture one failing transaction and change one relevant variable.

## Acceptance scenarios

Verify boot, HA restart, broker restart if used, network interruption, stale data, command duplication and recovery from a failed update. For a physical control, include manual override and behavior while HA is unavailable. A clean compile does not prove correct wiring or safe startup state.

For the included lab YAML, validation can establish schema consistency and compilation can establish buildability for the configured board. Hardware behavior still requires the intended board and actual credentials. Do not call a YAML parser result an ESPHome compile or hardware test.

## Dated firsthand evidence

**ESP32 active BLE regression, 2026-08-22.** The original reporter in [esphome/esphome #18614](https://github.com/esphome/esphome/issues/18614) described active BLE failures on ESP32-WROOM after 2026.8 while Wi-Fi/API remained available; the same board/configuration reportedly worked on 2026.7.2. The issue was closed as completed on 2026-08-23 with a link to #18609. This is a historical reproduction lead, not evidence that all current proxies require a downgrade. Inspect the linked resolution and installed version before prescribing a workaround.

Use original reports with model, version, reproduction and outcome. A compilation failure on a different chip or an abandoned third-party fork does not establish a defect in the current built-in component. For new failures, use the evidence format in `smart-home-architecture`.

## Primary source map

Research baseline **2026-10-22**. Reopen the exact release documentation before running commands or deploying firmware.

| Subject | Source |
|---|---|
| CLI and validation/build/upload boundaries | [ESPHome CLI](https://esphome.io/guides/cli/) |
| YAML types, substitutions and secrets | [Configuration types](https://esphome.io/guides/configuration-types/) |
| Native API | [API component](https://esphome.io/components/api/) |
| Current encrypted OTA contract | [ESPHome OTA](https://esphome.io/components/ota/esphome/) |
| Release context | [2026.9 announcement](https://esphome.io/blog/2026/09/16/esphome-2026-9/) · [2026.10 changelog](https://esphome.io/changelog/2026.10.0/) |
| Recovery and protection | [Safe mode](https://esphome.io/components/safe_mode/) · [Security guidance](https://esphome.io/guides/security_best_practices/) |
| MQTT device behavior | [ESPHome MQTT](https://esphome.io/components/mqtt/) |
| HA discovery and sensor semantics | [HA MQTT](https://www.home-assistant.io/integrations/mqtt/) · [MQTT sensor](https://www.home-assistant.io/integrations/sensor.mqtt/) |
| Broker configuration | [Mosquitto manual](https://www.mosquitto.org/man/mosquitto-conf-5.html) · [Authentication](https://www.mosquitto.org/documentation/authentication-methods/) |
| Transport semantics | [OASIS MQTT 5](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) |
| Dependencies | [External components](https://esphome.io/components/external_components/) |
| Lab example platform/sensors | [ESP32](https://esphome.io/components/esp32/) · [Uptime](https://esphome.io/components/sensor/uptime/) · [Status](https://esphome.io/components/binary_sensor/status/) |

Use the hardware reference for UART, IR and BLE sources. Exact firmware and dependency releases are observations to refresh, not permanent defaults.
