# Network inventory, presence, mesh, and segmentation

## Interpret the tracked-device count

Treat the router's number of tracked entries as a reported inventory size. Ask the router and HA registries separately how many are known, active, tracked, and associated with people. Multiple addresses, randomized MACs, retired hardware, guest clients, and multiple access paths can create misleading counts. A historical host table is not a live census.

Build a reconciliation table using a private stable identifier, observed MAC(s), IP(s), router name, HA device/entity IDs, connection path, last observed state, and intended role. Keep the exported table private. Do not delete entries simply because they are currently absent: a sleeping device or seasonal device may still own automations and reservations.

## Select an observation source

The [TR-064 Hosts specification](https://fritz.support/resources/TR-064_Hosts.pdf) and [Mesh Topology specification](https://fritz.support/resources/Mesh-Topology.pdf) describe different views. Mesh topology is a graph of nodes/interfaces/links; it is not necessarily a flat inventory of independently occupied rooms. Discover the actual bulk-host/topology actions and interpret absent information conservatively.

The [HA Tools documentation](https://www.home-assistant.io/integrations/fritz/) offers a `Consider home` delay and an old-discovery option relevant to non-mesh/mixed network scenarios. Host deletion in FRITZ can also remove associated HA entities. Use those mechanisms after comparing observed topology and desired identity retention; do not flip discovery modes solely because one device missed a poll.

For each presence decision, identify what is actually measured: router association, DHCP/host activity, a companion app location, Bluetooth observation, or a room sensor. Keep these signals separate until an explicit fusion policy combines them.

## Design presence behavior

Use router tracking as one input. Wi-Fi sleep, device shutdown, MAC randomization, AP roaming, and router reboot can all resemble departure. A phone connected to home Wi-Fi also does not prove that its owner is in a particular room.

Define arrival/departure rules using observed false-positive/false-negative costs. Lighting comfort may tolerate a delay; security disarming should not depend on a single unauthenticated network observation. Treat `unavailable` as unknown, and suppress absence-driven heating/security changes during router or integration downtime.

Create a small representative trial: one phone, one wired device, one sleeping IoT client, and one guest. Record true transitions and observed transitions across normal usage. Adjust the away delay from those measurements. Do not claim a universal best timeout.

## Mesh and radios

Draw separate relationships for FRITZ Wi-Fi mesh, Ethernet transport, DECT radio bases, and Zigbee coordinators. A mesh repeater can share Wi-Fi settings without repeating every smart-home radio protocol. A Smart Gateway can add DECT ULE/Zigbee devices without serving as a Wi-Fi client access point.

For each repeater/AP, identify wired or wireless backhaul. Disabling the radio that carries its backhaul can eliminate remote access. Mesh-adopted settings may be overwritten by the master; determine the configuration owner before editing the repeater.

Prefer a stable Ethernet connection for HA and infrastructure where practical. Place radio equipment based on measured coverage, not the router's convenient location next to the coax socket. Separate Wi-Fi congestion from DECT range problems: more Zigbee routers do not extend a DECT thermostat network.

## Guest access and VLAN boundaries

FRITZ guest access intentionally separates guests from home-network devices; the [6591 knowledge article](https://fritz.com/de-at/apps/knowledge-base/FRITZ-Box-6591-Cable/549_kein-zugriff-auf-andere-gerate-im-fritz-heimnetz-moglich) identifies this as a reason local access fails. Moving an IoT device there can break HA control, discovery, callbacks, and firmware services. Do not recommend that move without a complete communication plan.

Do not infer general-purpose LAN VLAN routing/firewall capabilities from a WAN VLAN-ID field. For a segmented installation, verify the actual router, switch, and AP roles and introduce a capable firewall/router where necessary. Define each permitted flow by initiator, destination, protocol, and purpose. Multicast discovery and stateful unicast callbacks are separate requirements; a reflector alone does not create the full path.

## Addressing and operational load

Use deliberate DHCP reservations or another documented addressing plan for gateways and integrations that need stable endpoints. Keep DNS consistent across HA, router-originated webhooks, containers, and VPN clients. Diagnose IPv4 and IPv6 independently; do not disable IPv6 globally to mask a discovery or name-resolution error.

Reduce duplicate pollers first when router API latency rises. Stagger noncritical collection, prefer bulk data, and retain sensible failure backoff. Record request duration and update age alongside connectivity. More retries against an overloaded gateway can turn occasional lateness into sustained unavailability.
