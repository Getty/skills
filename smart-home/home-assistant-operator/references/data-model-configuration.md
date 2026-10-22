# Data model and configuration

## Identify the object

| Object | Meaning | Common mistake |
| --- | --- | --- |
| Integration domain | Software for a technology/service | Treating it as one login/device |
| Config entry | Configured integration instance | Deleting it to remove one entity |
| Device record | Group for a physical/logical device | Counting every record as physical hardware |
| Entity | Measurement, control, or event | Assuming one device has one entity |
| Entity ID | Current address such as `sensor.kitchen_temperature` | Assuming an immutable hardware identity |
| Unique ID | Stable integration-provided identity | Changing it in a refactor and creating duplicates |
| Area/floor/label | Organization and targeting | Treating organization as authorization |

Config entries have setup/retry/reauth/unload/migration lifecycles. Entity records preserve customization when proper unique IDs exist. Device identifiers/connections group related entities. Consult the contracts for repair or development. [Config entries](https://contributors.home-assistant.io/core/integrations/config-entries/), [entity registry](https://contributors.home-assistant.io/core/entities/registry/), [device registry](https://contributors.home-assistant.io/core/integrations/device-registry/).

## Establish ownership

Classify settings as UI-managed, supported YAML, dashboard, HAOS app, external service, or vendor firmware/cloud. That determines the reload/restart and backup boundary. Prefer the integration's supported config flow; check historical `platform:` examples before reuse. [YAML integration policy](https://developers.home-assistant.io/docs/configuration_yaml_index/).

Never edit `.storage` while HA runs. It is application state, not a general public API. Exceptional repair requires diagnosed corruption, stopped HA, backup, and a narrow reversible patch preserving related records.

## Handle duplicates

Identify deliberate parallel paths first: Hue native plus Matter, Shelly native plus MQTT, phone randomized MACs, direct camera plus NVR. Record capabilities, automation references, and statistics before choosing the survivor. Disable the redundant path in stages; observe dependents. Renaming an entity is not equivalent to merging histories and statistics. Do not promise integration deletion/recreation preserves IDs.

Use stable semantic IDs and human-friendly names. Maintain a physical-label → model/firmware → integration → entity → room mapping. Distinguish disabled entities, hidden cards, unavailable states, and unsupported features. `/api/states` only contains loaded states; it cannot establish that the registry contains no disabled entities.
