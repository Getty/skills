# Cable FRITZ!Box: provider firmware, operations, and recovery

## Verify ownership and provisioning

A cable model on a cable provider — for example a 6591 Cable on Vodafone — does not settle whether the box is provider-managed or a retail unit used on that service. Record exact model/article number, ownership, region/network, current FRITZ!OS, update controls, provider provisioning, telephony registration method, WAN address type, and any bridge/IP-client restrictions visible in the actual unit.

Providers can own firmware delivery: Vodafone's [6591 support page](https://www.vodafone.de/hilfe/router/fritzbox-cable-6591.html), for example, states that its supplied unit's firmware is updated by the provider. Do not promise a manually installable retail image, a release date, or availability of the newest REST/Matter functions on that unit. A report of one subscriber receiving an update is not evidence that every region or customer has received it.

## Keep WAN diagnosis separate from HA diagnosis

| Failure | Useful evidence | Avoid assuming |
| --- | --- | --- |
| Cable link/sync problem | Router cable status, events, provider incident status | HA caused a DOCSIS problem |
| Internet fails but LAN/API works | WAN status, DNS tests, IPv4/IPv6 paths | Router API is broken |
| HA cannot reach router but browsers can | HA namespace route/DNS/TLS, guest/VLAN path | Provider line fault |
| Native FRITZ devices work but HA does not | Integration logs, address selected, permissions | All devices need re-pairing |
| Remote access fails only from IPv4 networks | DS-Lite/public IPv6/client reachability | A different forwarding rule can create public IPv4 |

Cable modem operation is not PPPoE. Discover the WAN service and read the relevant status rather than replaying a DSL reconnect recipe. Reconnection does not guarantee a new address and is not a general maintenance requirement.

## Prepare a usable backup

Before a meaningful configuration change, create a password-protected settings export through the supported interface and store its password separately. Record firmware/model and export time. Also preserve the information needed to rebuild HA associations: router address, users/rights, reservations, native smart-home groups/schedules, and device assignments. Do not put the configuration export in a public issue or repository.

Distinguish router settings, phonebook/answering-machine data, USB/NAS files, radio pairing state, HA backup, and Matter fabric state. One export does not automatically guarantee recovery of every component. Verify the supported migration/restore procedure for the source and target model before replacing hardware.

For automated backup work, inspect [DeviceConfig](https://fritz.support/resources/TR-064_Device_Config.pdf) and the actual advertised actions. Returned export URLs may be short-lived secrets. Do not use a supposed backup action that in fact restores or resets the unit.

## Update with a measured rollback plan

Read model/provider release notes, identify the reason for the update, record current behavior, and schedule a suitable interruption. Prepare local wired access. Afterward verify WAN, telephony, DHCP/DNS, mesh, native thermostat operation, HA integrations, and essential automations. A successful boot alone is not enough.

Provider rollback may be unavailable, and downgrades can be unsupported. Do not promise a one-click rollback or flash a different provider/retail image. For an HA regression, restoring the HA version from a valid backup can be more relevant than changing router firmware; verify release-specific remedies first.

## Recover progressively

1. Preserve error timestamps, current LEDs/state, and any working access path.
2. Check power, cabling, the management address, and local Ethernet before changing configuration.
3. Compare direct IP access with DNS; inspect the execution environment's resolver.
4. Use the model-specific documented recovery/access method if normal access is lost.
5. Reboot only with the expected shared-service impact understood.
6. Reset/recover/re-pair only when the evidence and the user's request justify it, with a restoration plan and any required provider reactivation information.

Do not apply a Windows recovery executable intended for another FRITZ model or assume a cable device supports a retail recovery workflow. Do not confuse physical factory reset with restarting an HA integration.

Use the model's service hub and the provider's manual and support for precise procedures — for the 6591 Cable, the [6591 service hub](https://fritz.com/pages/service-fritz-box-6591-cable) and the [Vodafone manual](https://www.vodafone.de/downloadarea/FRITZ%21Box_6591_Cable_Handbuch_de.pdf). Old manuals establish hardware-era context, while the observed firmware and current provider documentation govern available menus.
