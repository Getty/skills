# Design an MQTT boundary

## Separate broker and application meaning

The broker routes topics; it does not know that a payload means water leakage or a temperature. Document topic hierarchy, producer, consumer, schema, units, availability, security, retained-message policy and command ownership.

Example private namespace:

```text
house/lab_sensor_01/state
house/lab_sensor_01/availability
house/lamp_01/set
house/lamp_01/state
```

These are example topic names, not discovered household addresses. Keep stable device IDs in topics and human-friendly names in presentation. Avoid exposing room occupants or personal names when machine identity is sufficient.

## Choose delivery semantics deliberately

The [OASIS MQTT 5 standard](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) defines delivery, retained messages and session behavior. QoS 1 can deliver duplicates. QoS guarantees do not make a physical actuator transaction exactly once. Use idempotent commands such as setting a target state; do not interpret every repeated payload as a fresh toggle.

| Message | Usual design decision | Verify |
|---|---|---|
| Discovery/config | Retain or republish on HA birth | HA can reconstruct entities after restart |
| Sensor state | Choose per freshness semantics | Old retained data cannot masquerade as a fresh reading |
| Availability | Last will + online publication | Graceful/ungraceful disconnect and retained history |
| Desired steady state | Retain only when deliberately designed | Reconnect will not reapply an obsolete hazardous state |
| Impulse/toggle/unlock/start | Do not retain | Duplicate/replay handling and authorization |

Use command IDs/expiry where the device contract supports them. Check physical state feedback separately from acknowledgement of receipt. Do not claim an optimistic switch confirms the relay position.

## Configure a protected broker

Record the installed Mosquitto version and deployment. Use authenticated listeners, per-device/service authorization, persistent data and a deliberate TLS policy. Current Mosquitto documentation includes evolving security-plugin configuration; follow the installed release's [configuration manual](https://www.mosquitto.org/man/mosquitto-conf-5.html), [authentication methods](https://www.mosquitto.org/documentation/authentication-methods/) and [ACL plugin guidance](https://www.mosquitto.org/documentation/plugins/acl-file/). Do not copy a legacy `per_listener_settings` recipe without checking its replacement.

Grant publishers only their required state/config topics and subscribers only their required commands. HA may need broader discovery/state access, but an individual plug does not. Keep anonymous internet access disabled. Restrict diagnostic subscriptions to the device namespace; a global `#` stream can expose more household data than necessary.

## Observe and recover

Check broker connection, authorized publish, payload validity, expected subscriber, then HA interpretation. Back up broker persistence, authentication/authorization configuration and certificates separately if the broker runs outside HAOS. Reconnect tests must cover retained state and duplicate commands, not just a successful TCP connection.

Use `mqtt-discovery.md` for HA semantics and `home-assistant-automations` for rule behavior. Keep the native device control path available while introducing a broker dependency.
