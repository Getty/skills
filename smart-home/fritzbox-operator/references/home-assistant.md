# Home Assistant integration routes

## Choose the correct integration

| Integration / domain | Role | Prerequisites to verify |
| --- | --- | --- |
| FRITZ!Box Tools / `fritz` | Router state, network tracking, selected controls | App/TR-064 access, UPnP status setting, settings permission, correct router/repeater account |
| FRITZ!SmartHome / `fritzbox` | Thermostats, plugs, supported lights/covers, templates, routines, ancillary sensors | Smart Home right, supported endpoint, correct master in a mesh |
| FRITZ!Box Call Monitor / `fritzbox_callmonitor` | Live call state and optional name resolution | Activated local TCP monitor; credentials/telephone-data rights for optional phonebook lookup |

Use the setup screens documented by [Tools](https://www.home-assistant.io/integrations/fritz/), [SmartHome](https://www.home-assistant.io/integrations/fritzbox/), and [Call Monitor](https://www.home-assistant.io/integrations/fritzbox_callmonitor/). `FRITZ!DECT` is an older product/integration naming cue; do not invent a fourth current domain called `fritzdect` merely because a tutorial uses that name.

The native SmartHome route currently polls at 30 seconds. It can expose auxiliary readings from some event-oriented devices while lacking their principal button/contact events. That is a capability limitation, not a broken card. In a mesh, follow the documented master-oriented configuration rather than adding every radio base and creating duplicate representations. [SmartHome data and limitations](https://www.home-assistant.io/integrations/fritzbox/)

## Inspect actual entities

Export or inspect the device/entity registry and integration diagnostics. Record entity ID, unique ID, device, integration, enabled/disabled status, supported features, availability, and last update. Do not assume an entity ID from a model name; users rename entities, and duplicate integrations can add suffixes.

Separate diagnostic entities from automation inputs. Enabling every possible entity on a large list of known network hosts creates clutter and history volume. Decide which hosts matter for presence, which need connectivity alerts, and which need no HA representation. A router can keep historical DHCP/host entries after a device stops participating.

Use native entity actions such as `climate.set_temperature`, `switch.turn_on`, or `button.press` against observed entities. Check available actions in the installed HA release instead of copying obsolete service names. Generic capability examples should not include a reboot/reconnect target unless that is the requested action.

## Preserve identity and ownership

Before reconfiguring the integration, save its current entry settings and affected entity mappings. Prefer reauthentication/reconfiguration over deleting and re-adding a working entry. Before changing the router IP, DNS, or mesh master, record how HA reaches it and how discovery can update the address.

If native FRITZ and Matter both expose the same physical device, mark one path as the active control route. Keep alternate entities clearly named and excluded from general automations unless intentionally used for comparison. Two paths can differ in diagnostic richness and update timing without either being universally superior.

## Diagnose one layer at a time

| Comparison | Interpretation to test |
| --- | --- |
| Device works physically and in FRITZ UI, not HA | Endpoint, authentication, coordinator, library, capability mapping |
| Device absent in FRITZ UI too | Power, battery, pairing, radio base, range |
| All smart-home entities fail at once | Router session/transport/integration, not simultaneous device failure |
| Only one class fails | Model fields, capability bitmask, unsupported feature, firmware-specific payload |
| Tracking fails but thermostats work | Tools/TR-064 path distinct from AHA |
| Router works by IP but not hostname | HA runtime's DNS and discovery-selected host |

Record the earliest exception and the elapsed operation time. A reauthentication prompt does not prove that the password changed; a connection or discovery failure may have preceded it. The September 2026 host-resolution report and October 2026 SSDP fix in [community evidence](community-evidence.md) illustrate why this distinction matters.

## Check the installed source when needed

For HA 2026.10.2, the [manifest](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/fritzbox/manifest.json) specifies `pyfritzhome==0.6.21` and `local_polling`. The [coordinator](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/fritzbox/coordinator.py) centralizes device/template/trigger refresh. Treat this as a dated implementation observation, not a permanent guarantee. Recheck the release tag before diagnosing a future version, and avoid replacing a packaged dependency inside a live HA installation.
