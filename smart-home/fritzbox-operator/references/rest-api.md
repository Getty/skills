# FRITZ! Smart Home REST API

## Version boundary

Read the [FRITZ interface index](https://fritz.com/pages/schnittstellen) and match a published API specification to the router's deployed firmware. The 8.50 document is linked with publication date 2026-10-01; its schema identifies API version 1.0.0 and records an earlier 0.9.5 interface for FRITZ!OS 8.20. A schema version, the URL base `api/v0`, and the FRITZ!OS version are separate identifiers. Do not infer Vodafone rollout from document availability.

Primary machine contract: [8.50 OpenAPI YAML](https://fritz.support/resources/SmarthomeRestApiFRITZOS85.yaml). Human reference: [8.50 rendered documentation](https://fritz.support/resources/SmarthomeRestApiFRITZOS85.html). Use the [8.20 reference](https://fritz.support/resources/SmarthomeRestApiFRITZOS82.html) for that firmware, rather than assuming all 8.50 operations are available.

## Authentication and object model

The OpenAPI security scheme uses an FRITZ SID in the header:

```text
Authorization: AVM-SID <session-id>
```

Its default server origin is HTTPS and base path is `/api/v0`. `/smarthome/overview` exposes devices, units, groups, templates, triggers, and global state. `/configuration` and `/connect` need stronger rights than the basic smart-home overview. `/connect` enrollment is radio pairing, not an SSE/WebSocket event feed. The specification also lists geofence endpoints; do not assume a generic external geofence client is equivalent to the supported FRITZ app registration. [OpenAPI security scheme and paths](https://fritz.support/resources/SmarthomeRestApiFRITZOS85.yaml)

Keep physical-device identity distinct from the functional unit. Group control can affect multiple physical endpoints; thermostat groups need special attention because an individual thermostat command may propagate within the group. The [rendered overview/group sections](https://fritz.support/resources/SmarthomeRestApiFRITZOS85.html) describe those semantics. Do not route a device UID into a unit endpoint by constructing an imagined suffix.

## Build a read-only proof first

1. Record actual firmware and observed HTTPS origin.
2. Establish a SID with only the rights needed for the read.
3. Request `GET /api/v0/smarthome/overview` once, with a timeout and validated TLS.
4. Record response status, schema shape, and capability names without printing SID or complete household inventory.
5. Choose one known device and compare a returned reading to the FRITZ UI.
6. Store a sanitized fixture and implement parsing tests for missing interfaces, disconnected devices, unknown enum values, and empty lists.

A successful overview is evidence for that endpoint, not proof of write rights or support for every schema variant. A 404 may indicate firmware/path mismatch; an authorization error must be resolved separately from a network timeout.

## Prepare writes as explicit commands

Generate typed request models from the matching schema where useful, then add application-level constraints. Do not let a generated client expose unrestricted delete/configuration commands to an LLM by default. Define a narrow command such as `set_room_target(room, degrees, until)` and validate its targets against an inventory allowlist.

Before a write, capture the relevant current values and dependencies. Check device capability, entity/UID identity, group membership, manual override, and expiry. Send only the intended fields; do not round-trip an entire GET response into a PUT without checking read-only fields and replacement semantics. Treat transport retry after a lost response as an uncertain result, then read back before repeating an operation with side effects.

## Migrate AHA deliberately

Run read-only comparison during a short observation period. Match devices by discovered identity, not list order or display name. Compare value units and timestamps, normalize enum states, and account for grouped devices. Keep one active writer during the cutover. Retain a fallback route until the new client has passed startup, reconnect, SID-expiry, device-unavailable, and schedule-boundary checks.

Do not equate the existence of REST with a current HA migration. The inspected [HA 2026.10.2 manifest](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/fritzbox/manifest.json) still names `pyfritzhome==0.6.21`; the [coordinator](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/fritzbox/coordinator.py) uses 30-second polling. Verify future releases before changing this conclusion.
