# Security, firewalls, and administrative boundaries

Verified against primary documentation on **2026-10-04**. Recheck provider capabilities and permissions before changing production access. Recommendations below are operational design guidance; they are not additional Hetzner product guarantees.

## Contents

- [Choose the correct enforcement layer](#choose-the-correct-enforcement-layer)
- [Accounts, projects, and credentials](#accounts-projects-and-credentials)
- [Cloud Firewall behavior](#cloud-firewall-behavior)
- [Robot firewall behavior](#robot-firewall-behavior)
- [Private services and containers](#private-services-and-containers)
- [Change access without locking yourself out](#change-access-without-locking-yourself-out)
- [Required security handover](#required-security-handover)

## Choose the correct enforcement layer

Start with a packet path and an identity path. Identify where each connection enters, whether it is forwarded or locally terminated, and which human or machine can modify that path.

| Layer | Appropriate job | Boundary to remember |
|---|---|---|
| Account and project permissions | Control infrastructure administration | Infrastructure membership does not replace application authentication |
| Cloud Firewall | Filter supported public traffic of attached Cloud servers | Private Network traffic and Load Balancer attachment are unsupported |
| Robot firewall | Filter dedicated-server switch-port traffic | Stateless rules require explicit treatment of both directions |
| Guest firewall | Enforce host and routed traffic policy | Container forwarding can follow a different chain from host INPUT |
| Application | Authenticate users, authorize operations, limit requests | A private address alone does not establish trust |

Provider boundaries: [Cloud Firewall FAQ](https://docs.hetzner.com/cloud/firewalls/faq/), [Robot firewall](https://docs.hetzner.com/robot/dedicated-server/firewall/).

Hetzner advertises automatic DDoS filtering. Treat that as network-attack mitigation; still design application authentication, rate limits, expensive-query limits, and overload handling. A valid authenticated request can consume excessive resources without resembling a network flood. [Hetzner DDoS protection](https://www.hetzner.com/unternehmen/ddos-schutz/)

## Accounts, projects, and credentials

Use named accounts and project invitations. The current roles are Owner, Admin, Member, and Restricted. Owners pay for project resources. Admin and Owner can manage members, API tokens, and S3 credentials. Member and Restricted both retain write capabilities; **Restricted is not a read-only role**. External collaborators can use light accounts without supplying payment details. Both light and full accounts support 2FA. Verify permitted operations against the current table. [Cloud general FAQ](https://docs.hetzner.com/cloud/general/faq/)

Documentation caution: some feature FAQs contain Restricted permissions that conflict with the newer general table. For example, the [Snapshot FAQ](https://docs.hetzner.com/cloud/servers/backups-snapshots/faq/) and general permissions table disagree about snapshot mutations. Use the current general table for planning and inspect the current interface/capability or a disposable test resource; do not test destructive permissions on recovery data or resolve the conflict by granting a broader role automatically.

Cloud API tokens are generated inside a project with Read or Read & Write permissions. Read permits GET requests; Read & Write also permits mutations. Full tokens are shown once. Use separate credentials for inventory, provisioning, and each integration, and keep secrets out of prompts, examples, logs, cloud-init, and repositories. [Token creation](https://docs.hetzner.com/cloud/api/getting-started/generating-api-token/)

Enable account 2FA and store recovery material independently of the account and servers it protects. Multiple authentication methods can be active. Treat recovery as a tested operational dependency, especially when the same account controls VPN, DNS, and the only recovery environment. [2FA guidance](https://docs.hetzner.com/general/security-and-identify/two-factor-authentication/)

## Cloud Firewall behavior

Cloud Firewalls are stateful allowlists. Unmatched new inbound traffic is denied. With no outbound rules, outbound traffic is allowed; adding outbound rules makes unmatched outbound traffic denied. Rules from multiple attached Firewalls combine, and order does not create deny precedence. Existing connections survive restrictive rule changes. Certain infrastructure traffic bypasses filtering, including metadata and specified Hetzner services. Verify actual attachment after label changes, especially on servers without public IPs. [Cloud Firewall FAQ](https://docs.hetzner.com/cloud/firewalls/faq/)

Build rules from an explicit flow inventory:

| Connection | Example policy |
|---|---|
| Administration | SSH from the management VPN or approved administrator addresses |
| Public application | Only required public ports; authenticate at the application |
| Database | Reachable through private interfaces and explicit host policy |
| Health checks | Permit the actual checker path to its required port |
| Outbound dependencies | Identify DNS, time, updates, certificate renewal, APIs, and backup destinations before restricting egress |

Test IPv4 and IPv6 independently. Removing public IPv4 while retaining Primary IPv6 still leaves a public-facing server. [Primary IP FAQ](https://docs.hetzner.com/cloud/servers/primary-ips/faq/)

## Robot firewall behavior

Robot filtering is stateless and supports incoming and outgoing directions. It operates at the switch port, **including vSwitch traffic**. IPv4 filtering is the default; IPv6 filtering must be enabled separately. Rules are ordered, with a maximum of ten per direction. Unmatched packets are discarded. Reply traffic needs suitable rules; a TCP ACK test is not connection tracking. IPv6 filtering has additional restrictions, including always-permitted ICMPv6. The Hetzner Services option affects inbound infrastructure traffic, so restrictive outbound policy needs its own allowances. [Robot firewall](https://docs.hetzner.com/robot/dedicated-server/firewall/)

Do not paste an ephemeral-port recipe without checking the installed OS, clients, UDP traffic, and intended outbound services. Preserve vSwitch management connectivity when introducing port-level filtering. Keep detailed stateful policy in the guest when the provider rule model cannot express the requirement clearly.

## Private services and containers

Define allowed private flows explicitly, such as app-to-database, replication, metrics collection, and backup traffic. Separate application credentials and administrative credentials. Authenticate and encrypt sensitive connections according to the threat model, even within a private Network. Avoid treating a subnet label as an isolation policy.

Inspect listening addresses and published container ports. Linux Docker bridge networking creates forwarding/NAT rules; published ports can bypass UFW's expected INPUT/OUTPUT processing. Docker's iptables and nftables backends also differ in how they handle forwarding defaults. Identify the installed backend before choosing policy integration. Do not disable Docker's rule management as a generic fix. [Docker firewall documentation](https://docs.docker.com/engine/network/packet-filtering-firewalls/)

For reverse proxies, restrict backend reachability and trust forwarded client headers only from the intended proxy. Terminate management interfaces behind the management access path. Rotate application secrets after restoring images that may contain older keys.

## Change access without locking yourself out

1. Record the active route, source address, firewall rules, and network manager.
2. Confirm a usable recovery console and guest login before tightening access.
3. Add the new management path and test a **new** SSH connection through it.
4. Apply the narrow change; keep the existing session open while testing.
5. Verify required permitted connections and representative forbidden connections from appropriate source networks.
6. Remove superseded access after successful verification and persist the configuration.

The Cloud console provides guest console access and a root-password reset workflow. A reset is a mutation, not a diagnostic command. Confirm that the actual image supports the expected recovery mechanism. [Using the console](https://docs.hetzner.com/cloud/servers/getting-started/vnc-console/)

## Required security handover

Return the resource scope, administrators, credential ownership, public and private flow table, IPv6 policy, guest/container enforcement points, tested recovery path, verification results, and rollback procedure. Highlight the specific unresolved boundary if evidence is missing; avoid declaring a system secure solely because a provider Firewall is attached.
