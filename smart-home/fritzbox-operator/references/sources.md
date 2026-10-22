# Source register and refresh procedure

Research snapshot: **2026-10-22**. Runtime code inspected at **Home Assistant Core 2026.10.2**. This skill was built from public documentation/source and reported experiences; it has not connected to or tested the user's hardware. Public API publication dates do not establish rollout to a provider-managed box.

## Official interface contracts

| Source | Use / version boundary |
| --- | --- |
| [FRITZ interface index](https://fritz.com/pages/schnittstellen) | Canonical discovery of published APIs; identifies AHA as frozen/retained and links REST |
| [TR-064 First Steps](https://fritz.support/resources/TR-064_First_Steps.pdf) | Discovery, SOAP, authentication, transport; indexed 2026-03-26 |
| [TR-064 overview](https://fritz.support/resources/TR-064_Overview.pdf) | Service families; indexed 2025-08-07 |
| [HTTP session ID](https://fritz.support/resources/HTTP_Session-ID_DE.pdf) | Modern/legacy challenge authentication, SID/rights/blocking; dated 2021-05-03 |
| [AHA HTTP interface](https://fritz.support/resources/AHA-HTTP-Interface.pdf) | Legacy smart-home commands, identifiers and units; index 2025-08-05, internal revision 1.63 |
| [REST for FRITZ!OS 8.20](https://fritz.support/resources/SmarthomeRestApiFRITZOS82.html) | Earlier REST contract; do not merge its capability set with 8.50 |
| [REST for FRITZ!OS 8.50](https://fritz.support/resources/SmarthomeRestApiFRITZOS85.html) | Human API reference; index publication 2026-10-01 |
| [REST 8.50 OpenAPI YAML](https://fritz.support/resources/SmarthomeRestApiFRITZOS85.yaml) | Machine contract; schema 1.0.0; verified AVM-SID authorization header and pairing paths |
| [Hosts](https://fritz.support/resources/TR-064_Hosts.pdf) | Hosts, mesh topology entry points; indexed 2026-01-29 |
| [Mesh topology](https://fritz.support/resources/Mesh-Topology.pdf) | Mesh data schema; index version 8.7, dated 2026-06-19 |
| [WLAN configuration](https://fritz.support/resources/TR-064_WLAN_Configuration.pdf) | Radio/SSID/AP service contract; indexed 2026-03-10 |
| [WAN IP connection](https://fritz.support/resources/TR-064_WAN_IP_Connection.pdf) | IP connection and mapping actions; indexed 2025-12-18 |
| [WAN PPP connection](https://fritz.support/resources/TR-064_WAN_PPP_Connection.pdf) | PPP-specific actions; not automatically applicable to cable |
| [Device configuration](https://fritz.support/resources/TR-064_Device_Config.pdf) | Configuration-related actions; indexed 2025-12-01 |
| [Authentication service](https://fritz.support/resources/TR-064_Authentication.pdf) | Confirmation/authentication functions; verify actual action exposure |
| [OnTel / contacts](https://fritz.support/resources/TR-064_Contact_SCPD.pdf) | Phonebooks/call-related functions; indexed 2025-08-07 |
| [VoIP](https://fritz.support/resources/TR-064_VoIP.pdf) | Telephony configuration/functions |
| [Storage](https://fritz.support/resources/TR-064_Storage.pdf) | Storage service capabilities, distinct from file access |

## HA and client implementation

| Source | Evidence |
| --- | --- |
| [FRITZ!Box Tools](https://www.home-assistant.io/integrations/fritz/) | Domain `fritz`, router services, tracking, permissions, limitations |
| [FRITZ!SmartHome](https://www.home-assistant.io/integrations/fritzbox/) | Domain `fritzbox`, native devices, mesh/master recommendation, polling/event boundary |
| [Call monitor](https://www.home-assistant.io/integrations/fritzbox_callmonitor/) | TCP call events, activation, optional phonebook lookup |
| [Webhook trigger](https://www.home-assistant.io/docs/automation/trigger/#webhook-trigger) | Methods, query variables, local-only behavior, secret IDs |
| [2026.10.2 manifest](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/fritzbox/manifest.json) | `pyfritzhome==0.6.21`, local polling |
| [2026.10.2 coordinator](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/fritzbox/coordinator.py) | Actual update interval and error handling |
| [2026.10.2 climate](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/fritzbox/climate.py) | Actual climate modes, presets, ranges and write guards |
| [2026.10.2 sensors](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/fritzbox/sensor.py) | Capabilities, measurement mapping and scheduled values |
| [python-fritzhome](https://github.com/hthiery/python-fritzhome) | Maintained client implementation; default branch is not the installed release |
| [fritzconnection](https://fritzconnection.readthedocs.io/en/latest/) | SOAP/AHA/call-monitor client; inspected docs displayed 1.15.1 |
| [October 2026 HA changelog](https://www.home-assistant.io/changelogs/core-2026.10/) | Confirm release inclusion of fixes, separate from merge date |

## Products, provider, and radio roles

| Source | Evidence / limitation |
| --- | --- |
| [Vodafone 6591 support](https://www.vodafone.de/hilfe/router/fritzbox-cable-6591.html) | Provider firmware management; do not infer retail ownership from ISP alone |
| [6591 manual hosted by Vodafone](https://www.vodafone.de/downloadarea/FRITZ%21Box_6591_Cable_Handbuch_de.pdf) | Hardware/platform context; old manual is not a current API contract |
| [FRITZ 6591 service hub](https://fritz.com/pages/service-fritz-box-6591-cable) | Current model-specific support entry point |
| [FRITZ smart-home catalogue](https://fritz.com/collections/smart-home) | Product family discovery, current rebranding |
| [Smart Gateway](https://fritz.com/en/products/fritz-smart-gateway-20003012) | Zigbee/ULE, Matter bridge, uplink and non-AP/non-telephone limitations |
| [Thermo 302](https://fritz.com/en/products/fritz-smart-thermo-302-20003120) | Native thermostat capability/context |
| [Control 440](https://fritz.com/en/products/fritz-smart-control-440-20003121) | Button/views, sensor and native control roles |
| [Control 350](https://fritz.com/en/products/fritz-smart-control-350-20003119) | Contact-sensor family |
| [Energy 200](https://fritz.com/en/products/fritz-smart-energy-200-20003113) | Plug family |
| [Energy 250 setup / meters](https://fritz.com/pages/stromsensor) | Meter-specific compatibility and setup |
| [Zigbee compatibility](https://fritz.com/pages/zigbee) | Exact model/firmware compatibility; no brand-wide inference |
| [Matter with FRITZ](https://fritz.com/pages/matter-mit-fritz) | Current 5690 Pro and Smart Gateway bridge roles |
| [September 2026 announcements](https://about.fritz.com/en/press/press-releases/2026/09/fritz-makes-the-digital-home-future-proof-new-fritzbox-genera-tion-and-more-power-for-fiber-optics-5g-mesh-wi-fi-and-the-smart-home) | New names/models and announced rollout; verify actual shipping separately |
| [302 and DECT repeaters](https://fritz.com/apps/knowledge-base/FRITZ-Smart-Thermo-302/1362_fritz-heizkorperregler-mit-dect-repeater-einsetzen) | Model-specific repeater question; dynamic page body was not reliably retrievable |
| [Thermostat schedules](https://fritz.com/en-fr/apps/knowledge-base/FRITZ-DECT-301/4354_Configuring-a-schedule-for-FRITZ-radiator-controls) | Model-scoped UI procedure; dynamic-body retrieval limitation |
| [Thermostat temperature adjustment](https://fritz.com/apps/knowledge-base/FRITZ-DECT-301/3422_am-fritz-heizkorperregler-gemessene-temperatur-anpassen) | Offset/measurement question; verify actual firmware UI |
| [6591 guest isolation](https://fritz.com/de-at/apps/knowledge-base/FRITZ-Box-6591-Cable/549_kein-zugriff-auf-andere-gerate-im-fritz-heimnetz-moglich) | Guest/home reachability boundary; some knowledge pages returned only a shell |
| [6591 LAN guest access](https://fritz.com/apps/knowledge-base/fritz-box-6591-cable/949_lan-gastzugang-in-fritz-box-einrichten) | Model-scoped guest-port documentation; verify deployed UI |
| [VPN and IPv6](https://fritz.com/apps/knowledge-base/FRITZ-Box-7590-AX/3732_ubertragt-die-fritz-box-ipv6-daten-uber-vpn) | Separate outer VPN transport from inner routed address families; model-scoped |

## Firsthand sources and fixes

See [Community evidence](community-evidence.md) for dates, model/version context, outcomes, and limitations. Original sources: [Control 440 webhook report](https://community.home-assistant.io/t/fritz-smart-control-440-blueprint-webhook/981706), [RolloTron issue #110335](https://github.com/home-assistant/core/issues/110335), [7490 timeout discussion](https://community.home-assistant.io/t/fritzbox-option-to-change-default-timeout/949176), [DNS correction #182103](https://github.com/home-assistant/core/issues/182103), [October regression #185818](https://github.com/home-assistant/core/issues/185818), [fix #186029](https://github.com/home-assistant/core/pull/186029), [Energy 250 hands-on article](https://chrissmart.de/fritz-smart-energy-250-im-test-mit-home-assistant/).

The [Control 440 author's blueprint gist](https://gist.github.com/jhol-byte/c9ee61b60337455622a7187871280321) is linked as a reviewable community implementation, not bundled or implicitly trusted executable code.

## Refresh procedure

1. Identify the installed router/device/provider and HA versions. Keep observations distinct from manufacturer listings.
2. Open the current FRITZ interface index and matching model documentation. Record document dates and schema versions separately.
3. Inspect the HA integration at the installed tag, including its manifest dependency, then inspect that library release. Use the default branch only as evidence of unreleased/future behavior unless release matching is established.
4. Reproduce with a sanitized, bounded read where authorized. Compare discovery descriptions and actual returned capabilities against advertised ones.
5. Recheck open issues and fixes with exact versions. Prefer first-person accounts with model/context; label missing versions, speculation, and commercial context.
6. Update the affected reference and its snapshot/version claim. Do not silently turn a model-specific result into a whole-family guarantee.

Dynamic FRITZ knowledge-base pages sometimes yielded only navigation/shop content in this research session. Search snippets can establish a narrow claim but cannot support reconstructing a missing procedure. Reopen the model-specific manual or ask for the actual displayed UI when those details matter. No passwords, live SIDs, private router exports, or complete third-party API documents are bundled with this skill.
