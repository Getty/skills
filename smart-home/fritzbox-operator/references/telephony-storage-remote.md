# Telephony, storage, remote access, and media

## Telephone events and call history

The [HA Call Monitor integration](https://www.home-assistant.io/integrations/fritzbox_callmonitor/) listens on TCP 1012 and exposes call state; its setup documents activation by dialing `#96*5*` from a directly connected phone. It also needs the documented network access and rights for directory lookup. Treat enabling the monitor as a configuration change, not an automatic read-only prerequisite. Keep the event stream local; phone numbers are household data.

Live events and stored history solve different tasks. An integration offline during a call may miss the real-time event. Use documented call-list retrieval if the goal is historical reconciliation, and decide retention/redaction before placing caller information in HA history or notifications.

The [OnTel specification](https://fritz.support/resources/TR-064_Contact_SCPD.pdf) covers phonebook lists/entries, call-list URLs, and forwarding-related functions. Resolve the actual phonebook IDs; do not assume the default list contains every contact. Follow returned URLs with their required session context, keep tokens private, and normalize telephone numbers before lookup. A display name match is not a unique identity.

## SIP, dialing, and answering machines

Use the [VoIP service specification](https://fritz.support/resources/TR-064_VoIP.pdf) for supported management actions. A local IP telephone registers with its own configured SIP identity; an FRITZ web user is not interchangeable with that account. Separate SIP signaling, RTP media, codecs, NAT/firewall behavior, and registration status when diagnosing calls that connect without audio.

For a click-to-dial operation, identify the selected endpoint, number, and call impact. Do not place test calls without authorization or repeatedly dial on an automation retry. The [Tools integration](https://www.home-assistant.io/integrations/fritz/) exposes a dialing action, but that does not make the router a general-purpose HA speech-output device. For answering-machine control, distinguish enabling the machine, retrieving messages, and changing greetings or schedules.

## NAS and USB storage

TR-064 [Storage](https://fritz.support/resources/TR-064_Storage.pdf) manages storage service settings; data transfer uses the relevant file protocol. Diagnose permissions, filesystem health, USB power, name resolution, protocol version, and throughput independently. Do not turn on obsolete SMB compatibility merely because an old client cannot connect; check the client's supported protocol and current firmware first.

Keep NAS credentials scoped to required shares. A writable USB share on the same router is not an independent disaster-recovery copy of the router or HA installation. For HA backups, verify the actual supported backup/network-storage route and perform a restore check; a directory listing is not a backup validation.

For media, UPnP AV/DLNA discovery, file decoding, and TV playback are separate layers. “Visible in the media server” does not establish codec support or transcoding. Verify the consuming device's capabilities.

## VPN and MyFRITZ

MyFRITZ naming/account features do not magically provide reachability through every carrier NAT or client network. Inventory public/private IPv4, DS-Lite, IPv6 prefix, endpoint DNS, and the remote client's connectivity. A public IPv6 path can support a VPN even without inbound public IPv4, but both ends and the exact firmware must support the chosen path. Distinguish the address family carrying the VPN transport from the address families routed inside it; consult the current [FRITZ VPN IPv6 documentation](https://fritz.com/apps/knowledge-base/FRITZ-Box-7590-AX/3732_ubertragt-die-fritz-box-ipv6-daten-uber-vpn) for the target model/version rather than generalizing from its title.

Prefer a supported VPN or an explicitly chosen HA remote-access service over exposing FRITZ administrative APIs. Verify WireGuard availability in the actual provider firmware; do not infer it from another FRITZ model. Keep peer private keys and generated connection files secret. Define intended subnets, DNS behavior, and whether traffic is split or full tunnel before changing routes.

Avoid overlapping LAN subnets when connecting homes/sites. Record a recovery route before modifying an active VPN remotely. Test from a genuinely external network and account for client IPv4-only access before declaring remote access complete.

## Port mappings and IPv6 exposure

The [WAN IP specification](https://fritz.support/resources/TR-064_WAN_IP_Connection.pdf) limits certain self-managed mappings to the requesting host. HA's port-forward switches consequently do not represent unrestricted arbitrary-router firewall control. An IPv4 NAT mapping and an IPv6 firewall permission are different operations; do not open both indiscriminately or imply that DS-Lite yields a dedicated IPv4 address.

## Cable TV and other interfaces

Some FRITZ Cable hardware/firmware provides DVB-C-related functions. Verify tuner support, provider restrictions, actual streaming endpoints, and client formats before integration. The [official interface index](https://fritz.com/pages/schnittstellen) links the `X_AVM-DE_Media` service; its presence in documentation does not prove a feature is enabled on the supplied 6591. Hand media playback and camera-specific work to `smart-home-video-media` while keeping router provisioning here.
