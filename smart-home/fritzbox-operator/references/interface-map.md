# Interface map and selection

Use this map to choose a supported control surface. Refresh the [FRITZ developer index](https://fritz.com/pages/schnittstellen) when a task depends on a recent function. Published interface documents cover firmware families; they do not prove that an individual provider device offers every listed service.

## Match the operation to the interface

| Surface | Main role | Authentication / transport | Operational boundary |
| --- | --- | --- | --- |
| TR-064 | Router status/configuration; hosts, Wi-Fi, WAN, phonebooks, NAS settings | SOAP over HTTP/HTTPS; discover descriptions and supported authentication | Home-network administration; discover actions on the actual unit |
| UPnP IGD | Gateway information and selected port mappings | Separate UPnP family; some status is unauthenticated | Do not equate all TR-064 actions with UPnP or enable automatic mapping unnecessarily |
| AHA HTTP | Existing smart-home readings and actuator commands | FRITZ SID; plain text or XML | Remains available but frozen; important for existing clients |
| Smart Home REST | Structured smart-home overview/configuration | JSON under `/api/v0/smarthome`; `Authorization: AVM-SID …` | Match specification to firmware and rights |
| Call monitor | Live telephone event stream | TCP 1012 after activation | Sensitive events; not audio, SIP registration, or full call history |
| SIP / RTP | Telephone registration and media | Separate telephone credentials/media negotiation | Management APIs do not replace telephony protocols |
| SMB/FTP/FTPS/media | NAS access and media playback | Service-specific settings/rights | Management access does not enable file service access |
| Matter bridge | Export selected devices to a Matter fabric | Matter commissioning/operational credentials | Inspect actual endpoints and features |
| TR-069 / TR-369 USP | Provider/controller provisioning | Provider/operator relationship | Not the local user API or a general HA route |
| Web UI / support pages | Interactive administration and diagnostics | Session and sometimes physical confirmation | Internal calls are not automatically a documented API |

The [TR-064 overview](https://fritz.support/resources/TR-064_Overview.pdf) identifies service documents; the [REST specification](https://fritz.support/resources/SmarthomeRestApiFRITZOS85.yaml) defines its own paths and authentication. Do not translate service names between surfaces by intuition.

## Choose the shortest reliable path

For an operation represented as an HA entity/action, use HA to centralize availability, credentials, and identity. If a documented router capability is missing, evaluate a small client or maintained custom integration. Specify the missing component: command, data field, device trigger, scheduler configuration, or timeliness. A dashboard card cannot create a missing event source.

For new smart-home clients, evaluate REST on supported firmware first. Preserve AHA compatibility when the fleet requires it. Do not migrate HA by hand-replacing its bundled Python dependency; the integration owns its expected library contract.

For network data, prefer bulk lists and an existing coordinator to independent per-entity scrapers. A process polling every host every second may create more problems than the added freshness solves. Measure API duration and failure rate before changing intervals.

## Record a capability contract

```yaml
target_model: observed-model
firmware: observed-value
provider_variant: verify-retail-or-provider-managed
operation: read-known-hosts
surface: TR-064
discovered_service_type: observed-URN
discovered_action: observed-action
required_right: documented-right
integration_exposure: observed-entity-or-not-exposed
readback: same-interface-and-ui-comparison
fallback: documented-alternate-read-path
```

Use placeholders until observed. Record negative evidence narrowly: “not advertised in this device description” differs from “the installed HA integration does not expose it.” Neither establishes that every FRITZ device lacks the function.

## Keep management paths recoverable

Identify what carries the current session: Ethernet, Wi-Fi, VPN, DNS, DHCP, or proxy. A Wi-Fi change can disconnect both target and controller. A router reboot also affects calls, cameras, presence signals, cloud integrations, and notifications. Prepare local access for changes to these shared dependencies and suppress misleading absence decisions during expected downtime.
