# Networking and access

## Determine the endpoint

Record hostname, scheme, port, internal/external URL, proxy, and release. Current HTTP docs state HAOS defaults to port 80 from 2026.8; Container stays at 8123. Existing configured values can differ. HTTP settings now use Settings → System → Network with confirmation/automatic rollback. Treat pre-2026.8 `http:` YAML as version-gated migration material. [HTTP integration](https://www.home-assistant.io/integrations/http/).

An old `:8123` bookmark failing does not prove HA is down. An open TCP port does not prove authentication or integrations work.

## Trace both directions

List initiating host, destination, discovery multicast, control connection, callbacks/subscriptions, DNS, and NTP. Test from HA's host/container network, not only a laptop.

| Symptom | Distinguishing check |
| --- | --- |
| IP reachable, no discovery | mDNS/SSDP scope, selected interfaces, duplicates |
| Polling works, events fail | Callback route, subscription and reverse traffic |
| Flat LAN works, VLAN fails | Exact flows and IPv6 routing |
| Login works, UI stops updating | Proxy WebSocket behavior/timeouts |
| Matter pairs, later fails | IPv6, mDNS, controller and Thread topology |

Do not disable IPv6 to simplify Matter. An mDNS reflector does not create all necessary routes. Use `smart-home-radio` for radio-specific networking.

## Proxy and remote access

Trust only actual proxy hops and preserve WebSockets. Do not permit arbitrary forwarding headers or disable certificate validation to hide TLS errors. Choose documented remote access or VPN as appropriate. [Remote access](https://www.home-assistant.io/docs/configuration/remote/).

Exposing HA does not require publishing TR-064, MQTT, camera management, or IoT device APIs. Identify CGNAT/DS-Lite before suggesting IPv4 forwarding; route router details to `fritzbox-operator`.

## Host boundaries and changes

Check each component's documented network mode. Multicast, DNS, USB permissions, Bluetooth D-Bus, and host networking are separate issues. A VM migration can change network/device identity despite identical HA configuration.

Keep console/alternate access before IP/proxy changes, record old values, and verify from both needed client locations. Check Companion URLs, webhooks, callbacks, and OAuth reachability. Replace temporary broad firewall exceptions with the exact required flows after identifying the fault.
