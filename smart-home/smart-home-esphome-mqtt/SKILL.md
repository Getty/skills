---
name: smart-home-esphome-mqtt
description: "Use when writing ESPHome YAML, flashing or recovering an ESP32, ESP8266 or LibreTiny device, OTA or safe mode, Bluetooth proxies, or designing MQTT topics, Mosquitto, discovery, retained messages and availability for Home Assistant."
---

# Smart Home ESPHome and MQTT

Treat firmware, device behavior, transport, broker, discovery and HA entities as separate layers. Prefer a functioning supported native integration when custom firmware provides no required benefit.

## Work in explicit stages

1. Resolve the exact board/chip, flash size, power design, pin map, existing firmware and recovery access. Never infer flashability from a Tuya or SONOFF brand name.
2. Select native ESPHome API, MQTT, or a documented combination according to required consumers and features. Bluetooth proxy/voice paths can require the native API.
3. Design local fail behavior, physical override, restore state, telemetry freshness and command semantics before writing firmware.
4. Validate and compile with the intended ESPHome release; inspect external dependencies first. Treat upload as a separate device-changing operation.
5. Test one representative device, reconnect/restart behavior and rollback before expanding a fleet.

## Load on demand

| Task | Read |
|---|---|
| Board identity, build, configuration and deployment | [firmware-workflow.md](references/firmware-workflow.md) |
| Native API, keys, OTA and migration | [api-and-ota.md](references/api-and-ota.md) |
| Broker, topics, commands, retained state and security | [mqtt-design.md](references/mqtt-design.md) |
| HA discovery, unique IDs and availability | [mqtt-discovery.md](references/mqtt-discovery.md) |
| Sensors, BLE/IR/serial and appliance bridges | [hardware-and-bridges.md](references/hardware-and-bridges.md) |
| External components, packages and development | [external-components.md](references/external-components.md) |
| Failure isolation, recovery and primary sources | [troubleshooting-and-sources.md](references/troubleshooting-and-sources.md) |

Adapt [esp32-lab.yaml](assets/esp32-lab.yaml) only to a matching development board and supported release. Supply unique secrets; it controls no external load. Use [mqtt-sensor-discovery.json](assets/mqtt-sensor-discovery.json) as an offline schema example; publishing it creates an entity and requires choosing the correct broker/topic first.

## Preserve these invariants

- Do not retain impulse commands such as toggle, unlock or start. Design duplicate/reconnect handling and make state reports authoritative where physical feedback exists.
- Do not turn unknown/stale telemetry into zero or a safe physical state by default.
- Use stable unique IDs and separate device identity from display names. Discovery payloads and state payloads have different lifecycles.
- Store per-device API/OTA keys and broker credentials outside shared examples. An OTA password alone does not mean the firmware transfer is encrypted.
- Check both running device firmware and build-tool version before migrating encrypted OTA. Do not remove an old password or rotate a HA-provisioned key prematurely.
- For MQTT-only firmware, remove unused API configuration or deliberately configure its reboot timeout; a missing API client can otherwise cause periodic reboots.
- Preserve hardwired/local safety behavior. Firmware interlocks and HA rules do not replace required hardware protection.

Use `smart-home-radio` for RF/proxy placement, `home-assistant-operator` for HA runtime, and `smart-home-devices` for original vendor integration alternatives.

Research baseline: **2026-10-22**, including published ESPHome 2026.9/2026.10 OTA changes. Refresh the installed schema before compiling. Distinguish text/schema checks, compiled firmware and actual hardware tests in every report.
