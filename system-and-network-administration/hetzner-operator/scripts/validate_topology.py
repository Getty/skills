#!/usr/bin/env python3
"""Validate one routed IPv4 Hetzner Cloud Network plus VPN topology, offline.

Usage: python3 validate_topology.py topology.json
       python3 validate_topology.py - < topology.json

Input is one JSON object with exactly these fields:
  network_cidr: canonical RFC1918 IPv4 CIDR
  cloud_subnets: nonempty list of disjoint CIDRs inside network_cidr
  vpn_gateway_ip: Cloud IPv4 address of the VPN gateway VM
  vpn_cidr: canonical RFC1918 IPv4 VPN CIDR
  site_cidrs: list of canonical RFC1918 IPv4 site CIDRs
  other_cidrs: list of other canonical IPv4 CIDRs that must not overlap
  private_servers: nonempty list of {name, ip}
  provider_routes: list of {destination, gateway}
  guest_routes: list of {server, destination, via}

The only modeled provider routes are one exact route for each VPN/site prefix
through vpn_gateway_ip. Each private server must have one exact guest route to
each such prefix through the first usable address of the CLOUD NETWORK, not the
first address of its subnet. Extra routes, including default routes, aggregates,
and split more-specific routes, are rejected rather than analyzed partially.

This deliberately conservative model requires at least eight addresses in Cloud
Networks/subnets and four in VPN/site prefixes. These are validator scope limits,
not claims about Hetzner product limits. Arrays are limited to 256 entries each.

No network, subprocess, API, configuration, or infrastructure actions occur.
PASS establishes consistency of the supplied model, not real reachability. It
does not validate WireGuard AllowedIPs, forwarding, NAT, firewall rules, MTU,
DNS, OS route persistence, actual provider state, or failover.

Output is JSON: valid, errors, warnings, derived_gateway.
Exit status: 0 valid; 1 inconsistent topology; 2 malformed input or usage.
"""

import ipaddress
import json
import re
import sys


MAX_INPUT_CHARS = 1_048_576
MAX_LIST_ITEMS = 256
RFC1918 = tuple(
    ipaddress.IPv4Network(value)
    for value in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")
)
PUBLIC_GATEWAY = ipaddress.IPv4Address("172.31.1.1")
ROOT_FIELDS = {
    "network_cidr", "cloud_subnets", "vpn_gateway_ip", "vpn_cidr",
    "site_cidrs", "other_cidrs", "private_servers", "provider_routes",
    "guest_routes",
}
RECORD_FIELDS = {
    "private_servers": {"name", "ip"},
    "provider_routes": {"destination", "gateway"},
    "guest_routes": {"server", "destination", "via"},
}
SCOPE_WARNING = (
    "Offline consistency check only: actual provider/guest state, WireGuard "
    "AllowedIPs, forwarding, NAT, firewalls, DNS, MTU, persistence, and failover "
    "are not tested. Only exact VPN/site return routes are modeled."
)


def report(errors, warnings=None, gateway=None):
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings or [],
        "derived_gateway": str(gateway) if gateway is not None else None,
    }


def check_fields(value, expected, path, errors):
    if not isinstance(value, dict):
        errors.append(f"{path}: expected an object")
        return False
    for field in sorted(expected - value.keys()):
        errors.append(f"{path}: missing field {field!r}")
    for field in sorted(value.keys() - expected):
        errors.append(f"{path}: unexpected field {field!r}")
    return True


def structure_errors(data):
    errors = []
    if not check_fields(data, ROOT_FIELDS, "$", errors):
        return errors
    for field in ("network_cidr", "vpn_cidr", "vpn_gateway_ip"):
        if field in data and not isinstance(data[field], str):
            errors.append(f"{field}: expected a string")
    for field in ("cloud_subnets", "site_cidrs", "other_cidrs"):
        if field not in data:
            continue
        if not isinstance(data[field], list):
            errors.append(f"{field}: expected an array of strings")
            continue
        if len(data[field]) > MAX_LIST_ITEMS:
            errors.append(f"{field}: at most {MAX_LIST_ITEMS} entries are supported")
        for index, value in enumerate(data[field]):
            if not isinstance(value, str):
                errors.append(f"{field}[{index}]: expected a string")
    for field, required in RECORD_FIELDS.items():
        if field not in data:
            continue
        if not isinstance(data[field], list):
            errors.append(f"{field}: expected an array of objects")
            continue
        if len(data[field]) > MAX_LIST_ITEMS:
            errors.append(f"{field}: at most {MAX_LIST_ITEMS} entries are supported")
        for index, record in enumerate(data[field]):
            path = f"{field}[{index}]"
            if check_fields(record, required, path, errors):
                for key in sorted(required & record.keys()):
                    if not isinstance(record[key], str):
                        errors.append(f"{path}.{key}: expected a string")
    return errors


def parse_network(value, path, errors, private=False, max_prefix=32):
    try:
        network = ipaddress.ip_network(value, strict=True)
    except ValueError:
        errors.append(f"{path}: expected a canonical IPv4 CIDR with no host bits")
        return None
    if not isinstance(network, ipaddress.IPv4Network):
        errors.append(f"{path}: IPv6 is outside this validator's scope")
        return None
    if str(network) != value:
        errors.append(f"{path}: canonical spelling is {str(network)!r}")
    if private and not any(network.subnet_of(block) for block in RFC1918):
        errors.append(f"{path}: must be wholly within an RFC1918 IPv4 range")
    if network.prefixlen > max_prefix:
        errors.append(
            f"{path}: /{network.prefixlen} is too small for this model; "
            f"prefix length must be at most /{max_prefix}"
        )
    return network


def parse_address(value, path, errors):
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        errors.append(f"{path}: expected a canonical IPv4 address")
        return None
    if not isinstance(address, ipaddress.IPv4Address):
        errors.append(f"{path}: IPv6 is outside this validator's scope")
        return None
    if str(address) != value:
        errors.append(f"{path}: canonical spelling is {str(address)!r}")
    return address


def check_overlaps(named_networks, errors):
    for index, (name, network) in enumerate(named_networks):
        for other_name, other in named_networks[index + 1:]:
            if network.overlaps(other):
                errors.append(f"{name} ({network}) overlaps {other_name} ({other})")


def validate(data):
    """Return (JSON-ready result, exit status) without external side effects."""
    malformed = structure_errors(data)
    if malformed:
        return report(malformed), 2
    errors = []
    network = parse_network(data["network_cidr"], "network_cidr", errors, True, 29)
    vpn = parse_network(data["vpn_cidr"], "vpn_cidr", errors, True, 30)
    vpn_gateway = parse_address(data["vpn_gateway_ip"], "vpn_gateway_ip", errors)
    gateway = (
        ipaddress.IPv4Address(int(network.network_address) + 1)
        if network is not None and network.prefixlen <= 30 else None
    )
    parsed = {}
    for field in ("cloud_subnets", "site_cidrs", "other_cidrs"):
        parsed[field] = []
        for index, value in enumerate(data[field]):
            path = f"{field}[{index}]"
            prefix_limit = 29 if field == "cloud_subnets" else 30
            item = parse_network(
                value, path, errors, field != "other_cidrs",
                prefix_limit if field != "other_cidrs" else 32,
            )
            if item is not None:
                parsed[field].append((path, item))
    if not data["cloud_subnets"]:
        errors.append("cloud_subnets: at least one assigned Cloud subnet is required")
    if not data["private_servers"]:
        errors.append("private_servers: at least one private server is required")
    global_ranges = []
    if network is not None:
        global_ranges.append(("network_cidr", network))
    if vpn is not None:
        global_ranges.append(("vpn_cidr", vpn))
    global_ranges.extend(parsed["site_cidrs"] + parsed["other_cidrs"])
    check_overlaps(global_ranges, errors)
    subnets = parsed["cloud_subnets"]
    check_overlaps(subnets, errors)
    for path, subnet in subnets:
        if network is not None and not subnet.subnet_of(network):
            errors.append(f"{path}: {subnet} is not inside Cloud Network {network}")

    assigned = {}

    def check_host(address, path):
        if address is None:
            return
        if address in assigned:
            errors.append(f"{path}: address {address} is already used by {assigned[address]}")
        else:
            assigned[address] = path
        if network is not None and address not in network:
            errors.append(f"{path}: {address} is outside Cloud Network {network}")
        matches = [subnet for _, subnet in subnets if address in subnet]
        if len(matches) != 1:
            errors.append(f"{path}: {address} must belong to exactly one Cloud subnet")
        if address == PUBLIC_GATEWAY:
            errors.append(f"{path}: 172.31.1.1 is reserved for the public gateway")
        if gateway is not None and address == gateway:
            errors.append(f"{path}: {address} is the reserved Cloud Network gateway")
        for subnet in matches:
            if address in (subnet.network_address, subnet.broadcast_address):
                errors.append(f"{path}: {address} is a subnet network/broadcast address")
        if network is not None and address in (
            network.network_address, network.broadcast_address
        ):
            errors.append(f"{path}: {address} is the Network network/broadcast address")

    check_host(vpn_gateway, "vpn_gateway_ip")
    server_names = set()
    for index, server in enumerate(data["private_servers"]):
        path = f"private_servers[{index}]"
        name = server["name"]
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,62}", name):
            errors.append(f"{path}.name: use 1-63 ASCII letters, digits, dots, underscores or hyphens; start with a letter or digit")
        if name in server_names:
            errors.append(f"{path}.name: duplicate server name {name!r}")
        server_names.add(name)
        address = parse_address(server["ip"], f"{path}.ip", errors)
        check_host(address, f"{path}.ip")

    destinations = {str(item) for _, item in parsed["site_cidrs"]}
    if vpn is not None:
        destinations.add(str(vpn))

    def check_destination(value, path):
        destination = parse_network(value, path, errors)
        if destination is None:
            return None
        canonical = str(destination)
        if canonical not in destinations:
            errors.append(
                f"{path}: unexpected route {canonical}; only exact VPN/site prefixes "
                "are allowed (no default, aggregate, split, or extra routes)"
            )
        return canonical

    seen_provider = set()
    for index, route in enumerate(data["provider_routes"]):
        path = f"provider_routes[{index}]"
        destination = check_destination(route["destination"], f"{path}.destination")
        next_hop = parse_address(route["gateway"], f"{path}.gateway", errors)
        if destination is not None:
            if destination in seen_provider:
                errors.append(f"{path}: duplicate provider destination {destination}")
            seen_provider.add(destination)
        if next_hop is not None and vpn_gateway is not None and next_hop != vpn_gateway:
            errors.append(f"{path}.gateway: must be VPN gateway VM {vpn_gateway}, not {next_hop}")
    for missing in sorted(destinations - seen_provider):
        errors.append(f"provider_routes: missing exact return route for {missing} through vpn_gateway_ip")

    seen_guest = set()
    for index, route in enumerate(data["guest_routes"]):
        path = f"guest_routes[{index}]"
        name = route["server"]
        if name not in server_names:
            errors.append(f"{path}.server: unknown private server {name!r}")
        destination = check_destination(route["destination"], f"{path}.destination")
        next_hop = parse_address(route["via"], f"{path}.via", errors)
        if destination is not None:
            key = (name, destination)
            if key in seen_guest:
                errors.append(f"{path}: duplicate guest route for {name!r} to {destination}")
            seen_guest.add(key)
        if next_hop is not None and gateway is not None and next_hop != gateway:
            errors.append(
                f"{path}.via: must be Cloud Network gateway {gateway}, not {next_hop}; "
                "derive it from network_cidr, not cloud_subnets or vpn_gateway_ip"
            )
    expected_guest = {(name, destination) for name in server_names for destination in destinations}
    for name, destination in sorted(expected_guest - seen_guest):
        errors.append(f"guest_routes: missing exact return route for {name!r} to {destination} via {gateway}")
    return report(errors, [SCOPE_WARNING], gateway), 1 if errors else 0


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"non-finite JSON number {value!r} is not allowed")


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1 or args[0] in ("-h", "--help"):
        result = report(["Usage: python3 validate_topology.py FILE.json (or - for stdin). See the module docstring for schema and scope."])
        code = 2
    else:
        try:
            if args[0] == "-":
                raw = sys.stdin.read(MAX_INPUT_CHARS + 1)
            else:
                with open(args[0], "r", encoding="utf-8") as handle:
                    raw = handle.read(MAX_INPUT_CHARS + 1)
            if len(raw) > MAX_INPUT_CHARS:
                raise ValueError(f"input exceeds {MAX_INPUT_CHARS} characters")
            data = json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject_constant)
            result, code = validate(data)
        except (OSError, UnicodeError, ValueError, RecursionError) as error:
            result, code = report([f"Malformed input: {error}"]), 2
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
