# Build and deploy firmware deliberately

## Establish hardware identity

Record the actual MCU family, module, board revision, flash/PSRAM, supply, GPIO assignments, existing image and bootloader. A retail SKU may change internally without its title changing. Separate ESP32/ESP8266, BK72xx/RTL87xx and other supported targets; do not flash an ESP binary onto another chipset.

For a working Shelly, SONOFF or Tuya product, compare native integration, local vendor API and firmware replacement first. Flashing can lose factory calibration, vendor features, account provisioning or a recovery path. Keep an original dump where lawful and technically possible; do not claim it guarantees recoverability.

Use development boards and low-voltage test loads for experiments. Do not connect programming equipment to a mains-powered device unless its isolation and safe service procedure are established. A correct YAML pin number does not establish a safe electrical connection.

## Keep a reproducible project

Maintain configuration, secrets separately, ESPHome version, board/framework choice, dependency revisions and known-good output. Use [configuration types](https://esphome.io/guides/configuration-types/) and the exact component schema. Distinguish substitutions, packages, IDs, entity names and HA entity IDs.

Use the Device Builder or the documented [CLI](https://esphome.io/guides/cli/):

```bash
esphome version
esphome config lab-sensor.yaml
esphome compile lab-sensor.yaml
```

These are build/validation stages, not proof of hardware behavior. Validation/build can fetch and execute custom dependencies; review them before running. Keep output containing secrets private. Upload only to an explicitly identified device after validating the image and recovery path.

## Choose runtime ownership

Use the native API for ordinary HA integration where it meets the requirement. Use MQTT for independent consumers or an existing messaging architecture. Avoid duplicate native and MQTT entities unless intentional. Specify which path writes outputs and how a lost connection affects the firmware.

Keep necessary physical behavior on the device when appropriate: a wall button should not require a cloud round trip to operate its nearby light. For heating, pumps or covers, define failure behavior based on the actual equipment, not a generic “restore last state” rule.

## Deploy one representative unit

1. Confirm device identity and recovery access.
2. Validate/compile against the intended released version.
3. Confirm credentials and API/OTA migration compatibility.
4. Install during an agreed window; retain logs and the previous known-good configuration.
5. Test sensor units/calibration, manual controls, HA entities, loss of HA/broker, device reboot and power return.
6. Verify a subsequent update works before adopting the process for a fleet.

Do not erase flash or reset credentials as the first response to a communication failure. Capture logs while the failure is present and isolate Wi-Fi, API, broker and application behavior separately.
