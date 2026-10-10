# Automation, APIs, infrastructure as code, and bootstrap

Verified against primary sources on **2026-10-04**. Recheck API changelog, installed tool versions, provider schemas, images, locations, and live prices before execution. Examples below inspect resources; they do not provision infrastructure.

## Contents

- API selection and inventory
- Credentials and reliable requests
- Terraform/OpenTofu lifecycle
- Ansible and cloud-init
- Change runbook

## API selection and inventory

Use the [API overview](https://docs.hetzner.cloud/) to select the correct control plane: `https://api.hetzner.cloud/v1` for Cloud resources and Console DNS, `https://api.hetzner.com/v1` for Storage Boxes, and the separate Robot Webservice for dedicated servers. Object Storage uses its S3-compatible endpoint. A Cloud token is not a universal credential for every Hetzner product.

Useful Cloud API GET routes, as documented in the [Cloud reference](https://docs.hetzner.cloud/reference/cloud):

| Need | Route |
|---|---|
| Servers and creation choices | `/servers`, `/server_types`, `/images`, `/isos`, `/locations` |
| Network inventory | `/networks`, `/primary_ips`, `/floating_ips`, `/firewalls` |
| Application edge | `/load_balancers`, `/load_balancer_types`, `/certificates` |
| Persistence and placement | `/volumes`, `/placement_groups` |
| DNS | `/zones` and zone RRSet routes |
| Current catalog prices | `/pricing` |

Use resource-specific action endpoints for asynchronous work. Check the returned action until success/error, then read the resource again. An accepted request does not prove that an attachment, rebuild, or certificate operation finished.

Use `location`, not the removed `server.datacenter` / `primary_ip.datacenter` properties. Since **2026-10-01**, `/datacenters` and `/datacenters/{id}` return 410. Since September, `/networks/{id}/members` provides attachment inventory. Check per-location server-type deprecation data; the older `deprecated` fields have a further removal scheduled for **2026-11-02**. [API changelog](https://docs.hetzner.cloud/changelog)

For a previously configured, appropriate read-only context:

```bash
hcloud version
hcloud context list
hcloud api --method GET /locations
hcloud api --method GET /server_types
hcloud api --method GET /pricing
hcloud api --method GET --value page=1,per_page=50 /servers
```

`hcloud api` defaults to GET; use its explicit method and query options when constructing requests. Confirm current syntax with `hcloud api --help`. The API CLI command returns raw responses; follow pagination rather than assuming one page is complete. [Official CLI manual](https://github.com/hetznercloud/cli/blob/main/docs/reference/manual/hcloud_api.md)

Treat `/pricing` as the catalog for the project owner's currency and VAT, not a complete invoice or a guarantee of deployable capacity. Preserve net/gross distinction, location, traffic assumptions, retained resources, and any existing-server price conditions in estimates. [Pricing API](https://docs.hetzner.cloud/reference/cloud#pricing)

## Credentials and reliable requests

Create separate credentials per environment and automation purpose. Cloud API tokens belong to a project; read-only tokens allow GET, while read/write tokens also permit mutations. Prefer a read-only token for discovery. Verify the intended project using expected resource IDs/names before changing anything. [Token documentation](https://docs.hetzner.com/cloud/api/getting-started/generating-api-token/)

Supply `HCLOUD_TOKEN` through a secret manager or protected process environment. Never place real tokens in examples, shell history, source control, user-data, Terraform variables committed to disk, or public logs. Avoid debug output during authenticated work unless its handling is understood. Restrict project membership and rotate credentials after exposure.

Honor `RateLimit-*` headers and 429 responses; use bounded retries with jitter. Retry a timed-out mutation only after checking whether its resource/action already exists. For collection reads, follow `meta.pagination.next_page`/Link until exhausted. Do not hard-code one global request budget across separate APIs. [Cloud API request behavior](https://docs.hetzner.cloud/reference/cloud)

## Terraform/OpenTofu lifecycle

Use the official `hetznercloud/hcloud` provider; its upstream supports both Terraform and OpenTofu. Pin a reviewed provider release and tool version, retain the dependency lockfile, and inspect upgrades before changing the lock. Use provider documentation for the pinned release, not only `main`. [Provider repository](https://github.com/hetznercloud/terraform-provider-hcloud)

Before applying:

1. Inventory existing resources and import by documented IDs instead of recreating them.
2. Assign one owner for each property. Avoid having Terraform and a Kubernetes controller both manage the same Load Balancer service/targets.
3. Read every replacement in the plan, including changes to image, location, SSH-key injection, networking, or identity. Preserve database disks and addresses deliberately.
4. Review the saved plan in the same environment and state workspace that will apply it. Treat plan/state files as confidential; `sensitive` presentation flags are not encryption.
5. Keep a recovery path that works before network rules are changed.

The provider may **remove API delete protection while destroying a resource**. Use `lifecycle { prevent_destroy = true }` where Terraform-side protection is required; it protects while the lifecycle configuration remains present and is not a backup. [Provider protection semantics](https://registry.terraform.io/providers/hetznercloud/hcloud/latest/docs/index) [Terraform lifecycle](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#prevent_destroy)

For `hcloud_server`, explicitly configure `public_net` if public IP creation is unwanted. Use a supported subnet dependency (`subnet_id` on versions supporting it, or an explicit subnet dependency); network creation alone is insufficient. Changing injected `ssh_keys` can trigger replacement; rotate guest keys through configuration management instead. Recheck documented `alias_ips = []` workarounds against the pinned provider. [Server resource](https://github.com/hetznercloud/terraform-provider-hcloud/blob/main/docs/resources/server.md)

## Ansible and cloud-init

Use the maintained `hetzner.hcloud` collection for discovery/provisioning and its dynamic inventory for configuration management. Pin collection/Python dependencies. Choose `server_info` or inventory for read-only discovery, scope labels deliberately, and explicitly select private connection addresses plus bastion/VPN access. Check mode is module-specific. [Collection](https://docs.ansible.com/projects/ansible/latest/collections/hetzner/hcloud/index.html) [Inventory](https://docs.ansible.com/projects/ansible/latest/collections/hetzner/hcloud/hcloud_inventory.html)

Distinguish first-boot configuration from ongoing management. Establish routing, DNS, repository/registry access, and time synchronization before package-install/bootstrap steps depend on them. A private interface being configured does not create internet egress.

Current Hetzner images configure private interfaces through cloud-init 25.3+ or `hc-utils`, depending on image. Identify the actual owner before overriding configuration; avoid competing DHCP clients. Persist and reboot-test custom routes. Do not universally remove `hc-utils` from every image or assume an interface is named `eth1`. [Network configuration](https://docs.hetzner.com/networking/networks/server-configuration/)

Keep user-data nonsecret: install public keys, public configuration, and bootstrap logic, then obtain narrowly scoped secrets through a controlled channel. Cloud-init retains sensitive instance/user-data on disk; review and sanitize captured diagnostics. Validate YAML before deployment and inspect `cloud-init status --long` plus its logs after boot. [Cloud-init instance data](https://cloudinit.readthedocs.io/en/latest/topics/instancedata.html)

## Change runbook

Record desired state, project, affected IDs, price effect, dependencies, and rollback. Read inventory; generate the change; inspect the plan; perform the authorized operation; await actions; verify guest networking and application behavior; record remaining drift. For outages, first preserve evidence and a working management connection instead of repeatedly rebuilding resources.
