# Route a smart home task

## Skill boundaries

| Skill | Owns | Typical request |
|---|---|---|
| `smart-home-architecture` | Whole-home tradeoffs, inventory, procurement, dependency/failure analysis | “What should I add, retain, or replace?” |
| `home-assistant-operator` | Installation, backup, restore, integrations, APIs, diagnostics, development and access | “HA is slow; inspect the cause and plan a repair.” |
| `home-assistant-automations` | YAML, templates, helpers, scripts, dashboards, climate, presence, energy, voice/AI policy | “Build a heating rule that survives a restart.” |
| `home-assistant-hacs` | HACS lifecycle, community integrations/cards, extension selection and rollback | “Which extension solves this missing capability?” |
| `fritzbox-operator` | FRITZ! network, provider firmware, TR-064, AHA/REST, DECT, telephone/NAS/VPN integration | “What can my cable FRITZ!Box expose and control?” |
| `smart-home-radio` | ZHA/Zigbee2MQTT, Zigbee topology, Matter/Thread, BLE, Z-Wave, RF diagnosis | “These battery sensors keep disappearing.” |
| `smart-home-devices` | Exact models, vendor families, integration routes, firmware caveats and firsthand evidence | “Will this Tuya/Aqara/Shelly variant actually work?” |
| `smart-home-video-media` | Reolink/NVR/chime, RTSP/ONVIF, Frigate/go2rtc, LG/Fire TV and other cameras/media | “Video works but the doorbell event never arrives.” |
| `smart-home-esphome-mqtt` | Device firmware, native API, MQTT, discovery, custom components and device recovery | “Make a local sensor bridge without a vendor cloud.” |

Load adjacent skills for interfaces between domains, rather than copying entire references. The suite remains usable when only one skill is installed: name a missing companion and continue with the local reference's boundary information.

## Multi-domain procedure

For a leak response, identify the exact sensor in the device skill; diagnose its radio in the radio skill; design latching/acknowledgement and valve behavior in the automations skill; check durable restoration with the operator skill. Treat a silent sensor and a dry sensor as different states.

For FRITZ heating, establish FRITZ-side schedules and supported API data. Then decide whether HA adjusts setpoints or owns an outer control loop. Prove the need for an additional thermostat controller before installing one.

For a Reolink installation, map every NVR and the doorbell channels before adding integrations. A duplicate camera through direct access and an NVR is two software paths to one physical camera, not redundancy by itself.

For a new Amazon product, start with the listing variant and exact requirement, then resolve its protocol and firmware. Vendor-family references narrow the search; the current model page, integration, and relevant issue history make the decision.

## Keep the installation portable

Use stable human names for areas and functions. Keep hardware identity separate from the entity name chosen for automations. Document which physical device fulfills a role so a failed plug can be replaced without reconstructing every rule. Capture configuration exports through their supported route; do not edit internal registries as the normal migration mechanism.

This routing is an organizational design for the collection, not a statement that a vendor requires all these software layers.
