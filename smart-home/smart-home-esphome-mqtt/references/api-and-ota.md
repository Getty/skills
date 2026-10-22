# Native API, encryption and OTA

## Distinguish access channels

The [native API](https://esphome.io/components/api/) is the HA/device communication channel. The ESPHome OTA service updates firmware. A web server, captive portal, MQTT and serial bootloader are separate interfaces with their own exposure and recovery implications.

Use unique device keys, retain the key HA actually provisioned, and restrict network access. `secrets.yaml` avoids repeating secrets in a config but is still a sensitive plaintext file. Keep it out of public repositories. Follow the current [security guidance](https://esphome.io/guides/security_best_practices/) for supported protections.

## Version-aware encrypted OTA

Published [ESPHome 2026.9 release guidance](https://esphome.io/blog/2026/09/16/esphome-2026-9/) introduced encrypted OTA capability; [2026.10 release guidance](https://esphome.io/blog/2026/10/21/esphome-2026-10/) adds further migration handling. The running firmware and the uploader both matter. Updating an old image is not magically encrypted before that image can negotiate encryption.

For a new device flashed over a controlled serial path using a compatible current release, the pattern is:

```yaml
api:
  encryption:
    key: !secret lab_sensor_api_key

ota:
  - platform: esphome
    encryption:
```

The OTA encryption block can inherit the API key. For an already deployed device, follow the [current OTA migration procedure](https://esphome.io/components/ota/esphome/) rather than pasting this final-state fragment over an old password configuration. Preserve the old authentication until the running image can accept the transition. Newer tools can refuse a plaintext upload when encryption is required; that is not evidence the device is broken.

A documented one-install plaintext migration option exists in current releases. Use it only when the exact migration requires it, within the agreed trusted maintenance path, then remove it. Never silently weaken encryption to make an upload succeed. If the required key is lost, inspect supported physical recovery instead of guessing or replacing keys blindly.

## Define disconnect behavior

Native API reboot timeout can deliberately recover a disconnected device. It can also cause periodic restarts when firmware declares an API that nobody uses. For MQTT-only designs, remove the API or intentionally set its timeout according to the [MQTT component warning](https://esphome.io/components/mqtt/). An API timeout change does not change an independent Wi-Fi or MQTT timeout.

Do not disable all recovery timers reflexively. Decide which control must keep working without HA and verify the chosen behavior on a low-risk test unit.

## Recover from failed application startup

[Safe mode](https://esphome.io/components/safe_mode/) keeps a reduced recovery environment after repeated boot failures. It does not repair wrong wiring, power instability or a missing bootloader. Capture serial logs, identify the earliest failure, and recover with a known-good compatible build. Preserve source/configuration, credentials and update procedure alongside the firmware image.
