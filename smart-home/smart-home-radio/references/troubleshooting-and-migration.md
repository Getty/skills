# Diagnose and migrate without losing the home

## Start with the smallest distinguishing observation

| Symptom | First comparison | Avoid |
|---|---|---|
| One sensor stops reporting | Expected report interval, battery, parent, raw packet/event | Resetting the coordinator |
| All devices disappear | Owner process, radio transport, power, broker/server | Re-pairing every device |
| Device pairs but lacks functions | Signature, quirk/converter and firmware | Assuming a stronger antenna fixes unsupported data |
| Commands work but buttons do not | Actual emitted events and binding support | Inventing event IDs |
| Matter appears but cannot control | IPv6 routing/session/fabric and server | Disabling IPv6 |
| BLE API connected but target fails | Advertisement/GATT distinction, free slots and firmware | Treating proxy Wi-Fi health as proof of BLE health |
| Repeated duplicate actions | Competing stacks/automations and duplicate entities | Adding retries without idempotency |

Log a short reproducible window and redact secrets. State the installed versions and last working configuration. Consult current upstream alerts and exact-model issues before trying an old workaround.

## Define a migration package

Preserve network backups, application databases/configuration, radio identities, firmware versions, device signatures, groups/bindings, entity mapping and the original topology. Keep secret material separately protected. Identify the tested restore target before making the change.

For ZHA-to-Z2M or the reverse, verify current interoperability for the actual adapter families and tool versions. Do not promise that importing a coordinator backup transfers all application knowledge, entity IDs, automations or vendor quirks. Plan for re-pairing when the official procedure requires it.

## Migrate one controlled domain

1. Choose one network or room and a maintenance window.
2. Capture baseline control and battery-device reporting.
3. Stop the old owning application and prevent automatic restart.
4. Perform the supported migration or explicit re-pair sequence.
5. Confirm no second application or radio has the same live identity.
6. Validate actuator control, button events, sensors, secure functions and HA entity mappings.
7. Verify recovery after restarting the new owner.
8. Keep the old backup until the new path has passed the agreed observation period.

Restore the whole relevant state when rolling back; avoid combining an old radio backup with an incompatible new application database without checking the migration documentation.

## Apply OTA as a separate change

Record image source, matching model/hardware, battery/power prerequisites, recoverability and documented warnings. Updating all sleepy devices at once can create avoidable traffic and uncertainty. Firmware may not be downgradeable. If an exact device page reports bricking, hold that update and verify the affected fingerprint and issue before proceeding.

Direct linking/binding, event behavior and measurement should be tested after the update. Do not use a successful progress bar as the sole acceptance criterion.

Primary procedures: [ZHA](https://www.home-assistant.io/integrations/zha/), [Zigbee2MQTT FAQ](https://www.zigbee2mqtt.io/guide/faq/), [Zigbee2MQTT OTA](https://www.zigbee2mqtt.io/guide/usage/ota_updates.html), [Thread](https://www.home-assistant.io/integrations/thread/) and [Z-Wave](https://www.home-assistant.io/integrations/zwave_js/).
