# Plan networking around actual flows

## Build a flow inventory

Record source, destination, protocol/port, direction, discovery method, authentication, and whether the connection is needed during commissioning or normal operation. Use the exact installed configuration rather than universal port assumptions.

| Flow | Typical consideration |
|---|---|
| HA → native hub/device | Local API reachability and a stable address; cloud login may be separate |
| Device → HA | Webhook/event callback must reach the advertised address; working outbound polling does not prove this |
| HA → MQTT broker ← device | Credentials, topic authorization, broker persistence and reconnect behavior |
| HA → Matter server → device | WebSocket service plus IPv6 device communication |
| Phone ↔ new Matter device | Commissioning permissions, Bluetooth, credentials and local discovery |
| Thread border router ↔ LAN | IPv6 routing, multicast, route advertisement handling |
| HA/Frigate → camera | Separate control API, stream, events and talkback paths |
| Phone → remote HA | Authenticated reachable URL; snapshot/media access may differ from text push delivery |

HA's [network integration](https://www.home-assistant.io/integrations/network/) controls interface selection; [Zeroconf](https://www.home-assistant.io/integrations/zeroconf/) and [SSDP](https://www.home-assistant.io/integrations/ssdp/) are distinct discovery mechanisms. The [Matter server OS requirements](https://github.com/home-assistant-libs/python-matter-server/blob/main/docs/os_requirements.md) explain host requirements that ordinary TCP connectivity does not establish.

## Establish a working baseline before segmentation

Discover and test one device on an ordinary trusted LAN first. Then introduce one routing/filtering change and rerun the same checks. Keep a known-good path for administering the router and HA. Do not move every hub into a guest SSID and then attempt to debug all integrations simultaneously.

Separate discovery from data access. mDNS reflection can make a name visible without making the advertised IPv6 address routable. A manually supplied IP can fix discovery for some integrations but cannot bypass a broken event callback or multicast requirement.

Do not disable IPv6 globally to fix a single device. Matter/Thread uses IPv6 locally even when the internet provider offers only IPv4. Conversely, an IPv6-only HA host is a separate configuration with software prerequisites; dual stack is a useful baseline for diagnosis. A dated firsthand report of a Zeroconf initialization failure on IPv6-only HA Container is [core #161398](https://github.com/home-assistant/core/issues/161398); it is not evidence that Thread should use IPv4.

## Treat a FRITZ guest network as a separate product feature

A FRITZ guest network is not a general-purpose configurable VLAN firewall. Determine the exact model, firmware, router/IP-client mode and guest isolation behavior in `fritzbox-operator`. Do not prescribe arbitrary VLAN interfaces or enterprise ACLs that the box cannot configure. If the desired design requires a managed router/switch, describe that added component and its operational burden.

Use DHCP reservations where appropriate and document device identity. An IP address is a locator, not necessarily a persistent device ID. Large host lists can contain old leases, privacy MAC addresses and virtual interfaces.

## Diagnose in layers

1. Verify power, link and address.
2. Resolve hostnames from HA's own environment, not only the user's desktop.
3. Test the exact control service and authentication.
4. Verify event direction using timestamps and logs.
5. Verify each required media/data path.
6. Examine multicast and IPv6 routes only where relevant.
7. Retest after a controlled HA/service restart and a single device reconnect.

Do not deploy a blanket firewall-open rule as the final fix. Record the successful minimum flows, and distinguish a short diagnostic experiment from the resulting policy. Keep vendor cloud and DNS/time dependencies explicit when evaluating offline operation.
