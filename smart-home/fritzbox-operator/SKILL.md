---
name: fritzbox-operator
description: "Use when integrating, automating or debugging a FRITZ!Box or FRITZ! smart-home devices — TR-064, AHA HTTP, the Smart Home REST API, login or SID errors, Home Assistant FRITZ!Box Tools or FRITZ!SmartHome, DECT thermostats, Control 440 buttons, presence trackers, mesh, guest network, provider-managed cable firmware, VPN, NAS, telephony."
---

# FRITZ!Box Operator

Treat the router as a shared network, telephony, and heating dependency. Identify the actual interface and owning controller before making changes. Use this skill with `home-assistant-operator` for HA deployment, `home-assistant-automations` for control logic, and `smart-home-radio` for non-FRITZ radio networks.

## Establish the operating facts

1. Record model, hardware/article revision where relevant, FRITZ!OS, retail/provider ownership, ISP, mesh role, management address, HA version, and desired outcome. Keep credentials, serial numbers, telephone numbers, public addresses, and support dumps out of ordinary reports.
2. Separate what the device supports, what its firmware exposes, what the API exposes, and what the installed HA integration implements. A working FRITZ app or web UI proves only part of that chain.
3. Use the current [interface map](references/interface-map.md), then inspect descriptions, entities, and capabilities. Prefer native HA integrations for supported operations, documented APIs for missing capabilities, and label scraped web UI endpoints as version-specific custom interfaces.
4. Record the household's actual FRITZ! inventory in the project — from the user or a read-only router/HA export — and treat counts as reports, not discovery results. A router's tracked-host count is not a count of active clients or people.
5. Refresh the primary source in [sources](references/sources.md) for new firmware, product, API, or regression claims. Snapshot checked: 2026-10-22; HA implementation inspected at tag 2026.10.2.

## Route the task

| Task | Load |
| --- | --- |
| Choose TR-064, provider TR-069/USP, AHA, REST, or Matter | [Interface map](references/interface-map.md) |
| Discover SOAP services, actions, arguments, security port, libraries | [TR-064](references/tr064.md) |
| Read/control older smart-home endpoints; interpret AINs and units | [AHA HTTP](references/aha-http.md) |
| Build a client for the versioned JSON API | [Smart Home REST API](references/rest-api.md) |
| Fix login, SID, PBKDF2/legacy compatibility, permissions, TLS | [Authentication](references/authentication.md) |
| Configure the three HA integrations and inspect entities | [Home Assistant](references/home-assistant.md) |
| Operate 301/302 thermostats, groups, schedules, external sensors | [Heating](references/heating.md) |
| Integrate Control/DECT 400 or 440 presses with webhooks | [Buttons](references/buttons.md) |
| Diagnose hosts, switches/APs, VLANs, guest isolation, mesh | [Network and presence](references/network-presence.md) |
| Operate a cable or provider-managed FRITZ!Box, update, migrate, recover | [Cable and recovery](references/cable-and-recovery.md) |
| Use calls, phonebooks, SIP, NAS, VPN, MyFRITZ, DVB-C | [Telephony, storage, remote access](references/telephony-storage-remote.md) |
| Compare FRITZ product families, radio roles, gateways, Matter | [Products and radios](references/products-and-radios.md) |
| Assess user reports without generalizing anecdotes | [Community evidence](references/community-evidence.md) |
| Refresh sources and version boundaries | [Sources](references/sources.md) |

## Execute in a controlled order

1. Inspect locally and read first: firmware/UI status, HA diagnostics, entity attributes, TR-064 description, and smart-home inventory. Never probe the public internet for an owner's router.
2. State the operation, target, expected impact, capability evidence, validation, and rollback. Reuse the user's authorization. Inspecting heating does not authorize rebooting the WAN router or changing firewall rules.
3. Use one writer per control decision. Resolve FRITZ schedules, native groups, manual input, HA automations, and vendor cloud controls before adding another writer.
4. Apply the smallest relevant change. Preserve entity identity, pairing, scheduled fallback, and local manual operation where practical.
5. Validate through readback and the observable result. Account for HA polling and battery radio latency. HTTP 200 or SOAP success alone does not prove that a radiator moved.
6. Distinguish name resolution, transport/TLS, authentication, authorization, API support, integration mapping, radio reachability, and device behavior. Compare the same timestamp across layers; avoid reset/re-pair/reinstall cycles without evidence.

## Enforce important boundaries

- Do not promise Control 440 button events through the current native `fritzbox` integration. Use verified FRITZ URL actions/webhooks when suitable, or verify an alternate bridge's actual endpoint support.
- Do not call AHA the sole current API. FRITZ publishes Smart Home REST versions for 8.20 and 8.50; AHA is frozen but still available. Do not assume 8.50 is deployed on a provider-managed box.
- Do not mistake REST `/connect` device subscription for push subscriptions; it concerns radio enrollment.
- Do not equate a DECT base with Zigbee, Smart Gateway with Wi-Fi repeater, or Matter bridge with universal Matter controller/Thread border router.
- Do not treat WAN VLAN settings as general LAN VLAN segmentation. Guest isolation can block local HA access by design.
- Do not use blind reconnects, factory resets, firmware flashing, arbitrary port forwarding, phone calls, lock changes, or unsafe heating changes as diagnostic defaults.
- Keep SIDs, secret-bearing URLs, webhook secrets, Wi-Fi/VPN/SIP credentials, and full diagnostics out of repositories and public issues.

## Local inspection helper

Use `python3 scripts/inspect_tr064.py path/to/tr64desc.xml` to list services from an already downloaded description. Use `--kind scpd` to list a service description's action signatures. The helper reads bounded local XML and performs no network or router operations. Read [TR-064](references/tr064.md) before constructing calls.

## Return a useful result

Provide the verified model/version/interface, observations, selected change, affected entities/devices, validation, rollback, and unresolved capability questions. For procurement, identify exact SKU and protocol and distinguish native HA support, community integration support, and advertised ecosystem compatibility.
