# Secure writable registry + separate Hub cache

This is a **configuration template**, not a deploy-and-forget production stack. The two instances have separate storage, HTTP secrets, TLS files, and htpasswd inputs. No upstream private-account credentials are supplied. The writable registry has deletion disabled; the cache enables deletion for scheduler maintenance.

## Required provisioning

Provide `tls/registry.crt`, `tls/registry.key`, `tls/cache.crt`, `tls/cache.key`, `auth/registry.htpasswd`, and `auth/cache.htpasswd`. Use certificates valid for the exact hostnames clients use, with complete chains and appropriate SANs. Generate bcrypt htpasswd entries through a trusted interactive tool; do not put plaintext passwords on a process command line. Restrict file access and protect key backups.

Copy `.env.example` to an untracked `.env`, select the reviewed registry image, and generate two independent high-entropy HTTP secrets through your approved process. All replicas of **one** deployment need the same stable secret; the writable registry and cache here are separate deployments. Environment-based secret delivery is used for clarity and is visible to Docker administrators; use a suitable secret manager/provisioning wrapper where required. Never commit the completed file or share rendered `config` output.

Validate with `docker compose -f compose.yaml config -q`. File existence, certificate validity, auth behavior, and image/runtime compatibility require separate tests. Loopback bindings are the default; choosing another interface is an exposure decision requiring firewall/TLS/auth review.

## Client validation

Test expected anonymous 401 behavior, authenticated access, a writable-registry push, rejection of a push to the cache, and manifest/blob pulls from every intended client. Native htpasswd is authentication, not repository-level RBAC. Prefer a suitable authorization service/platform for per-repository permissions.

An authenticated cache is not transparently compatible with every Docker Hub mirror client configuration. Test how each Docker/containerd/BuildKit client supplies mirror credentials. Do not weaken downstream auth or add broad upstream private credentials merely to make a test pass. Network-restricted alternatives require an explicit threat model.

## Operations

Read [configuration timing](../../references/operations/config-files-and-reload.md), [TLS](../../references/deployment/tls-and-private-access.md), and [cache design](../../references/mirrors/pull-through-design.md). Production additionally needs tested backups, monitored storage, resource sizing, rotation, controlled upgrades, and a GC maintenance plan. No certificates, passwords, or live endpoint assumptions are bundled.
