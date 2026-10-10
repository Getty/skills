# Web Hosting, Managed Servers, domains and DNS boundaries

Evidence snapshot: **2026-10-04**. Confirm plan features, supported runtime versions, DNS integration and domain-transfer rules for the actual account. This module covers selection and migration; use the DNS-specific module for detailed API/record operations.

## Contents

- [Select the hosting contract](#select-the-hosting-contract)
- [Check application compatibility](#check-application-compatibility)
- [Separate domain registration from DNS](#separate-domain-registration-from-dns)
- [Handle current DNS integration](#handle-current-dns-integration)
- [Migrate in controlled stages](#migrate-in-controlled-stages)
- [Operate and verify](#operate-and-verify)

## Select the hosting contract

Web Hosting supplies a constrained application environment, hosting databases, mail and plan-dependent development features. Compare process counts, memory limits, database allocation, cronjobs, SSH and runtime support. Do not assume every plan has the same developer features. Current web-hosting packages list domains as separate orders, so domain cost and configuration belong in the deployment plan. [Web Hosting catalog](https://www.hetzner.com/webhosting/).

Managed Servers provide a provider-administered hosting stack. Hetzner handles the underlying OS/server administration; the customer works through konsoleH and ordinary users, without root access. The current catalog distinguishes virtual MC and physical MA offerings. This does not mean a customer can ask the provider to operate arbitrary Kubernetes, kernel modules, custom database extensions or a chosen reverse-proxy stack under the same contract. [Managed Server catalog and FAQ](https://www.hetzner.com/managed-server/).

Use Cloud or a dedicated root server when the workload requires system-level control. Use a managed hosting product when its documented environment fits the application and reduced administration work matters more than that control.

konsoleH remains the management surface for Web Hosting, Managed Servers, Storage Share and associated domains. Customer identity and billing details have moved to the central accounts service; product-specific actions remain attached to the product. [konsoleH account/product overview](https://docs.hetzner.com/managed/administration-on-konsoleh/account-overview/).

Storage Share is a different managed application, based on Nextcloud. Its selected administrative OCC operations are available through konsoleH; this is not general-purpose root shell access. Check whether an app or maintenance operation is supported before promising a custom Nextcloud deployment. [Storage Share OCC](https://docs.hetzner.com/storage/storage-share/configuration/occ-commands/).

## Check application compatibility

Create a requirement matrix before ordering:

| Requirement | Evidence to obtain |
|---|---|
| PHP/Python/Perl/Node or another runtime | Supported version, invocation model, extensions and long-running-process policy |
| Database | Engine/version, available extensions, connection limits, import size and export/restore access |
| Background work | Cron limits, execution duration, queue-worker lifecycle and restart behavior |
| System dependency | Is it supplied, installable as a normal user, or dependent on root? |
| Persistent uploads | Quota, backup coverage, ownership and migration method |
| Mail | Domain setup, mailbox size, DNS records, delivery behavior and migration path |
| TLS | Certificate issuance, validation path, supported names and renewal responsibility |
| Availability | What is monitored and repaired by the provider; what must the application owner test? |

Do not infer package support merely because software runs on Linux. For example, a database extension requiring privileged installation is a separate compatibility question from whether PostgreSQL is present. Ask the current product documentation or support a precise question with the required version and operation.

## Separate domain registration from DNS

A domain involves three independent concerns: the registrar/registry delegation, authoritative DNS records, and the application hosting destination. Moving any one of them does not automatically migrate the other two. A DNS record update does not copy a website, database or mailbox.

For domains administered through konsoleH, its nameserver change operation updates registry delegation; editing NS records inside the zone alone is insufficient. If the registrar is external, change delegation there. Verify A and AAAA independently so an old IPv6 destination cannot keep serving stale content. [Current konsoleH DNS administration](https://docs.hetzner.com/managed/domain-and-dns/dnsadministration/).

Domain Registration Robot is another registration/administration product and must not be confused with free DNS hosting. Preserve the existing registrar and contract unless transfer is part of the requested change. [Documentation/control-plane map](https://docs.hetzner.com/).

## Handle current DNS integration

The current documentation puts primary DNS management in **Hetzner Console**. konsoleH retains hosting-related zone authorization and nameserver functions. Therefore, neither “all DNS is still the old DNS Console” nor “konsoleH has been discontinued” is a valid operating assumption. [DNS administration, updated 2026-08-31](https://docs.hetzner.com/managed/domain-and-dns/dnsadministration/).

DNS automation uses the current Cloud API and project-scoped credentials. The migration documentation explicitly states that old DNS Console tokens do not work with the new API. Integrations may also require provider-name, module-name or environment-variable changes. Inventory ACME clients, dynamic DNS, Terraform state, ExternalDNS and ad-hoc scripts before retiring old credentials. [DNS integration differences](https://docs.hetzner.com/networking/dns/migration-to-hetzner-console/features-and-differences/), [current DNS service](https://www.hetzner.com/dns/).

Treat a working browser record edit as only one migration test. Prove an automated create/read/update/delete cycle in an expendable record, then prove certificate renewal using the intended credential scope. Do not expose tokens in logs or migrate production by deleting and recreating the whole zone.

## Migrate in controlled stages

The provider's migration guide covers hosting, mail and domain transfer. Use it for product-specific steps; adapt sequencing to the application's write behavior and tolerated downtime. [Provider migration guide](https://docs.hetzner.com/managed/administration-on-konsoleh/change-of-provider/).

1. Inventory files, uploads, databases, cronjobs, mailboxes, aliases, redirects, certificates and DNS records. Export them before changes.
2. Provision the destination and validate the runtime matrix. Create the correct domain/hosting association so virtual-host and TLS behavior can be tested.
3. Copy static data, restore a database export and run application smoke tests against the destination without moving production traffic.
4. Plan final synchronization. For writes, use a short maintenance period or an application-aware replication/migration procedure; a DNS flip cannot resolve divergent databases.
5. Lower relevant TTLs ahead of time where useful, allowing old values to expire. Preserve mail authentication records and account for caches.
6. Move web traffic, inspect both IPv4 and IPv6, and test logins, uploads, background jobs and outgoing notifications.
7. Migrate mail with mailbox and alias verification. Allow for mail sent toward cached old MX records while the previous service is still available.
8. Transfer domain registration separately if needed. Confirm delegation and renewals, then cancel only the superseded products after acceptance and the chosen rollback window.

## Operate and verify

Maintain an application-level backup/export even when a hosting plan includes provider backups. Verify what can be restored, who can trigger it, granularity, retention and whether a full account restore would overwrite newer mail or data. Test a meaningful restore before a major application upgrade.

Record evidence that the public domain resolves to the intended nameservers and A/AAAA targets, TLS renews, mail reaches the correct destination, the application can write its data and scheduled tasks execute. Product health and application correctness are separate observations.
