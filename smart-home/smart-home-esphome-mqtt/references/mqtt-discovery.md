# MQTT discovery and entity lifecycle

## Define identity before publishing

Use the [HA MQTT discovery contract](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery) that matches the installed release. Discovery config describes an entity; a state topic carries observations; an availability topic describes producer connectivity. Treat these as separate contracts.

For a simple sensor, the component discovery topic has the shape `homeassistant/sensor/<object_id>/config`. The discovery prefix is configurable. Use an immutable `unique_id` and a stable `device.identifiers` value. Renaming a friendly label must not manufacture a second physical device. Multiple sensors on one device share its device identifier and have distinct entity unique IDs.

Inspect `assets/mqtt-sensor-discovery.json` as a single-sensor example. Adapt every lab identifier before publishing to a real broker. Its proposed discovery topic is `homeassistant/sensor/lab_sensor_01_temperature/config`, with state at `house/lab_sensor_01/state`. A state payload could be `{"temperature":21.4}`. The example assumes a fresh reading at least every minute and expires after five minutes; change both to match actual hardware behavior.

## Keep state trustworthy

Set device class, unit and state class from physical meaning. A temperature is a measurement; a lifetime energy meter and a resettable counter have different statistics semantics. Do not add `total_increasing` merely to make an entity selectable in an Energy dashboard.

The [MQTT sensor documentation](https://www.home-assistant.io/integrations/sensor.mqtt/) explains that retained state is replayed on subscription. With `expire_after`, replay can make an old value appear newly received after HA restarts. For the included example, publish sensor state **without retain**, use producer last-will availability, and republish a current measurement on reconnect. Retain discovery configuration if that is the chosen lifecycle. Do not describe broker receipt time as sensor measurement time.

For richer producers, carry a source timestamp/sequence in the payload and explicitly reject stale readings. Design the missing-value case; do not use a blanket numeric fallback that turns an invalid payload into a plausible zero.

## Exercise the full lifecycle

1. Inspect a bounded sample of the exact discovery, state and availability topics.
2. Validate the JSON shape and identity locally.
3. Publish one selected discovery config only after the broker and namespace are agreed.
4. Publish a fresh measurement and confirm entity, units and device grouping.
5. Restart HA, reconnect the producer, interrupt its network, and observe stale-state handling.
6. Rename only the display name and verify that history/identity remain associated as intended.

Producers can republish discovery following HA's birth message rather than relying only on retention. Read the current discovery guidance for birth/will behavior and newer device-level discovery formats; do not mix two discovery formats for the same entity without a migration plan.

## Remove and migrate deliberately

An empty retained payload on a selected discovery topic removes that retained configuration. It is a mutation, not a read-only diagnostic. List exact topics first; do not delete all retained messages to fix one duplicate entity. A device that republishes obsolete discovery will recreate it until its configuration is corrected.

When changing sensor state from retained to non-retained, the producer's new retain flag does not erase an old retained broker value. Stop that producer's retained publication, remove only the old retained message on its exact **state** topic with an empty retained payload, then publish a fresh non-retained measurement. Keep its discovery configuration intact. Verify by restarting HA with the producer temporarily offline: the obsolete measurement must not return as fresh.

When changing identity, record old and new unique IDs and downstream entity references. Verify dashboards, automations and statistics after migration. For broad entity-registry cleanup, use `home-assistant-operator` rather than editing HA storage files by hand.
