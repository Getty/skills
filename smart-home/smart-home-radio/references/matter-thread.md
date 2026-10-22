# Diagnose Matter and Thread separately

## Identify four different objects

| Object | Responsibility | Common mistaken inference |
|---|---|---|
| Matter controller/server | Owns a fabric and application control | “Any Thread router controls the lamp.” |
| Matter fabric | Security/admin relationship between controller and devices | “Joining Wi-Fi joined HA.” |
| Thread mesh + dataset | Radio/IP network and its credentials | “Same network name means same dataset.” |
| Thread border router | Routes IPv6 between Thread and LAN | “It is a Zigbee coordinator or a Matter bridge.” |

Matter may use Wi-Fi/Ethernet or Thread. Thread devices can use a higher-level protocol other than Matter. HA's [Matter](https://www.home-assistant.io/integrations/matter/) and [Thread](https://www.home-assistant.io/integrations/thread/) integrations describe these different roles. A vendor Matter bridge exposes selected functions of attached devices; it does not convert every vendor-specific feature.

## Commission in a known-good environment

1. Identify the exact device's transport and whether it is already paired to another controller.
2. Confirm a functioning HA Matter server and its persistent data. On a separately managed deployment, inspect its version/networking explicitly.
3. For Thread, identify the intended dataset and border router. Synchronize the necessary credentials with the commissioning phone through the supported flow.
4. Use the HA Companion app and supported phone permissions/services for new-device commissioning. A desktop browser is not a replacement for the documented commissioning flow.
5. Open the appropriate pairing window. For an already commissioned device, use the existing controller's sharing/multi-admin flow when supported rather than factory-resetting it automatically.
6. Test control from HA and the original controller, then restart HA/server to verify the persistent relationship.

Keep setup codes and Thread credentials private. Multi-admin support does not imply unlimited fabrics or identical feature exposure; check the product's limits.

## Test networking before resetting devices

Verify local IPv6 addresses and routes, multicast/mDNS reachability, router advertisements, and the actual interface used by the server. IPv6 internet service is a different requirement from local IPv6. mDNS forwarding alone cannot repair an unroutable address or incompatible kernel.

The [Matter server OS requirements](https://github.com/home-assistant-libs/python-matter-server/blob/main/docs/os_requirements.md) document host-network prerequisites. Containers and NAS kernels may differ from HAOS. Test on a simple LAN when a segmented topology fails, then restore boundaries one at a time.

Do not disable IPv4 merely because Thread is IPv6. A firsthand HA Container report [#161398](https://github.com/home-assistant/core/issues/161398) describes an IPv6-only Zeroconf initialization failure, including later 2026 reproduction. Use dual stack as a diagnostic comparison where appropriate; verify whether the installed release contains a fix.

## Separate control from updates

A reachable device can still lack an HA-supported OTA path. Verify vendor update provider, Matter server release, device firmware and border-router constraints. Current HA documentation records restrictions for OTA through Apple Thread border routers. Check the current procedure before offering to update; do not generalize that restriction to all ordinary control traffic.

For an apparent outage, distinguish the device's power/radio state, Thread routing, Matter session, controller process and HA entity. Keep normal sleepy-device behavior separate from sustained missing observations. Preserve logs before changing the Thread channel or dataset.

## Recover without losing ownership

Back up Matter server state and Thread credentials through the installed system's supported route. A fresh server with an empty data directory is a different controller even when HA's dashboard looks identical. Migrate radios with the documented process; leave working external border routers in place unless there is evidence they are the cause.
