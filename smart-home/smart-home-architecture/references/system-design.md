# Design control ownership and failure boundaries

## Separate five layers

| Layer | Examples | Failure question |
|---|---|---|
| Physical behavior | Valve, relay, thermostat, lamp, door lock | What does it do without software or after power returns? |
| Transport | DECT, Zigbee, Thread, BLE, Ethernet/Wi-Fi | What remains reachable if one router/bridge fails? |
| Device integration | FRITZ, Hue, Shelly, Reolink, MQTT | Does an event or command need LAN, cloud, or both? |
| Policy | Schedule, occupancy, quiet hours, frost limit | Which controller decides, and how is manual override respected? |
| Presentation | Dashboard, phone, wall control, voice | Can residents still use essentials if this is unavailable? |

Compare actual functions and recovery work before replacing a working local bridge. Native integration, a Matter bridge, and direct Zigbee can expose different capabilities. Evaluate the required feature list rather than a single compatible flag. Primary interfaces: [Matter](https://www.home-assistant.io/integrations/matter/) and [ZHA](https://www.home-assistant.io/integrations/zha/).

## Assign one policy owner per variable

Write a control contract for heating, lighting adaptation, covers, or irrigation:

1. State the owned variables, for example target temperature and operating mode.
2. Identify writers: FRITZ schedule, HA automation, physical dial, vendor app, voice, adaptive integration.
3. Define priority, manual override lifetime, expiry behavior and resynchronization after restart.
4. Define stale-input behavior independently of the ordinary happy path.
5. Verify that a second controller is not continuously undoing the first.

Use HA for coordination across otherwise working subsystems. A sensible initial design is to retain working native subsystems — for example FRITZ heating fallback and Hue room controls — while proving which cross-vendor behaviors add value. This is an engineering starting point, not a claim about any particular topology.

## Prefer replaceable boundaries

Expose a role such as hall occupancy or water alarm behind a helper/group where appropriate. Keep raw sensors available for diagnosis. Document which hardware and evidence produce that role. Do not make an abstraction conceal stale data or sensor disagreement.

Maintain one discovery owner for a device unless duplicate paths are deliberate. A device can appear through native, Matter, MQTT and a cloud bridge. Document why each is retained and which entity an automation uses; otherwise imports can produce duplicate commands and misleading counts.

## Choose autonomy deliberately

| Function | Useful independent fallback | HA's added role |
|---|---|---|
| Heating | Valid thermostat schedule and physical control | Presence/window coordination, monitoring and bounded adjustments |
| Lighting | Wall button or tested direct binding/group | Cross-vendor scenes and occupancy rules |
| Doorbell | Native chime still rings | Phone/TV notifications, snapshots and quiet hours |
| Leak detection | Local audible alarm where supported | Escalation, persistent alert and tested valve action |
| Camera recording | NVR or camera recording independent of HA UI | Event coordination and optional additional analytics |

A backup does not itself create active redundancy. Two instances writing to the same radio or actuator can make recovery worse. Prefer documented cold recovery unless a product explicitly supports coordinated failover.

## Make costs comparable

Record device, bridge, power supply, installation, subscriptions, batteries, maintenance, and exit/migration effort. Avoid numerical reliability or lifetime claims without measurements. Include what residents lose if a vendor account or service disappears.

Evaluate HA [LLM APIs](https://contributors.home-assistant.io/core/internals/llm-api/) separately from [MCP Server](https://www.home-assistant.io/integrations/mcp_server/) configuration. An administrative tool surface can reach beyond entities exposed to Assist; verify privileges before delegating control.
