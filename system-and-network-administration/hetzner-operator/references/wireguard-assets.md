# Bundled WireGuard example files and topology validator

Read when adapting the bundled WireGuard or nftables examples, or when checking a
Cloud/office/VPN address and route plan offline.

Use [WireGuard site-to-site](wireguard-site-to-site.md) as the implementation entry point.
It supplies prerequisites, Cloud and guest routes, firewall integration, tests, SNAT
alternative, rollout, and rollback. The example permits selected administrators to
initiate management connections; widen policy only for actual required flows.

- [Topology example](../assets/wireguard-topology.json): a routed Cloud/office/VPN address
  and route plan without credentials.
- [Hub configuration](../assets/wireguard/hub.conf.example),
  [office configuration](../assets/wireguard/office.conf.example), and
  [administrator configuration](../assets/wireguard/admin.conf.example): replace
  documentation addresses, interface names, and key placeholders locally before use.
- [Hub firewall](../assets/wireguard/hub.nft.example): an illustrative nftables policy for
  a dedicated gateway; integrate it with the existing firewall instead of flushing other
  rule owners.
- [Topology validator](../scripts/validate_topology.py): validate this example schema
  offline using Python's standard library. It checks CIDR overlaps, reserved/duplicate
  addresses, missing Cloud return routes, and wrong guest next hops. It neither provisions
  infrastructure nor proves that a live firewall, tunnel, or network manager is correct.

Run from the skill directory:

```bash
python3 scripts/validate_topology.py assets/wireguard-topology.json
```

When adapting the input, provide all participating private application servers and
relevant existing address ranges. The schema intentionally represents one routed IPv4
Cloud Network and one VPN gateway; use the other references for NAT, overlapping address
translation, multiple gateways, or IPv6 transport.
