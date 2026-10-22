# Operate Zigbee2MQTT

## Keep the ownership chain explicit

Zigbee2MQTT owns the Zigbee coordinator and publishes through an MQTT broker; HA consumes MQTT discovery/state. Confirm all three services independently. The HAOS app and a separately hosted container are deployment alternatives; HACS does not supply the radio runtime.

The current [adapter list](https://www.zigbee2mqtt.io/guide/adapters/) recommends zStack, EmberZNet and deCONZ families but notes different backup support. Use the [adapter settings](https://www.zigbee2mqtt.io/guide/configuration/adapter-settings.html) for the exact hardware and firmware. Do not copy an old `ezsp` configuration onto a current `ember` deployment without checking migration requirements.

## Configuration fragments

These are parts of Zigbee2MQTT's own `configuration.yaml`, not HA's file:

```yaml
homeassistant:
  enabled: true
```

The syntax is documented by [HA integration through MQTT discovery](https://www.zigbee2mqtt.io/guide/usage/integrations/home_assistant.html). Configure the broker and persistent serial/network endpoint for the deployment. Use the current project's supported secret mechanism and protected files; do not paste broker passwords into shared examples.

For a new installation only, create fresh network credentials through the documented setup. For an existing installation, preserve `network_key`, PAN information, coordinator identity and data directory. Replacing a working key with `GENERATE` is a network migration, not a harmless cleanup.

## Read the actual exposes

Open the exact model page and device's live exposes. Match full manufacturer identity, endpoints and options; do not use a generic Tuya DP map. Determine whether the field is reported, readable, writable, or startup-only. Units and scaling can differ even between similarly named plugs.

Use the frontend or documented [MQTT topics/messages](https://www.zigbee2mqtt.io/guide/usage/mqtt_topics_and_messages.html) for a bounded operation. Avoid publishing retained actuator commands. Do not repeatedly request state from sleeping battery sensors expecting immediate response.

## Diagnose by boundary

| Observation | Next check |
|---|---|
| Adapter will not initialize | Port ownership, firmware/adapter driver, permissions, stable serial identity |
| Z2M sees device, HA does not | Broker connection, discovery enabled, integration subscription, retained discovery and logs |
| HA entity exists but remains stale | Device reporting, availability settings, broker traffic and parser/converter |
| One feature is missing | Exact exposes/converter support, firmware and datapoint mapping |
| Everything disconnects together | Host, coordinator transport, power, broker and shared network dependencies |

## Update and restore deliberately

Back up the complete persistent data and radio backup before upgrading. Check both software and coordinator firmware compatibility, then read [FAQ/migration guidance](https://www.zigbee2mqtt.io/guide/faq/). Firmware backups and application database files serve different purposes. Never assume a backup from any adapter family restores to any other without pairing work.

Use `smart-home-esphome-mqtt` for broker/discovery semantics and `smart-home-devices` for exact device OTA warnings, including the matching TS0201 variant. Prefer the narrowest supported converter change; pin a community external converter and keep its removal path documented.
